from django.db import models

class DogPrediction(models.Model):
    breeds = models.JSONField()
    ubicacion = models.CharField(max_length=255)
    tieneCollar = models.CharField(max_length=10)
    nombre = models.CharField(max_length=255)
    edad = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    caracteristicas = models.TextField()
    fecha = models.DateField()
    form_type = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.nombre} - {self.form_type}'


class DogBreedPrediction(models.Model):
    image = models.ImageField(upload_to='dog_images/')
    breed = models.CharField(max_length=100)
    probability = models.FloatField()

    def __str__(self):
        return f"{self.breed}: {self.probability}"
