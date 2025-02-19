from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Escuela, ImagenUsuario, Pregunta, Usuario, Puntuación

admin.site.register(Usuario)
admin.site.register(Pregunta)
admin.site.register(Puntuación)
admin.site.register(ImagenUsuario)
admin.site.register(Escuela)

