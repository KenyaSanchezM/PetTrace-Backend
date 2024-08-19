from django.db import models
from .user import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager

def validate_postal_code(value):
    if len(value) != 5 or not value.isdigit():
        raise ValidationError('El código postal debe tener exactamente 5 dígitos y solo números.')

class ShelterUserManager(BaseUserManager):
    def create_user(self, email, nombre, telefono, password=None, estado=None, ciudad=None, direccion=None, codigoPostal=None):
        if not email:
            raise ValueError("El email debe ser proporcionado")
        shelter_user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            telefono=telefono,
            estado=estado,
            ciudad=ciudad,
            direccion=direccion,
            codigoPostal=codigoPostal,
            user_type='shelter'
        )
        shelter_user.set_password(password)  # Cambiado de 'user' a 'shelter_user'
        shelter_user.save(using=self._db)
        return shelter_user  # Cambiado de 'user' a 'shelter_user'

    def create_superuser(self, email, nombre, telefono, password=None):
        shelter_user = self.create_user(
            email=email,
            nombre=nombre,
            telefono=telefono,
            password=password,
            estado=None,
            ciudad=None,
            direccion=None,
            codigoPostal=None
        )
        shelter_user.is_admin = True
        shelter_user.save(using=self._db)
        return shelter_user  # Cambiado de 'user' a 'shelter_user'

class ShelterUser(User):
    estado = models.CharField(max_length=128, blank=True, null=True)
    ciudad = models.CharField(max_length=128, blank=True, null=True)
    direccion = models.CharField(max_length=128, blank=True, null=True)
    codigoPostal = models.CharField(max_length=5, blank=True, null=True, validators=[validate_postal_code])

    objects = ShelterUserManager()

    class Meta:
        verbose_name = "Shelter User"
        verbose_name_plural = "Shelter Users"
