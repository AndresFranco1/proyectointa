
from django import forms
from django.contrib.auth import authenticate
from .models import Usuario,Escuela, Pregunta, Puntuación, ImagenUsuario
import re

class UsuarioForm(forms.ModelForm):#recopila la información necesaria para poder crear un usuario
    password = forms.CharField(widget=forms.PasswordInput)#campos para la contraseña. PasswordInput convierte la entrada en puntos
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Usuario#se basa en el modelo Usuario para poder crearlo
        fields = ['first_name','last_name','school','username','password',"password2"]#campos que va a tener cada una de las instancias "Usuario"
    
    def clean(self):#sirve para hace validacioens adicionales antes de guardar los datos
        cleaned_data = super().clean()#procesa y valida los datos básicos del formulario
        password = cleaned_data.get("password")#obtiene los valores de las contraseñas. El .get() es para que no retorne errores si no existe el valor
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            #primero valida si pass y pass2 existen
            #despues valida si son distintas, en caso de serlo (true) lanza el error
            raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data #retorna los datos limpios y validados 
    

#FORMULARIO DE INGRESO
class IngresarForm(forms.Form):#.Form indica que es un formulario manual, no de django como ModelForm.
    #La información que entra no se guarda en la base de datos
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    
#FORMULARIO PARA AGREGAR ESCUELAS
class IngresarEscuelaForm(forms.ModelForm):
    class Meta:
        model = Escuela #cada respuesta al formulario crea una instancia del modelo Escuela
        fields = ["nombre_escuela","direccion_escuela","numero_escuela", "localidad_escuela"]
        #ccampos que va a tener cada una de las instancias "Escuela"

    def clean_nombre_escuela(self):
        nombre_escuela = self.cleaned_data.get('nombre_escuela')
        if Escuela.objects.filter(nombre_escuela=nombre_escuela).exists(): 
            #valida si el nombre ingresado ya está registrado, si es así (true) lanza el error
            raise forms.ValidationError("El nombre de la escuela ya ha está registrado")
        return nombre_escuela
    
    def clean_numero_escuela(self):
        numero_escuela = self.cleaned_data.get('numero_escuela')
        if not isinstance(numero_escuela, int):
            #valida si el numero ingresado es de tipo int, si no lo es (true) lanza el error
            raise forms.ValidationError('El número de escuela debe ser un valor numérico.')
        return numero_escuela
    
#FORMULARIO PARA INGRESAR UNA PREGUNTA
class IngresarPreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta#se basa en el modelo Pregunta para poder crearlo
        fields = ["texto_pregunta",]#campo que va a tener cada una de las instancias "Pregunta"
        
        
    #LA COMENTO PQ NO CUMPLE NINGUNA FUNCIÓN.    
    # def clean_texto_pregunta(self):
    #     texto_pregunta = self.cleaned_data.get('texto_pregunta')
    #     return texto_pregunta
    
#FORMULARIO PARA PUNTUAR PREGUNTAS
class PuntarPreguntasForm(forms.ModelForm):
    class Meta:
        model = Puntuación #se basa en el modelo Puntuación para poder crearlo
        fields = ["pregunta","puntuacion"]#campo que va a tener cada una de las instancias "Puntuación"

#FORMULARIO PARA SUBIR IMÁGAGENS ((NO ANDA))
class ImagenForm(forms.ModelForm):
    class Meta:
        model = ImagenUsuario#se basa en el modelo ImagenUsuario para poder crearlo
        fields = ['imagen', 'descripcion'] #campo que va a tener cada una de las instancias "ImagenUsuario"