import os, sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
import django
django.setup()
from EduConnectApp.models import Docentes, Usuarios

print('Docentes:')
for d in Docentes.objects.all():
    print(d.pk, 'id_usuario=', getattr(d,'id_usuario_id',None))
print('\nUsuarios:')
for u in Usuarios.objects.all():
    print(u.pk, u.email)
