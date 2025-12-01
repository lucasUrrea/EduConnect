"""Merge a JSON fixture into the database without creating duplicate PK conflicts.

Usage: python scripts/merge_fixture.py

This script loads `edudata.utf8.json`, then for each object it will either create it (with the same PK)
or update the existing row with the fixture fields. It processes models in an order that
attempts to satisfy foreign-key dependencies.

Be cautious: this runs against whatever DATABASES setting is active (MariaDB if USE_SQLITE unset).
"""
import os
import json
import sys
from django.db import transaction, IntegrityError
from django.utils.dateparse import parse_datetime

# Setup Django
# ensure project root is on sys.path so the settings module can be imported
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
import django
django.setup()
from django.apps import apps

FIXTURE = 'edudata.utf8.json'
if not os.path.exists(FIXTURE):
    print(f"Fixture {FIXTURE} not found. Create it first or adjust the filename.")
    sys.exit(1)

with open(FIXTURE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Group objects by model label (lowercase model name)
by_model = {}
for obj in data:
    model_label = obj['model'].split('.')[-1].lower()
    by_model.setdefault(model_label, []).append(obj)

# Define a processing order to satisfy FK dependencies (common for this app)
preferred_order = [
    'usuarios',
    'asignaturas',
    'categoriastemas',
    'docentes',
    'estudiantes',
    'docenteasignatura',
    'consultas',
    'respuestas',
]

# Add any remaining models at the end
remaining = [m for m in by_model.keys() if m not in preferred_order]
order = [m for m in preferred_order if m in by_model] + remaining

print('Processing order:', order)

created = 0
updated = 0
skipped = 0
errors = []

for model_name in order:
    objs = by_model.get(model_name, [])
    full_label = None
    # find the full app.model label from first matching entry
    for o in objs:
        full_label = o['model']
        break
    if not full_label:
        continue
    app_label, model_cls_name = full_label.split('.')
    Model = apps.get_model(app_label, model_cls_name)
    print(f"\n=== Processing {app_label}.{model_cls_name} ({len(objs)} objects) ===")

    for o in objs:
        pk = o['pk']
        fields = o['fields']
        # Prepare kwargs for creation/update
        kwargs = {}
        fk_assignments = {}
        for fname, val in fields.items():
            # skip auto fields if null
            if val is None:
                kwargs[fname] = None
                continue
            try:
                f = Model._meta.get_field(fname)
            except Exception:
                # Field not found (maybe historic field) - skip
                kwargs[fname] = val
                continue
            # Handle relations
            if f.is_relation and not f.many_to_many:
                # val should be a PK reference
                if val is None or val == '':
                    kwargs[fname] = None
                else:
                    rel_model = f.related_model
                    try:
                        rel_inst = rel_model.objects.get(pk=val)
                        kwargs[fname] = rel_inst
                    except rel_model.DoesNotExist:
                        # We'll try to resolve later by storing assignment
                        fk_assignments[fname] = val
            else:
                # Convert datetimes
                if f.get_internal_type() in ('DateTimeField', 'DateField') and isinstance(val, str):
                    try:
                        kwargs[fname] = parse_datetime(val) or val
                    except Exception:
                        kwargs[fname] = val
                else:
                    kwargs[fname] = val

        # Upsert: try to find existing instance by pk; if not found, try to locate by unique fields
        # Special pre-check for docentes: prefer matching by id_usuario or codigo_docente to avoid OneToOne/unique conflicts
        if model_name == 'docentes':
            uid_val = fields.get('id_usuario')
            cod_val = fields.get('codigo_docente')
            uid_inst = None
            cod_inst = None
            if uid_val:
                try:
                    uid_inst = Model.objects.filter(id_usuario_id=uid_val).first()
                except Exception:
                    uid_inst = None
            if cod_val:
                try:
                    cod_inst = Model.objects.filter(codigo_docente=cod_val).first()
                except Exception:
                    cod_inst = None

            # If both found and they differ, prefer the one that already owns the codigo_docente to avoid unique conflicts
            chosen = None
            if cod_inst:
                chosen = cod_inst
            elif uid_inst:
                chosen = uid_inst

            if chosen:
                inst = chosen
                # update chosen row safely: avoid setting codigo_docente to a value that conflicts (already owned)
                for k, v in kwargs.items():
                    # skip assigning codigo_docente if it would duplicate another row (and not this one)
                    if k == 'codigo_docente' and cod_inst and cod_inst.pk != inst.pk:
                        continue
                    setattr(inst, k, v)
                try:
                    inst.save()
                except Exception as e:
                    print(f"Warning: saving docentes pk={inst.pk} failed: {e}")
                else:
                    updated += 1
                    print(f"Updated docentes by pre-match pk={inst.pk}")
                    # Try to resolve any deferred FK assignments
                    if fk_assignments:
                        changed = False
                        for fname, refpk in fk_assignments.items():
                            f = Model._meta.get_field(fname)
                            rel_model = f.related_model
                            try:
                                rel_inst = rel_model.objects.get(pk=refpk)
                                setattr(inst, fname, rel_inst)
                                changed = True
                            except rel_model.DoesNotExist:
                                print(f"Warning: related {rel_model} pk={refpk} not found for {model_name}.{fname}")
                        if changed:
                            inst.save()
                continue

        
        try:
            with transaction.atomic():
                inst = None
                try:
                    inst = Model.objects.get(pk=pk)
                    # special-case: if updating Docentes and id_usuario in kwargs points to a different existing Docentes,
                    # prefer updating the existing Docentes row that owns that id_usuario to avoid OneToOne duplicate errors.
                    if model_name == 'docentes' and 'id_usuario' in kwargs and kwargs['id_usuario'] is not None:
                        new_uid = kwargs['id_usuario'].pk if hasattr(kwargs['id_usuario'], 'pk') else kwargs['id_usuario']
                        other = Model.objects.filter(id_usuario_id=new_uid).exclude(pk=pk).first()
                        if other:
                            print(f"Conflict: docentes pk={pk} would be set to id_usuario={new_uid} which is already owned by pk={other.pk}; updating that existing row instead.")
                            inst = other
                    # update fields
                    for k, v in kwargs.items():
                        setattr(inst, k, v)
                    inst.save()
                    updated += 1
                    print(f"Updated {model_name} pk={inst.pk}")
                except Model.DoesNotExist:
                    # try to find by unique or OneToOne fields present in kwargs
                    found = False
                    for f in Model._meta.fields:
                        fname = f.name
                        if (getattr(f, 'unique', False) or f.get_internal_type() == 'OneToOneField') and fname in kwargs and kwargs[fname] is not None:
                            qval = kwargs[fname]
                            # if it's a model instance, use its pk
                            try:
                                if hasattr(qval, 'pk'):
                                    qval = qval.pk
                                existing = Model.objects.filter(**{fname: qval}).first()
                                if existing:
                                    inst = existing
                                    for k, v in kwargs.items():
                                        setattr(inst, k, v)
                                    inst.save()
                                    updated += 1
                                    print(f"Updated existing {model_name} by unique field {fname} pk={inst.pk}")
                                    found = True
                                    break
                            except Exception:
                                continue
                    if not found:
                        # special-case handling for Docentes to avoid OneToOne duplication
                        if model_name == 'docentes' and ('id_usuario' in fields and fields['id_usuario'] is not None):
                            uid_val = fields['id_usuario']
                            try:
                                uid_pk = uid_val
                                existing = Model.objects.filter(id_usuario_id=uid_pk).first()
                                if existing:
                                    # update existing docentes record with fixture data
                                    inst = existing
                                    for k, v in kwargs.items():
                                        setattr(inst, k, v)
                                    inst.save()
                                    updated += 1
                                    print(f"Updated existing docentes by id_usuario pk={existing.pk} (skip creating pk={pk})")
                                    found = True
                            except Exception:
                                pass

                    if not found:
                        # create new instance with pk
                        obj_kwargs = kwargs.copy()
                        obj_kwargs['pk'] = pk
                        inst = Model.objects.create(**obj_kwargs)
                        created += 1
                        print(f"Created {model_name} pk={pk}")

                # Try to resolve any deferred FK assignments
                if fk_assignments and inst is not None:
                    changed = False
                    for fname, refpk in fk_assignments.items():
                        f = Model._meta.get_field(fname)
                        rel_model = f.related_model
                        try:
                            rel_inst = rel_model.objects.get(pk=refpk)
                            setattr(inst, fname, rel_inst)
                            changed = True
                        except rel_model.DoesNotExist:
                            print(f"Warning: related {rel_model} pk={refpk} not found for {model_name}.{fname}")
                    if changed:
                        inst.save()
        except IntegrityError as ie:
            msg = f"IntegrityError for {model_name} pk={pk}: {ie}"
            print(msg)
            errors.append(msg)
        except Exception as exc:
            msg = f"Error for {model_name} pk={pk}: {exc}"
            print(msg)
            errors.append(msg)

print('\nSummary:')
print(f'  created: {created}')
print(f'  updated: {updated}')
print(f'  skipped: {skipped}')
print(f'  errors: {len(errors)}')
if errors:
    for e in errors[:20]:
        print('  ', e)

print('\nDone.')
