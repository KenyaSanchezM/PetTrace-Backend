from django.db import models
from .user import User
from .shelter_user import ShelterUser

class DogPrediction(models.Model):
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
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Refugio = models.ForeignKey(ShelterUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre


