from django.urls import path
from . import ai_views

urlpatterns = [
    path('api/RegistroPerros/', ai_views.predict_breed, name='registrar-perro'),

]