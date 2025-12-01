import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulos_consultas.settings')
import django
django.setup()
from EduConnectApp.models import Estudiantes, Consultas
from django.utils import timezone

est = Estudiantes.objects.first()
print('Using Estudiante:', est.id_estudiante if est else None)
count_before = Consultas.objects.count()
print('consultas before:', count_before)
if est:
    c = Consultas(
        id_estudiante=est,
        id_asignatura=est.id_usuario and None,
        titulo='Test creación rápida',
        descripcion='Prueba de creación desde script',
        fecha_consulta=timezone.now(),
        estado='pendiente'
    )
    # set id_asignatura properly: pick first asignatura
    from EduConnectApp.models import Asignaturas
    asign = Asignaturas.objects.first()
    if asign:
        c.id_asignatura = asign
    else:
        print('No asignaturas available; aborting creation')
        exit(1)
    c.save()
    print('Created consulta id:', c.id_consulta)
    print('consultas after:', Consultas.objects.count())
else:
    print('No estudiantes found; cannot create test consulta')
