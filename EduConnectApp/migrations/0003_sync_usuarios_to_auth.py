from django.db import migrations


def sync_usuarios_to_auth(apps, schema_editor):
    Usuarios = apps.get_model('EduConnectApp', 'Usuarios')
    User = apps.get_model('auth', 'User')
    for u in Usuarios.objects.all():
        if not User.objects.filter(username=u.email).exists():
            user = User.objects.create(username=u.email, email=u.email, first_name=u.nombre or '', last_name=u.apellido_paterno or '')
            # si password_hash ya está hasheado con django, lo copiamos; si no, dejamos sin password
            try:
                # intentar detectar si parece un hash de Django (pbkdf2)
                if u.password_hash and u.password_hash.startswith('pbkdf2_'):
                    user.password = u.password_hash
                    user.save()
            except Exception:
                pass


class Migration(migrations.Migration):

    dependencies = [
        ('EduConnectApp', '0002_alter_consultas_adjunto_archivo_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(sync_usuarios_to_auth, migrations.RunPython.noop),
    ]
