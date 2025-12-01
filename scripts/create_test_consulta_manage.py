from EduConnectApp.models import Estudiantes, Consultas, Asignaturas
from django.utils import timezone

est = Estudiantes.objects.first()
print('Using Estudiante:', getattr(est, 'id_estudiante', None))
print('consultas before:', Consultas.objects.count())
if est:
    asign = Asignaturas.objects.first()
    if not asign:
        print('No asignaturas available; aborting creation')
    else:
        c = Consultas(id_estudiante=est, id_asignatura=asign, titulo='Test creación manage shell', descripcion='Prueba', fecha_consulta=timezone.now(), estado='pendiente')
        c.save()
        print('Created consulta id:', getattr(c, 'id_consulta', None))
        print('consultas after:', Consultas.objects.count())
else:
    print('No estudiantes found; cannot create test consulta')
