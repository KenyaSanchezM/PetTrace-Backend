from django.db import models
from .shelter_user import ShelterUser

class EventAdvertisement(models.Model):
    refUser = models.ForeignKey(ShelterUser, on_delete=models.CASCADE, related_name='events')
    lugar_evento = models.CharField(max_length=255)
    motivo_evento = models.CharField(max_length=255)
    anfitrion_evento = models.CharField(max_length=255)
    fecha_evento = models.DateField()
    hora_evento = models.TimeField()

    def __str__(self):
        return f'{self.motivo_evento} - {self.fecha_evento}'
