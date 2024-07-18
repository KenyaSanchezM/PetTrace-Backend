from django.db import models

class ShelterUser(models.Model):
    nombre = models.CharField(max_length=100)
    telefono_shelter = models.CharField(max_length=15)
    ubicacion = models.CharField(max_length=255)
    correo_electronico = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)
    publicaciones = models.ManyToManyField('api.DogPrediction', blank=True, related_name='shelter_publicaciones')
    image = models.ImageField(upload_to='shelters/')

    def __str__(self):
        return self.nombre
