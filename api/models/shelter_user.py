from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.core.exceptions import ValidationError

def validate_postal_code(value):
    if len(value) != 5 or not value.isdigit():
        raise ValidationError('El código postal debe tener exactamente 5 dígitos y solo números.')

class ShelterUser(AbstractBaseUser):
    nombre = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    telefono = models.CharField(max_length=15, default='Default')
    estado = models.CharField(max_length=128, default='Default state')
    ciudad = models.CharField(max_length=128, default='Default City')
    direccion = models.CharField(max_length=128, default='Default direccion')
    codigoPostal = models.CharField(max_length=5, validators=[validate_postal_code])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.nombre
