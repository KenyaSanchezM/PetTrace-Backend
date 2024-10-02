from django.urls import path, include
from .views.views import register_user, register_shelter, login_user, perfil_usuario,register_dog,register_dog_shelter, perfil_usuario_refugio,CustomTokenObtainPairView, DogPredictionListView, delete_dog_prediction, update_dog_prediction,delete_dog_prediction_shelter, update_dog_prediction_shelter, SearchDogsView, mark_dog, Refugios,PerfilUsuarioView, dog_filter, primeros_seis_perros,perfil_shelter_presente, register_event,Eventos, delete_event, update_event,refugios_principal,MatchPetsView,update_user_profile,delete_user_profile



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('registro-perros/', register_dog, name='registro-perros'),
    path('registro-perros-refugios/', register_dog_shelter, name='registro-perros-refugios'),
    #path('predict-breed/', predict_breed, name='predict-breed'),
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
    path('event/<int:pk>/delete/', delete_event, name='delete-event'),
    path('event/<int:pk>/update/', update_event, name='update-event'),
    path('search-matches/', SearchDogsView.as_view(), name='search-matches'),
    path('mark-dog/<int:pk>/', mark_dog, name='mark-dog'),
    path('ir-perfil-usuario/<int:user_id>/', PerfilUsuarioView.as_view(), name='ir-perfil-usuario'),
    path('dog-filter/', dog_filter, name='dog-filter'),
    path('perros-perdidos/',primeros_seis_perros,name='perros-perdidos'),
    path('refugios/', Refugios.as_view(), name='refugios'),
    path('ir-perfil-refugio/<int:id>/', perfil_shelter_presente.as_view(), name='perfil_usuario_refugio'),
    path('registrar-evento/', register_event, name='registrar-evento'),
    path('eventos/', Eventos.as_view(), name='eventos'),
    path('refugios-principal/',refugios_principal,name='refugios-principal'),
    path('match/', MatchPetsView, name='match-pets'),
    path('user-profile/update/<int:pk>/', update_user_profile, name='update_user_profile'),
    path('user-profile/delete/<int:pk>/', delete_user_profile, name='delete_user_profile')
]

