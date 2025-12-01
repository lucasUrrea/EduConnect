import os
import sys
import django
import pathlib

proj_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(proj_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
django.setup()

from EduConnectApp.models import Consultas
from django.conf import settings
from django.test import Client

# inspect latest consulta
new = Consultas.objects.order_by('-id_consulta').first()
if not new:
    print('No consultas found')
    sys.exit(1)

print('Consulta id=', new.id_consulta)
for f in ['titulo','descripcion','prioridad','estado','fecha_consulta','adjunto_archivo','created_at','updated_at']:
    val = getattr(new, f, None)
    print(f'{f}:', val)

# list files under MEDIA_ROOT/adjuntos
adj_dir = os.path.join(settings.MEDIA_ROOT, 'adjuntos')
print('\nMEDIA_ROOT:', settings.MEDIA_ROOT)
print('Adjuntos dir:', adj_dir)
if os.path.exists(adj_dir):
    print('Files in adjuntos:')
    for name in os.listdir(adj_dir):
        print('  ', name)
else:
    print('Adjuntos dir not found')

# render mis-consultas (correct path) and save
c = Client()
# attempt to set session for the consulta's estudiante
try:
    est = new.id_estudiante
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
    print('Could not set session:', e)

resp = c.get('/mis-consultas/')
print('\nGET /mis-consultas/ status_code=', resp.status_code)
html = resp.content.decode('utf-8')
path = pathlib.Path('tmp/mis_consultas_render2.html')
path.write_text(html, encoding='utf-8')
print('Saved', path.resolve())

if new.titulo in html:
    print('Title found in rendered mis-consultas HTML')
else:
    print('Title NOT found in rendered mis-consultas HTML')
