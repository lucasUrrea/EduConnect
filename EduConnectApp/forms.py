from django import forms
from .models import Consultas, Respuestas


class ProfileForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    apellido_paterno = forms.CharField(max_length=100, required=True)
    telefono = forms.CharField(max_length=20, required=False)


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consultas
        fields = ['id_asignatura', 'id_categoria', 'titulo', 'descripcion', 'prioridad', 'adjunto_archivo']


class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuestas
        fields = ['contenido_respuesta', 'tipo_respuesta', 'adjunto_archivo']
        widgets = {
            'contenido_respuesta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Escribe tu respuesta aquí...'
            }),
            'tipo_respuesta': forms.Select(attrs={
                'class': 'form-select'
            }),
            'adjunto_archivo': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
