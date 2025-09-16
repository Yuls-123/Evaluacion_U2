from django.forms import ModelForm
from .models import pelicula

class PeliculaForm(ModelForm):
    class Meta:
        model = pelicula
        fields = ['Titulo', 'Genero', 'sinopsis']