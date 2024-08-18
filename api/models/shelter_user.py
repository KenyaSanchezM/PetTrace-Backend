from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

def validate_postal_code(value):
    if len(value) != 5 or not value.isdigit():
        raise ValidationError('El código postal debe tener exactamente 5 dígitos y solo números.')

class ShelterUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password, **extra_fields)

User = get_user_model()
class ShelterUser(AbstractBaseUser):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, default='Default')
    estado = models.CharField(max_length=128, default='Default state')
    ciudad = models.CharField(max_length=128, default='Default City')
    direccion = models.CharField(max_length=128, default='Default direccion')
    codigoPostal = models.CharField(max_length=5, validators=[validate_postal_code])
    user_type = models.CharField(max_length=20, default=('shelter'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    objects = ShelterUserManager()

    def __str__(self):
        return self.nombre
