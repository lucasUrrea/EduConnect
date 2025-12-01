import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','modulos_consultas.settings')
import django
django.setup()
from django.core.management import call_command
with open('edudata.json','w',encoding='utf-8') as f:
    call_command('dumpdata','EduConnectApp','--indent','2', stdout=f)
print('Wrote edudata.json')
