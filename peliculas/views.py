from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import PeliculaForm
from .models import pelicula
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect("lista_peliculas")
            except IntegrityError:
                return render(request, 'signup.html', {
                    "form": UserCreationForm(),
                    "error": "El usuario ya existe"
                })
        else:
            return render(request, 'signup.html', {
                "form": UserCreationForm(),
                "error": "Las contraseñas no coinciden"
            })


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"]
        )
        if user is None:
            return render(request, "signin.html", {
                "form": AuthenticationForm(),
                "error": "Usuario o contraseña incorrecta"
            })
        else:
            login(request, user)
            return redirect("lista_peliculas")

def signout(request):
    logout(request)
    return redirect("home")

def lista_peliculas(request):
    if not request.user.is_authenticated:
        return redirect("signin")
    
    peliculas = pelicula.objects.filter(usuario=request.user)
    return render(request, "lista_peliculas.html", {"peliculas": peliculas})

def agregar_pelicula(request):
    if not request.user.is_authenticated:
        return redirect("signin")
    
    if request.method == "GET":
        return render(request, "agregar_pelicula.html", {"form": PeliculaForm})
    else:
        try:
            form = PeliculaForm(request.POST)
            nueva_pelicula = form.save(commit=False)
            nueva_pelicula.usuario = request.user
            nueva_pelicula.save()
            return redirect("lista_peliculas")
        except ValueError:
            return render(request, 'agregar_pelicula.html', {
                'form': PeliculaForm(),
                'error': 'Por favor ingresa datos válidos'
            })

def pelicula_detail(request, pelicula_id):
    if not request.user.is_authenticated:
        return redirect("signin")
    
    if request.method == "GET":
        pelicula = get_object_or_404(pelicula, pk=pelicula_id, usuario=request.user)
        form = PeliculaForm(instance=pelicula)
        return render(request, "pelicula_detail.html", {"pelicula": pelicula, "form": form})
    else:
        try:
            pelicula = get_object_or_404(pelicula, pk=pelicula_id, usuario=request.user)
            form = PeliculaForm(request.POST, instance=pelicula)
            form.save()
            return redirect("lista_peliculas")
        except ValueError:
            return render(request, "pelicula_detail.html", {
                "pelicula": pelicula, 
                "form": form,
                "error": "Error al actualizar película"
            })

def eliminar_pelicula(request, pelicula_id):
    if not request.user.is_authenticated:
        return redirect("signin")
    
    pelicula = get_object_or_404(pelicula, pk=pelicula_id, usuario=request.user)
    if request.method == "POST":
        pelicula.delete()
        return redirect("lista_peliculas")