from django.db import models

class User(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    correo_electronico = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)
    telefono_user = models.CharField(max_length=255)
    publicaciones = models.ManyToManyField('api.DogPrediction', related_name='propietario', blank=True)
    # Otros campos según sea necesario

    def __str__(self):
        return self.nombre
