
from django import forms
from django.contrib.auth import authenticate
from .models import Usuario,Escuela, Pregunta, Puntuación
import re

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Usuario
        fields = ['first_name','last_name','school','username','password',"password2"]
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data
    

#FORMULARIO DE INGRESO
class IngresarForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    
#FORMULARIO PARA AGREGAR ESCUELAS
class IngresarEscuelaForm(forms.ModelForm):
    class Meta:
        model = Escuela
        fields = ["nombre_escuela","direccion_escuela","numero_escuela", "localidad_escuela"]

    def clean_nombre_escuela(self):
        nombre_escuela = self.cleaned_data.get('nombre_escuela')
        if Escuela.objects.filter(nombre_escuela=nombre_escuela).exists():
            raise forms.ValidationError("El nombre de la escuela ya ha está registrado")
        return nombre_escuela
    def clean_numero_escuela(self):
        numero_escuela = self.cleaned_data.get('numero_escuela')
        if not isinstance(numero_escuela, int):
            raise forms.ValidationError('El número de escuela debe ser un valor numérico.')
        return numero_escuela
    

class IngresarPreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ["texto_pregunta",]
        
    def clean_texto_pregunta(self):
        texto_pregunta = self.cleaned_data.get('texto_pregunta')
    
        if not re.match("^[A-Za-z0-9 ¿?¡!]+$", texto_pregunta):
            raise forms.ValidationError("La pregunta solo debe contener letras, números, espacios y los símbolos ¿?¡!.")
        return texto_pregunta
    
class PuntarPreguntasForm(forms.ModelForm):
    class Meta:
        model = Puntuación
        fields = ["pregunta","puntuacion"]
