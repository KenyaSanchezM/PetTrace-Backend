from django.db import models
from api.models import User
from .shelter_user import ShelterUser
from django.conf import settings

class DogPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shelter_user = models.ForeignKey(ShelterUser, on_delete=models.CASCADE, related_name='dog_predictions', null=True, blank=True)
    breeds = models.CharField(max_length=255)
    image = models.ImageField(upload_to='dog_images/', default='temp_image.jpg' )
    estatus = models.CharField(max_length=50, default='Pendiente')
    ubicacion = models.CharField(max_length=255, blank=True)
    tieneCollar = models.CharField(max_length=255, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    edad = models.IntegerField()
    color = models.CharField(max_length=255, blank=True)
    caracteristicas = models.TextField(blank=True)
    fecha = models.DateField(blank=True)
    form_type = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nombre


