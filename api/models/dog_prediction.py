from django.db import models
from api.models import User
from .shelter_user import ShelterUser
from django.conf import settings

class DogPrediction(models.Model):
    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Hembra', 'Hembra'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    breeds = models.CharField(max_length=255)
    image = models.ImageField(upload_to='dog_images/', default='temp_image.jpg' )
    profile_image1 = models.ImageField(upload_to='dog_images/', null=True, blank=True)  # Primera imagen para mostrar
    profile_image2 = models.ImageField(upload_to='dog_images/', null=True, blank=True)  # Segunda imagen para mostrar
    ubicacion = models.CharField(max_length=255, blank=True)
    tieneCollar = models.CharField(max_length=255, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    edad = models.IntegerField()
    color = models.CharField(max_length=255, blank=True)
    caracteristicas = models.TextField(blank=True)
    fecha = models.DateField(blank=True)
    form_type = models.CharField(max_length=255, blank=True)
    sexo = models.CharField(max_length=6, choices=SEXO_CHOICES)  


    def __str__(self):
        return self.nombre


