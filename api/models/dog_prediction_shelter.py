from django.db import models
from .shelter_user import ShelterUser
from django.conf import settings

class DogPredictionShelter(models.Model):
    shelter_user = models.ForeignKey(ShelterUser, on_delete=models.CASCADE, null=True, blank=True)
    breeds = models.CharField(max_length=255)
    image = models.ImageField(upload_to='dog_images/', default='temp_image.jpg' )
    nombre = models.CharField(max_length=255, blank=True)
    edad = models.IntegerField()
    color = models.CharField(max_length=255, blank=True)
    caracteristicas = models.TextField(blank=True)
    sexo = models.CharField(max_length=50, blank=True)
    tamanio = models.CharField(max_length=50, blank=True)
    temperamento = models.CharField(max_length=100, blank=True)
    vacunas = models.CharField(max_length=255, blank=True)
    esterilizado = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.nombre

