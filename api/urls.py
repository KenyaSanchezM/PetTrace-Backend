from django.urls import path
from .views.views import register_user, register_shelter, login_user, perfil_usuario,register_dog,register_dog_shelter
from .views.ai_views import predict_breed

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('registro-perros/', register_dog, name='registro-perros'),
    path('registro-perros-refugios/', register_dog_shelter, name='registro-perros-refugios'),
    path('predict-breed/', predict_breed, name='predict-breed'),
    path('registro-usuario/', register_user, name='register'), 
    path('registro-refugio/', register_shelter, name='registro-refugio'),
    path('inicio-sesion/', login_user, name='login_user'),
    path('perfil-usuario/', perfil_usuario.as_view(), name='perfil-usuario'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
