import os, sys, pathlib
proj_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(proj_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
import django
django.setup()

from EduConnectApp.models import Consultas
from django.conf import settings

# Delete consultas with the test title
qs = Consultas.objects.filter(titulo='Prueba creación automática')
print('Found', qs.count(), 'test consultas to delete')
for c in qs:
    print('Deleting consulta id=', c.id_consulta, 'adjunto=', c.adjunto_archivo)
    c.delete()

# remove test file if exists
adj = pathlib.Path(settings.MEDIA_ROOT) / 'adjuntos' / 'test.txt'
if adj.exists():
    adj.unlink()
    print('Removed', adj)
else:
    print('No test file to remove at', adj)
