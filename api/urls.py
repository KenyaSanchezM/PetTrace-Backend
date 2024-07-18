# api/urls.py
from django.urls import path
from .views.views import register_user
from .views.ai_views import predict_breed

urlpatterns = [
    path('api/RegistroPerros/', predict_breed, name='registro-perros'),
    path('RegistroUsuarios/', register_user, name='register'),  # Eliminé 'api/' del path

]
