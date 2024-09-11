from django.contrib import admin
from django.urls import path
from tasks import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    
    #Registro
    path('', views.login_view),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.exit, name='logout'),
    
    #Barra de abajo, diferentes pestañas
    path('registration/home/', views.home_view, name="home"),
    path('story/', views.story, name="story"),
    path('settings/', views.settings, name="settings"),
    path('game/', views.game, name='game'),
    
    #Postas
    path('posta1/', views.posta1, name="posta1"),
    path('posta2/', views.posta2, name="posta2"),
    path('posta3/', views.posta3, name="posta3"),
    path('posta4/', views.posta4, name="posta4"),
    
    
    
    
    #SUPERUSER
    #usuarios
    path('info_usuarios/', views.info_usuarios, name="info_usuarios"),
    

     #preguntas
     path('ingresar_pregunta/', views.ingresar_pregunta, name='ingresar_pregunta'),
     path('puntuar_pregunta/', views.puntuar_pregunta, name='puntuar_preguntas'),
     path('lista_preguntas/', views.lista_preguntas, name='lista_preguntas'),
     path('lista_preguntas/modificar/<int:pk>/', views.modificar_pregunta, name='modificar_pregunta'),
     path('lista_preguntas/eliminar/<int:pk>/', views.eliminar_pregunta, name='eliminar_pregunta'),

     #escuelas
    path('ingresar_escuela/', views.ingresar_escuela, name = "ingresar_escuela"),
    path('lista_escuelas/', views.lista_escuelas, name='lista_escuelas'),
    path('eliminar_escuela/<int:pk>/', views.eliminar_escuela, name='eliminar_escuela'),

     #resultados preguntas
    path('estadisticas_resultados/', views.estadisticas_resultados, name='estadisticas_resultados'),

    
    # reset password urls
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="registration/reset_password.html"), 
         name="reset_password"),

    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="registration/reset_password_done.html"), 
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/reset_password_confirm.html"), 
         name="password_reset_confirm"),

    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/reset_password_complete.html"), 
         name="password_reset_complete"),
]
