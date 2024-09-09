
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import re
from django.core.exceptions import ValidationError



def validando_nombre_escuela (nombre_escuela):
    if not re.match(r'^[\w\s]+$', nombre_escuela):
        raise ValidationError('El nombre de la escuela solo puede contener letras, números y espacios.')

def validando_direccion_escuela(direccion_escuela):
    # Solo letras y números
    if not re.match(r'^[\w\s]+$', direccion_escuela):
        raise ValidationError('La dirección solo puede contener letras y números.')
    
def validando_localidad_escuela(localidad_escuela):
    # Solo letras
    if not re.match(r'^[a-zA-Z\s]+$', localidad_escuela):
        raise ValidationError('La localidad solo puede contener letras.')


class Escuela(models.Model):
    nombre_escuela = models.CharField(max_length = 100, unique= True, validators=[validando_nombre_escuela])
    direccion_escuela = models.CharField(max_length= 100, validators = [validando_direccion_escuela])
    numero_escuela = models.IntegerField()
    localidad_escuela = models.CharField(max_length=100, validators= [validando_localidad_escuela])
    
    def clean(self):
        # Convertir la primera letra de cada palabra a mayúscula
        self.nombre_escuela = self.nombre_escuela.title()
        self.direccion_escuela = self.direccion_escuela.title()
        self.localidad_escuela = self.localidad_escuela.title()
        
    def __str__(self):
        return (self.nombre_escuela, self.numero_escuela,self.direccion_escuela,self.numero_escuela,self.localidad_escuela)
     
class UsuarioManager(BaseUserManager):
    def create_user(self,username,first_name,last_name, password=None,school= None, **extra_fields):
        if not username:
            raise ValueError("El username es requerido")
        
        # school, created = Escuela.objects.get_or_create(nombre_escuela=school)
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            school = school,
            username= username,
            **extra_fields
        )
        user.set_password(password)  # Establece la contraseña usando set_password para que sea encriptada
        user.save(using = self._db)
        return user
    
    def create_superuser(self, username, first_name, last_name,school, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Asignar automáticamente la escuela INTA si es superusuario
        school = Escuela.objects.get(nombre_escuela="Inta")
        return self.create_user(username, first_name,last_name, password, school, **extra_fields)
                
    
class Usuario(AbstractBaseUser,PermissionsMixin):

    first_name= models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    school = models.ForeignKey(Escuela, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','last_name',"school","password"]
    
    def __str__(self):
        return self.username
    

class Pregunta(models.Model):
    texto_pregunta = models.CharField(max_length=260)
    
    def __str__(self):
        return self.texto_pregunta  
    
class Puntuación(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(choices=[(i,i) for i in range (1,6)])
    fecha = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"{self.pregunta} -- {self.puntuacion} estrellas"