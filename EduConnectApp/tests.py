from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import Usuarios, Estudiantes, Asignaturas, Consultas, Docentes, Respuestas
from rest_framework.test import APIClient


class APITest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = Usuarios.objects.create(
			email='apiuser@example.com',
			password_hash=make_password('apipass'),
			tipo_usuario='estudiante',
			nombre='Api',
			apellido_paterno='User',
			estado='activo'
		)
		self.estudiante = Estudiantes.objects.create(id_usuario=self.user, numero_matricula='MATAPI')
		# create corresponding django user
		from django.contrib.auth.models import User
		django_user = User.objects.create_user(username=self.user.email, email=self.user.email, password='apipass')
		self.client.login(username=self.user.email, password='apipass')

	def test_api_create_consulta(self):
		asig = Asignaturas.objects.create(codigo_asignatura='AP1', nombre_asignatura='API Test')
		data = {
			'id_estudiante': self.estudiante.id_estudiante,
			'id_asignatura': asig.id_asignatura,
			'titulo': 'Consulta API',
			'descripcion': 'Prueba via API'
		}
		resp = self.client.post('/api/consultas/', data, format='json')
		self.assertEqual(resp.status_code, 201)


class BasicModelsTest(TestCase):
	def setUp(self):
		# crear usuario y estudiante
		self.user = Usuarios.objects.create(
			email='estudiante@example.com',
			password_hash=make_password('s3cret'),
			tipo_usuario='estudiante',
			nombre='Test',
			apellido_paterno='User',
			estado='activo'
		)

		self.estudiante = Estudiantes.objects.create(
			id_usuario=self.user,
			numero_matricula='MAT123'
		)

		self.asig = Asignaturas.objects.create(
			codigo_asignatura='ASIG101',
			nombre_asignatura='Introduccion'
		)

	def test_create_consulta_and_respuesta(self):
		consulta = Consultas.objects.create(
			id_estudiante=self.estudiante,
			id_asignatura=self.asig,
			titulo='Necesito ayuda',
			descripcion='Descripcion de prueba',
			fecha_consulta=timezone.now()
		)

		# crear docente y respuesta
		user_doc = Usuarios.objects.create(
			email='docente@example.com',
			password_hash=make_password('docpass'),
			tipo_usuario='docente',
			nombre='Doc',
			apellido_paterno='Tor',
			estado='activo'
		)

		docente = Docentes.objects.create(
			id_usuario=user_doc,
			codigo_docente='DOC123'
		)

		respuesta = Respuestas.objects.create(
			id_consulta=consulta,
			id_docente=docente,
			contenido_respuesta='Respuesta de prueba',
			fecha_respuesta=timezone.now()
		)

		self.assertEqual(Consultas.objects.count(), 1)
		self.assertEqual(Respuestas.objects.count(), 1)


class ViewsExtraTest(TestCase):
	def setUp(self):
		from django.contrib.auth.models import User
		from django.contrib.auth.hashers import make_password
		# crear docente y estudiante
		self.user_doc = Usuarios.objects.create(
			email='docview@example.com',
			password_hash=make_password('docpass'),
			tipo_usuario='docente',
			nombre='Doc',
			apellido_paterno='Viewer',
			estado='activo'
		)
		self.docente = Docentes.objects.create(id_usuario=self.user_doc, codigo_docente='DVIEW')

		self.user_est = Usuarios.objects.create(
			email='estview@example.com',
			password_hash=make_password('estpass'),
			tipo_usuario='estudiante',
			nombre='Est',
			apellido_paterno='Viewer',
			estado='activo'
		)
		self.estudiante = Estudiantes.objects.create(id_usuario=self.user_est, numero_matricula='MV1')

		# asignatura y consulta
		self.asig = Asignaturas.objects.create(codigo_asignatura='ASG1', nombre_asignatura='Asign1')
		self.cons = Consultas.objects.create(id_estudiante=self.estudiante, id_asignatura=self.asig, titulo='Pregunta', fecha_consulta=timezone.now())

		# crear django user for login
		django_doc = User.objects.create_user(username=self.user_doc.email, email=self.user_doc.email, password='docpass')
		django_est = User.objects.create_user(username=self.user_est.email, email=self.user_est.email, password='estpass')

		self.client.login(username=self.user_doc.email, password='docpass')

	def test_mi_progreso_context(self):
		# login como estudiante
		self.client.logout()
		self.client.login(username=self.user_est.email, password='estpass')
		resp = self.client.get('/mi-progreso/')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('labels', resp.context)
		self.assertIn('values', resp.context)

	def test_panel_docente_access(self):
		resp = self.client.get('/panel/docente/')
		self.assertEqual(resp.status_code, 200)
		# debe contener la tabla de consultas
		self.assertContains(resp, 'Consultas Recientes')


class FileUploadTest(TestCase):
	def setUp(self):
		from django.contrib.auth.models import User
		from django.contrib.auth.hashers import make_password
		self.user = Usuarios.objects.create(
			email='filetest@example.com',
			password_hash=make_password('filepass'),
			tipo_usuario='estudiante',
			nombre='File',
			apellido_paterno='Tester',
			estado='activo'
		)
		self.est = Estudiantes.objects.create(id_usuario=self.user, numero_matricula='FT1')
		User.objects.create_user(username=self.user.email, email=self.user.email, password='filepass')
		self.client.login(username=self.user.email, password='filepass')

		self.asig = Asignaturas.objects.create(codigo_asignatura='FUP1', nombre_asignatura='FileUpload')

	def test_create_consulta_with_file(self):
		from django.core.files.uploadedfile import SimpleUploadedFile
		# Arrange
		before = Consultas.objects.count()
		f = SimpleUploadedFile('upload.txt', b'hello world', content_type='text/plain')
		data = {
			'id_asignatura': str(self.asig.id_asignatura),
			'id_categoria': '',
			'titulo': 'Test with file',
			'descripcion': 'Testing file upload',
			'prioridad': 'media',
			'tipo_consulta': 'consulta_general'
		}

		# ensure session contains usuario_id (middleware may not populate in test client)
		session = self.client.session
		session['usuario_id'] = self.user.id_usuario
		session['tipo_usuario'] = 'estudiante'
		session.save()

		# Act: include file in data so client builds multipart form
		post_data = data.copy()
		post_data['adjunto_archivo'] = f
		resp = self.client.post('/consulta/crear/', data=post_data, follow=True)
		self.assertIn(resp.status_code, (200, 302))

		# Assert
		after = Consultas.objects.count()
		self.assertEqual(after, before + 1)
		new = Consultas.objects.order_by('-id_consulta').first()
		self.assertTrue(bool(new.adjunto_archivo), msg=f"Adjunto not saved, value={new.adjunto_archivo}")

		# render mis-consultas and ensure link text is present
		resp2 = self.client.get('/mis-consultas/')
		self.assertEqual(resp2.status_code, 200)
		self.assertContains(resp2, 'Adjunto')

	def tearDown(self):
		# Remove any uploaded files created during the test to avoid leaving artifacts on disk
		try:
			for c in Consultas.objects.filter(id_estudiante=self.est).exclude(adjunto_archivo__isnull=True).exclude(adjunto_archivo__exact=''):
				try:
					# Use the FileField delete helper which delegates to the storage backend
					if getattr(c.adjunto_archivo, 'name', None):
						c.adjunto_archivo.delete(save=False)
				except Exception:
					# ignore deletion errors in cleanup
					pass
		except Exception:
			pass
