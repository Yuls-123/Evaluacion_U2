from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class pelicula(models.Model):
    Titulo = models.CharField(max_length=100)
    Genero = models.CharField(max_length=100)
    Idioma = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_now_add=True)
    sinopsis = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + " - por " + self.usuario.username