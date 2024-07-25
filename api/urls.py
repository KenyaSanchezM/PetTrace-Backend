from django.urls import path
from .views.views import register_user, register_shelter, login_user, perfil_usuario
from .views.ai_views import predict_breed

urlpatterns = [
    path('registro-perros/', predict_breed, name='registro-perros'),
    path('registro-usuario/', register_user, name='register'), 
    path('registro-refugio/', register_shelter, name='registro-refugio'),
    path('inicio-sesion/', login_user, name='login_user'),
    path('perfil-usuario/', perfil_usuario, name='perfil-usuario'),
]
