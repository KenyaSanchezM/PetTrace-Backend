from django.db import models
from .shelter_user import ShelterUser


class EventAdvertisement(models.Model):
    refUser = models.ForeignKey(ShelterUser, on_delete=models.CASCADE, related_name='events')
    nombre_evento = models.CharField(max_length=255)
    descripcion_evento = models.CharField(max_length=255)
    lugar_evento = models.CharField(max_length=255)
    motivo = models.CharField(max_length=255, blank=True)
    anfitrion_evento = models.CharField(max_length=255, blank=True)
    fecha_evento = models.DateField()
    hora_evento = models.TimeField()
    imagen_evento = models.ImageField(upload_to='event_images/', null=True, blank=True )

    def __str__(self):
        return f'{self.motivo} - {self.fecha_evento}'
