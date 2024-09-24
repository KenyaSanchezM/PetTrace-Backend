from django.urls import path, include
from .views.views import register_user, register_shelter, login_user, perfil_usuario,register_dog,register_dog_shelter, perfil_usuario_refugio,CustomTokenObtainPairView, DogPredictionListView, delete_dog_prediction, update_dog_prediction,delete_dog_prediction_shelter, update_dog_prediction_shelter, SearchDogsView, mark_dog
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
    path('perfil-refugio/', perfil_usuario_refugio.as_view(), name='perfil-refugio'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('dog-predictions/', DogPredictionListView.as_view(), name='dog-predictions-list'),
    path('dog-predictions/<int:pk>/delete/', delete_dog_prediction, name='delete-dog-prediction'),
    path('dog-predictions/<int:pk>/update/', update_dog_prediction, name='update-dog-prediction'),
    path('dog-predictions-shelter/<int:pk>/delete/', delete_dog_prediction_shelter, name='delete-dog-prediction-shelter'),
    path('dog-predictions-shelter/<int:pk>/update/', update_dog_prediction_shelter, name='update-dog-prediction-shelter'),
    path('search-matches/', SearchDogsView.as_view(), name='search-matches'),
    path('mark-dog/<int:pk>/', mark_dog, name='mark-dog'),
]

