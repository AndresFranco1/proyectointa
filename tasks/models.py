
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import re
from django.core.exceptions import ValidationError



def validando_nombre_escuela (nombre_escuela):
    if not re.match(r'^[\w\s]+$', nombre_escuela): 
        # re.match busca ese patrón en el la cadena, si no lo encuentra signfica que la cadena es válida, entra al if
        # ^ indica el incicio de la cadena, el $ indica el final. el + indica "al menos 1 vez"
        raise ValidationError('El nombre de la escuela solo puede contener letras, números y espacios.')

def validando_direccion_escuela(direccion_escuela):
    # Solo letras y números
    if not re.match(r'^[\w\s]+$', direccion_escuela):
         #re.match busca ese patrón en el la cadena, si la cadena tiene valores que no están dentro de los parámetros (true) lanza el error
        raise ValidationError('La dirección solo puede contener letras y números.')
    
def validando_localidad_escuela(localidad_escuela):
    if not re.match(r'^[a-zA-Z\s]+$', localidad_escuela):
         #re.match busca ese patrón en el la cadena, si la cadena tiene valores que no están dentro de los parámetros (true) lanza el error
        raise ValidationError('La localidad solo puede contener letras.')

def validando_texto_pregunta(texto_pregunta):
    if not re.match("^[A-Za-z0-9 ¿?¡!]+$", texto_pregunta):
        #re.match busca ese patrón en el la cadena, si la cadena tiene valores que no están dentro de los parámetros (true) lanza el error
        raise ValidationError("La pregunta solo debe contener letras, números, espacios y los símbolos ¿?¡!.")
    
class Escuela(models.Model):
    nombre_escuela = models.CharField(max_length = 100, unique= True, validators=[validando_nombre_escuela])#tipo de dato char, de 100 caracteres max, debe ser único. Se valida con la función validando_nombre_escuela
    direccion_escuela = models.CharField(max_length= 100, validators = [validando_direccion_escuela])
    numero_escuela = models.IntegerField()
    localidad_escuela = models.CharField(max_length=100, validators= [validando_localidad_escuela])
    
    def clean(self):
        # Convertir la primera letra de cada palabra a mayúscula
        self.nombre_escuela = self.nombre_escuela.title()
        self.direccion_escuela = self.direccion_escuela.title()
        self.localidad_escuela = self.localidad_escuela.title()
        
    def __str__(self):#devuelve un texto que describe la instancia de la clase (objeto) de manera lejible y comprensible
        return (f"Nombre:{self.nombre_escuela} | Número: {self.numero_escuela} | Dirección:{self.direccion_escuela} | Localidad: {self.localidad_escuela}")
     
class UsuarioManager(BaseUserManager): #se utuliza porque estamos usando un modelo de usuario personalizado, no el de django. Es el encargado de manejar los diferentes tipo de usuarios que pueden exsitir
   
    # def create_user(self,username,first_name,last_name, password=None,school= None, **extra_fields):
    def create_user(self,username,first_name,last_name, password,school= None, **extra_fields):
        if not username:# si falta el parámetro username lanza el error
            raise ValueError("El username es requerido")
        
        # school, created = Escuela.objects.get_or_create(nombre_escuela=school)
        
        user = self.model(#se utiliza self.model para crear una instancia con la clase que el UsuarioManager es administrador (en este caso es la clase Usuario). Viene a ser como "usá este modelo para crear una nueva instancia"
            first_name = first_name,#el first_name del parámetro recibido va a ser el first_name de la nueva instancia que se cree
            last_name = last_name,
            school = school,
            username= username,
            **extra_fields#posibles valores adicionales que pueden necesitarse
        )
        user.set_password(password)  # Establece la contraseña usando set_password para que sea encriptada, sino seríá texto plano
        user.save(using = self._db)#se guarda el usuario en la base, self._db asegura que se use la base de datos correcta
        return user
    
    def create_superuser(self, username, first_name, last_name,school, password=None, **extra_fields):
        #crea un usuario con campos específicos
        extra_fields.setdefault('is_staff', True)#extra_fields setea parametros extra
        extra_fields.setdefault('is_superuser', True)
        
        # Asigna automáticamente la escuela "Inta" si es superusuario
        school = Escuela.objects.get(nombre_escuela="Inta")
        return self.create_user(username, first_name,last_name, password, school, **extra_fields)#vuelve a llamar el método de arriba, pero con parametros diferentes
                
    
class Usuario(AbstractBaseUser,PermissionsMixin):

    first_name= models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    school = models.ForeignKey(Escuela, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50) #Usar siempre set_password() para encriptar antes de guardar
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UsuarioManager()#se establece que el UsuarioManager va a ser administrador del modelo Usuario
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','last_name',"school","password"]#campos requeridos para poder crear una instancia, además de USERNAME_FIELD
    
    def __str__(self):#devuelve un texto que describe la instancia de la clase (objeto) de manera lejible y comprensible
        return f"Usuario: {self.username} | Nombre : {self.first_name} | Apellido: {self.last_name} | Escuela: {self.school.nombre_escuela}"
    

class Pregunta(models.Model):
    texto_pregunta = models.CharField(max_length=260, validators=[validando_texto_pregunta])
    
    def __str__(self):#devuelve un texto que describe la instancia de la clase (objeto) de manera lejible y comprensible
        return self.texto_pregunta  
    
class Puntuación(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(choices=[(i,i) for i in range (1,6)])
    fecha = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):#devuelve un texto que describe la instancia de la clase (objeto) de manera lejible y comprensible
        return f"{self.pregunta} -- {self.puntuacion} estrellas"
    
    
class ImagenUsuario(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')
    descripcion = models.CharField(max_length=255, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):#devuelve un texto que describe la instancia de la clase (objeto) de manera lejible y comprensible
            return f"Fecha: {self.fecha_subida} | Descripción : {self.descripcion}"
