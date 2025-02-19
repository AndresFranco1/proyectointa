
from django.shortcuts import render,redirect, get_object_or_404
from .models import Usuario,Escuela,Pregunta,Puntuación, ImagenUsuario
from .forms import UsuarioForm,IngresarForm, IngresarEscuelaForm, IngresarPreguntaForm, PuntarPreguntasForm, ImagenForm
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from django.http import HttpResponse

#login_required es un decorador que solo deja que la función corra si el usuario está validado, si no lo está lo retorna a login_url, en este caso login
@login_required #(login_url='/login/')
def game(request):
    return render(request, 'game.html')#renderiza la pantalla game y la retorna como respuesta al usuario

@login_required(login_url='/login/')#login_required es un decorador que solo deja que la función corra si el usuario está validado, si no lo está lo retorna a login_url, en este caso login
def exit(request):
    logout(request)#desloguea al usuario
    return redirect('login.html')#renderiza la pantalla login y la retorna como respuesta al usuario

@login_required(login_url='/login/')
def story(request):
    return render(request, 'story.html')#renderiza la pantalla story y la retorna como respuesta al usuario

@login_required(login_url='/login/')
def settings(request):
    return render(request, 'settings.html')#renderiza la pantalla settings y la retorna como respuesta al usuario

@login_required(login_url='/login/')#login_required es un decorador que solo deja que la función corra si el usuario está validado, si no lo está lo retorna a login_url, en este caso login
def posta1(request):
    return render(request, 'posta1.html')#renderiza la pantalla posta1 y la retorna como respuesta al usuario

@login_required(login_url='/login/')
def posta2(request):
    return render(request, 'posta2.html')#renderiza la pantalla posta2 y la retorna como respuesta al usuario

@login_required(login_url='/login/')
def posta3(request):
    return render(request, 'posta3.html')#renderiza la pantalla posta3 y la retorna como respuesta al usuario

@login_required(login_url='/login/')#login_required es un decorador que solo deja que la función corra si el usuario está validado, si no lo está lo retorna a login_url, en este caso login
def posta4(request):
    return render(request, 'posta4.html')#renderiza la pantalla posta4 y la retorna como respuesta al usuario
  
#HOME
def home_view(request):
    return render(request, "registration/home.html") #renderiza la pantalla home y la retorna como respuesta al usuario

#REGISTRAR, INGRESAR Y SALIR
def signup(request):
    escuelas = Escuela.objects.all()#probando si poniendolo acá funciona igual. deberíá de hacerlo
    if request.method == 'POST':#si el método es POST, que significa que usuario está enviando datos, entra al if 
        form = UsuarioForm(request.POST)# crea una instancia de "UsuarioForm" con los datos enviados por el usuario 
        if form.is_valid() : #verifica si el formulario es válido
            user = form.save(commit=False)#lo crea pero aún no lo guarda, esto es para poder validar/modifcar datos antes de guardarlos en la base de datos
            user = Usuario.objects.create_user(#crea un objeto usuario basándose en el modelo Usuario
                first_name = form.cleaned_data['first_name'], #asigna el nombre del usuario
                last_name = form.cleaned_data['last_name'], #asigna el apellido del usuario
                school = form.cleaned_data['school'], #asocia al usuario con una escuela determinada
                username = form.cleaned_data['username'], #asigna el nombre del usuario
                password = form.cleaned_data["password"], #asigna la contraseña del usuario
            )
            # user.set_password(form.cleaned_data["password"])
            # user.set_password(form.cleaned_data["password2"])
            
            login(request, user) #inicia sessión de manera automática una vez que se registró 
            user.save()#guarda el usuario en la base de datos una vez ya validados los datos

            return  redirect('home')#redirecciona la página al home
        else:
            # escuelas = Escuela.objects.all() #obtiene todos las instancias de Escuela creadas para después mostrarlas
            context = {
            "form" : form,
            "escuelas" : escuelas,
            # "error" : "Las contraseñas no coinciden"
        }
            return render(request, 'registration/signup.html', context)#renderiza la pantalla signup junto con los errores, el formulario y la lista de Escuelas
    else:# significa que el método no es POST, sino que GET, indica que el usuario accede a la página
        form = UsuarioForm #crea un formulario vacío para crear un usuario
        # escuelas = Escuela.objects.all()#obtiene todos las instancias de Escuela creadas para después mostrarlas
        context = {
            "form" : form,
            "escuelas" : escuelas

        }
        return render(request, 'registration/signup.html', context) #renderiza la pantalla signup junto con el formulario y la lista de Escuelas
    
def login_view(request):
    if request.method == "POST":#si el método es POST, que significa que usuario está enviando datos, entra al if 
        form = IngresarForm(request.POST) # crea una instancia de "IngresarForm" con los datos enviados por el usuario
        # context = {
        #     "form":form,
        # }
        if form.is_valid() : #verifica si el formulario es válido
            username = form.cleaned_data['username'] #obtiene el valor del campo "username" del formulario enviado y lo asigna a username
            password = form.cleaned_data['password']#obtiene el valor del campo "password" del formulario enviado y lo asigna a password
            user = authenticate(username= username, password = password) #authenticate valida si el username y la password existen en la base, si es true devuelve el objeto user, sino un none
            if user:#valida si existe
                login(request, user)#logea al usuario
                return redirect("home") #redirecciona a la pantall home
            else:# ingresa si user= None
                context = {
                    "error" : "Contraseña o usuario incorrecto",
                    "form" : form }
                return render(request, "registration/login.html",context) # renderiza la página login con el error y con el formulario para poder llenarlo.
        else:
            context={
                "form":form,
                "error":"Formulario inválido"
            }
            return render(request,"registration/login.html",context)
    else:# significa que el método no es POST, sino que GET, indica que el usuario accede a la página
        form = IngresarForm() #crea un formulario vacío para crear que el usuario pueda logearse
        context = {
            "form":form
        }

        return render(request,"registration/login.html",context) #renderiza la pantalla login junto con el formulario 

def exit(request):
    logout(request) #desloguea automáticamente al usuario logeado
    return redirect ("login")

#ESCUELAS
@login_required(login_url='/login/')#login_required es un decorador que solo deja que la función corra si el usuario está validado, si no lo está lo retorna a login_url, en este caso login
def ingresar_escuela(request):
    if request.method == "POST": #si el método es POST, que significa que usuario está enviando datos, entra al if 
        form = IngresarEscuelaForm(request.POST) # crea una instancia de "IngresarEscuelaForm" con los datos enviados por el usuario
        try:#intenta guardar el formulario
            form.save()#lo guarda en la base datos
            return redirect('lista_escuelas') # redirecciona a la vista lista_escuelas
        except :
            context = {
                    "form": form,
            }
            return render(request, "ingresar_escuela.html", context) 
    else:# significa que el método no es POST, sino que GET, indica que el usuario accede a la página
        form = IngresarEscuelaForm() #crea un formulario vacío para crear que el usuario pueda ingresar una escuela
        context = {
            "form" : form,
        }
        return render(request, "ingresar_escuela.html",context)

@login_required
def lista_escuelas(request):
    escuelas = Escuela.objects.all() #obtiene una lista con todos las instancias de la clase Escuela
    context = {
        'escuelas': escuelas
        }

    return render(request, 'lista_escuelas.html', context)#renderiza la vista lista_escuelas junto con la lista de instancias

@login_required
def eliminar_escuela(request, pk):
    if request.method == 'POST':
        escuela = get_object_or_404(Escuela,pk=pk)#busca el objeto Escuela a partir de la primary key, si no la encuentra devuelve un error 404
        escuela.delete()#elimina la escuela de la base de datos con ese determinado pk
        return redirect("lista_escuelas")#redirecciona a la vista lista_esceulas
    else:
        return redirect("lista_escuelas")
    
#INFORMACION DE USUARIOS 
@login_required
def info_usuarios(request):
    usuarios = Usuario.objects.all() #Obtiene una lista de todas las instancias de la clase Usuario
    escuelas = Escuela.objects.all()#Obtiene una lista de todas las instancias de la clase Escuela
    
    
    escuela_filtrada= request.GET.get('escuela',None) # filtra por escuela seleccionada si es que se requiere
    first_name_filtrado= request.GET.get('first_name',None) # filtra por nombre ingresado si es que se requiere
    last_name_filtrado= request.GET.get('last_name',None) # filtra por apellido ingresado si es que se requiere
    username_filtrado = request.GET.get("username",None) # filtra por el nombre de usuario ingresado si es que se requiere
    
    if escuela_filtrada: #si en la variable "escuela_filtrada" hay algun valor a partir de lo que tomó el método GET, entra y filtra
        usuarios = usuarios.filter(school__nombre_escuela=escuela_filtrada)#filtra los usuarios que tengan el parámetro nombre_escuela igual a escuela_filtrada
        
    if first_name_filtrado: #si en la variable "first_name_filtrado" hay algun valor a partir de lo que tomó el método GET, entra y filtra
        usuarios = usuarios.filter(first_name__icontains=first_name_filtrado)#filtra los usuarios que contengan concidencials parciales ( sin importar mayus o minus) con first_name_filtrado
        
    if last_name_filtrado: #si en la variable "last_name_filtrado" hay algun valor a partir de lo que tomó el método GET, entra y filtra
        usuarios = usuarios.filter(last_name__icontains=last_name_filtrado)#filtra los usuarios que tengan el parámetro last_name similar a last_name_filtrado
        
    if username_filtrado: #si en la variable "username_filtrado" hay algun valor a partir de lo que tomó el método GET, entra y filtra
        usuarios = usuarios.filter(username__icontains=username_filtrado)#filtra los usuarios que tengan el parámetro username similar a username_filtrado
    
     # Contar el número total de usuarios
    total_usuarios = Usuario.objects.count()#cuenta la cantidad de instancias de la clase Usuarios en total
    
    context = {
        "usuarios" : usuarios, #lista de usuarios luego de pasar por todos los filtros
        "escuelas" : escuelas, #lista de las escuelas 
        "total_usuarios": total_usuarios #cantidad de usuarios en total
    }
    return render(request, 'info_usuarios.html', context)

#INGERESAR PREGUNTAS
@login_required(login_url='/login/')#login_required es un decorador que solo deja que la función corra si el usuario está validado, si no lo está lo retorna a login_url, en este caso login
def ingresar_pregunta(request):
    if request.method == "POST": #si el método es POST, que significa que usuario está enviando datos, entra al if 
        form = IngresarPreguntaForm(request.POST)  # crea una instancia de "IngresarEscuelaForm" con los datos enviados por el usuario
        try:#intenta guardar el form
            form.save()
            return redirect("lista_preguntas")
        except: #si no puede corre el except con el error
            context = {
                "form" : form,
            }
            return render( request,"ingresar_preguntas.html", context)#renderiza la pantalla ingresar_pregunta junto con el formulario para ingresar la pregunta correctamente
    else:# significa que el método no es POST, sino que GET, indica que el usuario accede a la página
        form = IngresarPreguntaForm() #crea un formulario vacío para que se pueda llenar
        context = {
            "form" : form
        }
        return render(request ,"ingresar_preguntas.html",context)#renderiza la pantalla ingresar_pregunta junto con el formulario para ingresar la pregunta

@login_required
def lista_preguntas(request):
    preguntas = Pregunta.objects.all()# obtiene una lista con todas las instancias de la clase Pregunta
    context = {
        "preguntas": preguntas
    }
    return render(request, "lista_preguntas.html", context)#renderiza la pantalla lista_preguntas junto con la el contexto que contiene la lista de instancias

@login_required
def modificar_pregunta(request,pk):
    pregunta = get_object_or_404(Pregunta, pk=pk)
    if request.method == "POST":
        form = IngresarPreguntaForm(request.POST, instance= pregunta)
        if form.is_valid():
            try:
                form.save()
                return redirect("lista_preguntas")
            except:
                
                error = "La pregunta solo debe contener letras, números, espacios y los símbolos ¿?¡!."
                context = {
                    "form" : form,
                    "error" : error
                }
                return render( request, "lista_preguntas.html", context)
    else:
        form = IngresarPreguntaForm(instance= pregunta)
        context = {
        "form" : form
            }
        return render(request , "ingresar_pregunta.html",context)

@login_required(login_url='/login/')#login_required es un decorador que solo deja que la función corra si el usuario está validado, si no lo está lo retorna a login_url, en este caso login
def eliminar_pregunta(request,pk):

    if request.method == "POST":
        pregunta = get_object_or_404(Pregunta, pk=pk)#busca el objeto Pregunta a partir de la primary key, si no la encuentra devuelve un error 404
        pregunta.delete()#elimina la pregunta de la base de datos con ese determinado pk
        return redirect ("lista_preguntas")
    else:
        return redirect("lista_preguntas")
        
#PUNTUAR PREGUNTAS
@login_required(login_url='/login/')#login_required es un decorador que solo deja que la función corra si el usuario está validado, si no lo está lo retorna a login_url, en este caso login
def puntuar_pregunta(request):
    preguntas = Pregunta.objects.all() #obtiene una lista con todos las instancias de la clase Pregunta
    puntuacion_registrada = False# flags para dsp validar si se subió al menos una
    imagen_registrada = False

    if request.method == 'POST':#si el método es POST, que significa que usuario está enviando datos, entra al if 
            #puntuaciones
            for pregunta in preguntas:
                estrellas = request.POST.get(f"estrellas_{pregunta.id}")#recupera desde el formulario enviado la puntuación de la pregunta actual
                if estrellas:#verifica si la puntuación es válida
                    Puntuación.objects.create(#crea un objeto Puntuación
                        pregunta = pregunta,
                        puntuacion = estrellas
                    )#asocia la pregunta de la iteración con la puntuación
                    puntuacion_registrada = True

                
            #imagenes
            form = ImagenForm(request.POST, request.FILES)#crea una isntancia de imagenform con post para txt y files par imgs
            if form.is_valid() and request.FILES.get('imagen'):#verifica si el form es válido y de si existe una imagen, sirve para no guardar forms vacios
                form.save()#guarda el form
                imagen_registrada = True


            if puntuacion_registrada or imagen_registrada: #si al menos un form se respondió, lo envía
                return redirect("home")
            else:
                context = {
                "error" : "Al menos un campo debe estar completado para que la respuesta sea válida",
                "preguntas" : preguntas,
                "form" : form,
                "imagen_form": ImagenForm
                }
                return render(request, "puntuar_preguntas.html", context )
            
    else:# significa que el método no es POST, sino que GET, indica que el usuario accede a la página
        preguntas = Pregunta.objects.all() #obtiene una lista con todos las instancias de la clase Pregunta
        form = PuntarPreguntasForm() # crea una instancia de puntuarpreguntaform
        imagen_form = ImagenForm() # crea una instancia de imagenform
        context = {
            "preguntas" : preguntas,
            "form" : form,
            "imagen_form": imagen_form
        }
        return render(request, "puntuar_preguntas.html", context )



#IMAGENES

def ver_imagenes(request):
    imagenes = ImagenUsuario.objects.all().order_by('-fecha_subida')#obtiene una lista con todos las instancias de la clase ImagenUsuario
    context = {
               'imagenes': imagenes,
               }
    return render(request, 'ver_imagenes.html', context)#renderiza la vista ver_imagenes junto con la lista de instancias de imágenes

def eliminar_imagen(request, imagen_id):
    imagen = get_object_or_404(ImagenUsuario, id=imagen_id)#busca el objeto ImagenUsuario a partir de la primary key, si no la encuentra devuelve un error 404

    if request.method == 'POST':#verifica si el método es POST, para mas seguridad
        imagen.delete()#elimina la pregunta de la base de datos con ese imagen_id
        # return redirect('ver_imagenes')
    return redirect('ver_imagenes')#redirecciona a la vista ver_imagenes


#ESTADÍSTICAS   
@login_required(login_url='/login/')#login_required es un decorador que solo deja que la función corra si el usuario está validado, si no lo está lo retorna a login_url, en este caso login
def estadisticas_resultados(request):
    
    preguntas = Pregunta.objects.all()#obtiene una lista de todas las instancias de la clase Pregunta creadas
    resultados = []
    for pregunta in preguntas:
        conteo_estrellas = Puntuación.objects.filter(pregunta=pregunta).values('puntuacion').annotate(conteo=Count('puntuacion')).order_by('puntuacion')
        #1: filtra las preguntas del modelo puntuacion para que se relacione cada instancia pregunta con la asociada a su puntuacion
        #2: Una vez filtrada la pregunta, tiene varias respeustas con diferentes valores de estrellas(1 estrella, 2 estrellas), lo q hace esto es agrupar las respuestas de 1 estrella de esa spregunta todas juntas, las respuestas de 2 estrellas todas juntas..., pero de la misma pregunta
        #3: cuenta cuanta cantidad de respuestas a esa misma pregunta hay de 1 estrella, de 2 estrellas, de 3 estrellas...
        #4: oredna segun la cantidad de estrellas de manera descendente
        
        total_respuestas = sum(item['conteo'] for item in conteo_estrellas)#Total de respuestas para cada pregunta, itera el diccionario conteo_estrellas de cada pregunta, cada pregunta tiene 5 clave:valor, 1estrella:xconteo, 2estrellas:xconteo. De cada item(diccionario) accede al valor conteo 
        resultado_pregunta = {
            'pregunta': pregunta,#la pregunta actual
            'total_respuestas': total_respuestas,#la cantidad de respuestas a esa pregunta
            'conteos': {item['puntuacion']: item['conteo'] for item in conteo_estrellas},#esto crea un diccionario a partir de conteo_estrellas, diccionarios dentro de otro mas grande, el que se crea clave:estrellas(1 estrella, 2 estrellas) valor: cuántas veces esa estrella fué elegida(1,2,3veces). 
            'porcentajes': {}#se calcula mas abajo
        }
        #CALCULANDO PORCENTAJES
        for estrellas, conteo in resultado_pregunta['conteos'].items():#itera sobre el diccionario de conteos( )
            if total_respuestas > 0:#si hay alguna respuesta calcula
                resultado_pregunta['porcentajes'][estrellas] = round((conteo / total_respuestas) * 100)#calcula el porcentaje para cada valor de estrella elegido, 1estrella,2estrellas
            else:
                resultado_pregunta['porcentajes'][estrellas] = 0.0

        for i in range(len(preguntas)):
            if i not in resultado_pregunta['conteos']:
                resultado_pregunta['conteos'][i] = 0
                resultado_pregunta['porcentajes'][i] = 0.0
    
        resultados.append(resultado_pregunta)
    context = {
        "resultados" : resultados
    }
    return render(request, 'estadisticas_resultados.html',context)