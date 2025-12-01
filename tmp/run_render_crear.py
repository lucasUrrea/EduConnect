import os
import sys
import django
import pathlib

# ensure project root is on sys.path so `modulos_consultas` can be imported
proj_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(proj_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
django.setup()
from django.test import Client
from EduConnectApp.models import Estudiantes

c = Client()
est = Estudiantes.objects.first()
if not est:
    print('No estudiantes found')
else:
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
    resp = c.get('/consulta/crear/')
    out = resp.content.decode('utf-8')
    p = pathlib.Path('tmp/crear_consulta_render.html')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(out, encoding='utf-8')
    print('Saved', p.resolve())
