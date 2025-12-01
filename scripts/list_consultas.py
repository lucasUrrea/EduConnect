from EduConnectApp.models import Consultas

qs = Consultas.objects.all().order_by('-fecha_consulta')[:10]
print('Últimas consultas (hasta 10):')
for c in qs:
    try:
        est = f'{c.id_estudiante.id_estudiante} (usuario {c.id_estudiante.id_usuario})'
    except Exception:
        est = str(c.id_estudiante)
    print(c.id_consulta, est, c.titulo, c.fecha_consulta, c.estado)
