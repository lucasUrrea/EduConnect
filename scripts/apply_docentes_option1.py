import os, sys, json, datetime
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
import django
django.setup()
from django.core import serializers
from EduConnectApp.models import Docentes

FIXTURE = os.path.join(project_root, 'edudata.utf8.json')
BACKUP_DIR = os.path.join(project_root, 'backups')
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Backup current docentes
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = os.path.join(BACKUP_DIR, f'docentes_backup_{timestamp}.json')
with open(backup_file, 'w', encoding='utf-8') as f:
    f.write(serializers.serialize('json', Docentes.objects.all()))
print(f'Backed up docentes to {backup_file}')

# Load fixture and find docentes entry
with open(FIXTURE, 'r', encoding='utf-8') as f:
    data = json.load(f)

docente_fixture = None
for obj in data:
    if obj.get('model', '').lower() == 'educonnectapp.docentes':
        docente_fixture = obj
        break

if not docente_fixture:
    print('No docentes object in fixture. Nothing to apply.')
    sys.exit(0)

fields = docente_fixture.get('fields', {})
fixture_id_usuario = fields.get('id_usuario')
fixture_codigo = fields.get('codigo_docente')

if not fixture_id_usuario:
    print('Fixture docentes has no id_usuario; aborting safe update.')
    sys.exit(1)

# Find existing docentes row that owns this usuario (this is option 1 target)
target = Docentes.objects.filter(id_usuario_id=fixture_id_usuario).first()
if not target:
    print(f'No existing Docentes row owns id_usuario={fixture_id_usuario}; aborting.')
    sys.exit(1)

print(f'Target docentes found: pk={target.pk}, id_usuario_id={target.id_usuario_id}, codigo_docente={target.codigo_docente}')

# Apply non-null fixture fields to target, but skip codigo_docente to avoid unique-conflict
changed = False
for fname, val in fields.items():
    if fname in ('id_usuario', 'codigo_docente'):
        continue
    if val is None:
        # skip nulls to avoid overwriting existing data with nulls
        continue
    # set attribute if different
    if hasattr(target, fname):
        current = getattr(target, fname)
        # if datetime strings appear, leave unchanged (models will parse if needed) — simple comparison
        if isinstance(current, (str, int, float, type(None))) or True:
            if current != val:
                setattr(target, fname, val)
                changed = True

if changed:
    target.save()
    print(f'Applied fixture non-null fields to docentes pk={target.pk}')
else:
    print('No non-null fields in fixture to apply (or values identical). No update performed.')

print('Done.')
