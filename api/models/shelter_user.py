from django.db import models

def validate_postal_code(value):
    if len(value) != 5 or not value.isdigit():
        raise ValidationError('El código postal debe tener exactamente 5 dígitos y solo números.')

class ShelterUser(models.Model):
    nombre = models.CharField(max_length=10,blank=False)
    email = models.EmailField(unique=True)
    password_R = models.CharField(max_length=128)
    telefono = models.CharField(max_length=15, default='Default')
    estado = models.CharField(max_length=128 , default='Default state')
    ciudad = models.CharField(max_length=128, default='Default City')
    direccion = models.CharField(max_length=128, default='Default direccion')
    codigoPostal = models.CharField(max_length=5, validators=[validate_postal_code])

    def __str__(self):
        return self.nombre
