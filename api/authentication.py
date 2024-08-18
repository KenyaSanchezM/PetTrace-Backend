from django.contrib.auth import get_user_model
from .models import ShelterUser
from django.contrib.auth.backends import BaseBackend

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        User = get_user_model()
        
        print(f'Intentando autenticar con email: {email}')
        
        # Autenticar como User
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                print(f'Autenticación exitosa como User: {user.email} con ID: {user.id}')
                return user
            else:
                print(f'Contraseña incorrecta para User: {user.email}')
        except User.DoesNotExist:
            print(f'No se encontró User con email: {email}')
        
        # Autenticar como ShelterUser
        try:
            shelter_user = ShelterUser.objects.get(email=email)
            if shelter_user.check_password(password):
                print(f'Autenticación exitosa como ShelterUser: {shelter_user.email} con ID: {shelter_user.id}')
                return shelter_user
            else:
                print(f'Contraseña incorrecta para ShelterUser: {shelter_user.email}')
        except ShelterUser.DoesNotExist:
            print(f'No se encontró ShelterUser con email: {email}')
        
        print('Autenticación fallida para ambos tipos de usuarios')
        return None

    def get_user(self, user_id):
        User = get_user_model()
        
        print(f'Buscando usuario con ID: {user_id}')
        
        # Primero verifica si es un User
        try:
            user = User.objects.get(pk=user_id)
            if user:
                print(f'Usuario encontrado como User con ID: {user.id}')
                return user
        except User.DoesNotExist:
            print(f'No se encontró User con ID: {user_id}')
        
        # Luego verifica si es un ShelterUser
        try:
            shelter_user = ShelterUser.objects.get(pk=user_id)
            if shelter_user:
                print(f'Usuario encontrado como ShelterUser con ID: {shelter_user.id}')
                return shelter_user
        except ShelterUser.DoesNotExist:
            print(f'No se encontró ShelterUser con ID: {user_id}')
        
        print(f'No se encontró usuario con ID: {user_id} en ninguna tabla')
        return None
