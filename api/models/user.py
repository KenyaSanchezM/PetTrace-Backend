from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, email, nombre, telefono, password=None, user_type='user'):
        if not email:
            raise ValueError("El email debe ser proporcionado")
        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            telefono=telefono,
            user_type=user_type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, telefono, password=None):
        user = self.create_user(
            email,
            nombre=nombre,
            telefono=telefono,
            password=password,
            user_type='admin'
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    user_type = models.CharField(max_length=20, default='user')
    profile_image = models.ImageField(upload_to='users_images/', blank=True, null=True)
    marked_dogs = models.ManyToManyField('DogPrediction', related_name='marked_by_users', blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'telefono']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
