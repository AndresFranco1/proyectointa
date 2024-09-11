
from django.shortcuts import render,redirect, get_object_or_404
from .models import Usuario,Escuela,Pregunta,Puntuación
from .forms import UsuarioForm,IngresarForm, IngresarEscuelaForm, IngresarPreguntaForm, PuntarPreguntasForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def game(request):
    return render(request, 'game.html')

@login_required(login_url='/login/')
def exit(request):
    logout(request)
    return redirect('login.html')

@login_required(login_url='/login/')
def story(request):
    return render(request, 'story.html')

@login_required(login_url='/login/')
def settings(request):
    return render(request, 'settings.html')

@login_required(login_url='/login/')
def posta1(request):
    return render(request, 'posta1.html')

@login_required(login_url='/login/')
def posta2(request):
    return render(request, 'posta2.html')

@login_required(login_url='/login/')
def posta3(request):
    return render(request, 'posta3.html')

@login_required(login_url='/login/')
def posta4(request):
    return render(request, 'posta4.html')
  
#HOME
def home_view(request):
    return render(request, "registration/home.html")

#REGISTRAR, INGRESAR Y SALIR
def signup(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid() :
            user = form.save(commit=False)
            user = Usuario.objects.create(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                school = form.cleaned_data['school'],
                username = form.cleaned_data['username'],
            )
            user.set_password(form.cleaned_data["password"])
            user.set_password(form.cleaned_data["password2"])
            user.save()

            return  redirect('login')
        else:
            escuelas = Escuela.objects.all()
            context = {
            "form" : form,
            "escuelas" : escuelas,
            "error" : "Las contraseñas no coincides"
        }
            return render(request, 'registration/signup.html', context)
    else:
        form = UsuarioForm
        escuelas = Escuela.objects.all()
        context = {
            "form" : form,
            "escuelas" : escuelas

        }
        return render(request, 'registration/signup.html', context)
    
def login_view(request):
    if request.method == "POST":
        form = IngresarForm(request.POST)
        context = {
            "form":form,
        }
        if form.is_valid() :
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username= username, password = password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                context = {
                    "error" : "Contraseña o usuario incorrecto",
                    "form" : form }
                return render(request, "registration/login.html",context)
        else:
            context={
                "form":form,
                "error":"Formulario inválido"
            }
            return render(request,"registration/login.html",context)
    else:
        form = IngresarForm()
        context = {
            "form":form
        }

        return render(request,"registration/login.html",context)

def exit(request):
    logout(request)
    return redirect ("login")

#ESCUELAS
@login_required
def ingresar_escuela(request):
    if request.method == "POST":
        form = IngresarEscuelaForm(request.POST)
        try:
            form.save()
            return redirect('lista_escuelas')
        except :
            context = {
                    "form": form,
            }
            return render(request, "ingresar_escuela.html", context)
    else:
        form = IngresarEscuelaForm()
        context = {
            "form" : form,
        }
        return render(request, "ingresar_escuela.html",context)

@login_required
def lista_escuelas(request):
    escuelas = Escuela.objects.all()
    context = {
        'escuelas': escuelas

        }

    return render(request, 'lista_escuelas.html', context)

@login_required
def eliminar_escuela(request, pk):
    if request.method == 'POST':
        escuela = get_object_or_404(Escuela,pk=pk)
        escuela.delete()
        return redirect("lista_escuelas")
    else:
        return redirect("lista_escuelas")
    
#INFORMACION DE USUARIOS 
@login_required
def info_usuarios(request):
    usuarios = Usuario.objects.all()
    escuelas = Escuela.objects.all()
    
    
    escuela_filtrada= request.GET.get('escuela',None)
    first_name_filtrado= request.GET.get('first_name',None)
    last_name_filtrado= request.GET.get('last_name',None)
    username_filtrado = request.GET.get("username",None)
    if escuela_filtrada:
        usuarios = usuarios.filter(school__nombre_escuela=escuela_filtrada)
    if first_name_filtrado:
        usuarios = usuarios.filter(first_name__icontains=first_name_filtrado)
    if last_name_filtrado:
        usuarios = usuarios.filter(last_name__icontains=last_name_filtrado)
    if username_filtrado:
        usuarios = usuarios.filter(username__icontains=username_filtrado)
    
     # Contar el número total de usuarios
    total_usuarios = Usuario.objects.count()
    
    context = {
        "usuarios" : usuarios,
        "escuelas" : escuelas,
        "total_usuarios": total_usuarios
    }
    return render(request, 'info_usuarios.html', context)

#INGERESAR PREGUNTAS
@login_required
def ingresar_pregunta(request):
    if request.method == "POST":
        form = IngresarPreguntaForm(request.POST)
        try:
            form.save()
            return redirect("lista_preguntas")
        except: 
            context = {
                "form" : form,
            }
            return render( request,"ingresar_preguntas.html", context)
    else:
        form = IngresarPreguntaForm()
        context = {
            "form" : form
        }
        return render(request ,"ingresar_preguntas.html",context)

@login_required
def lista_preguntas(request):
    preguntas = Pregunta.objects.all()
    context = {
        "preguntas": preguntas
    }
    return render(request, "lista_preguntas.html", context)

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

@login_required
def eliminar_pregunta(request,pk):

    if request.method == "POST":
        pregunta = get_object_or_404(Pregunta, pk=pk)
        pregunta.delete()
        return redirect ("lista_preguntas")
    else:
        return redirect("lista_preguntas")
        
#PUNTUAR PREGUNTAS
@login_required
def puntuar_pregunta(request):
    preguntas = Pregunta.objects.all()
    if request.method == 'POST':
        for pregunta in preguntas:
            estrellas = request.POST.get(f"estrellas_{pregunta.id}")
            if estrellas:
                Puntuación.objects.create(
                    pregunta = pregunta,
                    puntuacion = estrellas
                )
        return redirect("home")
    else:
        preguntas = Pregunta.objects.all()
        form = PuntarPreguntasForm
        context = {
            "preguntas" : preguntas,
            "form" : form
        }
        return render(request, "puntuar_preguntas.html", context )

@login_required   
def estadisticas_resultados(request):
    
    preguntas = Pregunta.objects.all()
    resultados = []
    for pregunta in preguntas:
        conteo_estrellas = Puntuación.objects.filter(pregunta=pregunta).values('puntuacion').annotate(conteo=Count('puntuacion')).order_by('puntuacion')
        #1: filtra las preguntas del modelo puntuacion para que se relacione cada instancia pregunta con la asociada a su puntuacion
        #2: Una vez filtrada la pregunta, tiene varias respeustas con diferentes valores de estrellas, lo q hace esto es agrupar las respuesta de 1 estrella de esa spregunta todas juntas, la respuesta de 2 estrellas todas juntas...
        #3: cuenta cuanta cantidad de respuestas a esa misma pregunta, hay de 1 estrella, de 2 estrellas, de 3 estrellas
        #4: oredna segun la cantidad de esgtrellas de manera descendente
        
        total_respuestas = sum(item['conteo'] for item in conteo_estrellas)#Total de respuestas para cada pregunta, itera el diccionario conteo_estrellas de cada pregunta, cada pregunta tiene 5 clave:valor, 1estrella:xconteo, 2estrellas:xconteo. De cada item(diccionario) accede al valor conteo 
        resultado_pregunta = {
            'pregunta': pregunta,
            'total_respuestas': total_respuestas,
            'conteos': {item['puntuacion']: item['conteo'] for item in conteo_estrellas},#esto crea un diccionario a partir de conteo_estrellas, diccionarios dentro de otro mas grande, el que se crea clave:estrellas(1 estrella, 2 estrellas) valor: cuántas veces esa estrella fué elegida(1,2,3veces). 
            'porcentajes': {}
        }
        
        for estrellas, conteo in resultado_pregunta['conteos'].items():
            if total_respuestas > 0:
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