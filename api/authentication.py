from django.contrib.auth import get_user_model
from .models.shelter_user import ShelterUser
from django.contrib.auth.backends import BaseBackend

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        User = get_user_model()
        
        # Autenticar como User
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
        
        # Autenticar como ShelterUser
        try:
            shelter_user = ShelterUser.objects.get(email=email)
            if shelter_user.check_password(password):
                return shelter_user
        except ShelterUser.DoesNotExist:
            pass
        
        return None

    def get_user(self, user_id):
        User = get_user_model()
        
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass

        try:
            return ShelterUser.objects.get(pk=user_id)
        except ShelterUser.DoesNotExist:
            pass
        
        return None

