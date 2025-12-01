import os
import sys
import django
import pathlib

proj_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(proj_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
django.setup()

from EduConnectApp.models import Consultas, Estudiantes
from django.conf import settings
from django.test import Client

# Find latest consulta
new = Consultas.objects.order_by('-id_consulta').first()
if not new:
    print('No consultas found')
    sys.exit(1)

print('Found consulta: id=', new.id_consulta)
print('  titulo:', new.titulo)
print('  id_estudiante:', getattr(new.id_estudiante, 'id_estudiante', new.id_estudiante_id))
print('  id_asignatura:', getattr(new.id_asignatura, 'id_asignatura', new.id_asignatura_id))
print('  adjunto_archivo (field):', new.adjunto_archivo)
print('  adjunto name:', getattr(new.adjunto_archivo, 'name', None))

# Check file existence
media_root = settings.MEDIA_ROOT
adj_name = getattr(new.adjunto_archivo, 'name', None)
if adj_name:
    abs_path = os.path.join(media_root, adj_name)
    exists = os.path.exists(abs_path)
    print('  expected path:', abs_path)
    print('  exists on filesystem?', exists)
else:
    print('  No adjunto file name present')

# Render mis_consultas page with student's session and save HTML
c = Client()
# find the estudiante object
est = getattr(new, 'id_estudiante', None)
if est is None:
    print('  cannot locate estudiante foreign object, aborting render')
else:
    # login or set session
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        u = User.objects.filter(username=est.id_usuario.email).first()
        if u:
            c.force_login(u)
        else:
            s = c.session
            s['usuario_id'] = est.id_usuario.id_usuario
            s['tipo_usuario'] = 'estudiante'
            s['nombre_completo'] = est.id_usuario.nombre + ' ' + est.id_usuario.apellido_paterno
            s.save()
    except Exception as e:
        s = c.session
        s['usuario_id'] = est.id_usuario.id_usuario
        s['tipo_usuario'] = 'estudiante'
        s['nombre_completo'] = est.id_usuario.nombre + ' ' + est.id_usuario.apellido_paterno
        s.save()

    resp = c.get('/mis_consultas/')
    out = resp.content.decode('utf-8')
    p = pathlib.Path('tmp/mis_consultas_render.html')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(out, encoding='utf-8')
    print('Saved mis_consultas render to', p.resolve())

    # Quick check: look for the title text in the HTML
    if new.titulo and new.titulo in out:
        print('  ✅ The new consulta title was found in the rendered mis_consultas HTML')
    else:
        print('  ⚠️ The new consulta title was NOT found in the rendered mis_consultas HTML')
