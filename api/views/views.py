from rest_framework.decorators import api_view, permission_classes  # Asegúrate de importar permission_classes
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.permissions import IsAuthenticated  # Asegúrate de importar IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from api.models.shelter_user import ShelterUser
from api.serializers import UserSerializer, ShelterUserSerializer, LoginSerializer, DogPredictionSerializer,CustomTokenObtainPairSerializer, DogPredictionShelterSerializer, EventAdvertisementSerializer
from api.models.dog_prediction import DogPrediction
from api.models.event_advertisement import EventAdvertisement
from api.models.dog_prediction_shelter import DogPredictionShelter
from django.contrib.auth import get_user_model
import os
from django.conf import settings
import logging
from django.http import JsonResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from django.core.files.storage import default_storage
import jwt
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny
from django.http import QueryDict
import json
from django.db.models import Q




class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

logger = logging.getLogger('api')

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    # Combina data y files
    data = request.data.copy()  # Crea una copia mutable de request.data
    data.update(request.FILES)  # Añade los archivos al diccionario

    # Inicializa el serializer con los datos combinados
    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_shelter(request):
    # Combina data y files
    data = request.data.copy()  # Crear una copia mutable de request.data
    data.update(request.FILES)  # Añadir los archivos al diccionario

    # Inicializa el serializer con los datos combinados
    serializer = ShelterUserSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Refugio registrado con éxito'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Autenticación del usuario
    user = authenticate(request, email=email, password=password)

    if user:
        # Usa el CustomTokenObtainPairSerializer para obtener ambos tokens
        serializer = CustomTokenObtainPairSerializer.get_token(user)
        tokens = {
            'refresh': str(serializer),
            'access': str(serializer.access_token),
            'user_type': user.user_type
        }
        return Response(tokens)
    else:
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)



class perfil_usuario(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.user_type == 'shelter':
            return Response({'error': 'No autorizado para acceder a este perfil'}, status=status.HTTP_403_FORBIDDEN)

        predictions = DogPrediction.objects.filter(user=user)
        user_serializer = UserSerializer(user)
        prediction_serializer = DogPredictionSerializer(predictions, many=True)

        return Response({
            'user': user_serializer.data,
            'predictions': prediction_serializer.data if predictions.exists() else []
        })


class perfil_usuario_refugio(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Verificar si el usuario es de tipo 'shelter'
        if user.user_type != 'shelter':
            return Response({'error': 'No autorizado para acceder a este perfil'}, status=status.HTTP_403_FORBIDDEN)

        try:
            # Obtener el perfil del refugio
            shelter_user = ShelterUser.objects.get(pk=user.pk)

            # Obtener las predicciones asociadas a este refugio, si existe una relación
            predictions = DogPredictionShelter.objects.filter(shelter_user=shelter_user)

            # Serializar los datos del refugio
            user_serializer = ShelterUserSerializer(shelter_user)
            prediction_serializer = DogPredictionShelterSerializer(predictions, many=True)

            # Devolver la información del refugio y las predicciones
            return Response({
                'shelter_user': user_serializer.data,
                'predictions': prediction_serializer.data if predictions.exists() else []
            })
        except ShelterUser.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)


# Configurar logging
logger = logging.getLogger('api')
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_dog(request):
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=403)

            img_file = request.FILES.get('file')
            profile_img1 = request.FILES.get('profile_image1')
            profile_img2 = request.FILES.get('profile_image2')

            dog_prediction = DogPrediction(
                breeds=request.POST.get('breeds', ''),
                image=img_file,
                profile_image1=profile_img1,
                profile_image2=profile_img2,
                ubicacion=request.POST.get('ubicacion', ''),
                tieneCollar=request.POST.get('tieneCollar', ''),
                nombre=request.POST.get('nombre', ''),
                edad=request.POST.get('edad', ''),
                color=request.POST.get('color', ''),
                caracteristicas=request.POST.get('caracteristicas', ''),
                fecha=request.POST.get('fecha', ''),
                sexo=request.POST.get('sexo', ''),
                form_type=request.POST.get('form_type', ''),
                user=request.user
            )
            dog_prediction.save()

            return JsonResponse({'message': 'Registro guardado exitosamente'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

logger = logging.getLogger('api')

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_dog_shelter(request):
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=403)

            # Obtención de las imágenes del request
            img_file = request.FILES.get('file')
            profile_img1 = request.FILES.get('profile_image1')
            profile_img2 = request.FILES.get('profile_image2')

            logger.info(f"Authenticated user: {request.user}")

            try:
                # Obtener la instancia del refugio
                user_instance = ShelterUser.objects.get(pk=request.user.pk)
                logger.info(f"ShelterUser instance: {user_instance}")
            except ShelterUser.DoesNotExist:
                logger.error(f"ShelterUser with pk={request.user.pk} does not exist.")
                return JsonResponse({'error': 'ShelterUser instance not found'}, status=404)

            # Creación de la instancia de DogPredictionShelter
            dog_prediction_shelter = DogPredictionShelter(
                breeds=request.POST.get('breeds', ''),
                image=img_file,  # Asigna directamente el archivo
                profile_image1=profile_img1,  # Primer perfil opcional
                profile_image2=profile_img2,  # Segundo perfil opcional
                sexo=request.POST.get('sexo', ''),
                tamanio=request.POST.get('tamanio', ''),
                nombre=request.POST.get('nombre', ''),
                edad=request.POST.get('edad', 0),  # Validar edad como entero
                color=request.POST.get('color', ''),
                caracteristicas=request.POST.get('caracteristicas', ''),
                temperamento=request.POST.get('temperamento', ''),
                vacunas=request.POST.get('vacunas', ''),
                esterilizado=request.POST.get('esterilizado', ''),
                shelter_user=user_instance
            )
            dog_prediction_shelter.save()

            return JsonResponse({'message': 'Registro guardado exitosamente'})

        except Exception as e:
            logger.error(f"Error al registrar el perro de refugio: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

class DogPredictionListView(generics.ListAPIView):
    queryset = DogPrediction.objects.select_related('user').all()  # Optimiza para incluir los datos del usuario
    serializer_class = DogPredictionSerializer
    permission_classes = [IsAuthenticated]  # Asegúrate de que se requiera autenticación

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dog_prediction(request, pk):
    try:
        dog_prediction = DogPrediction.objects.get(pk=pk, user=request.user)
    except DogPrediction.DoesNotExist:
        return Response({'error': 'Publicación no encontrada o no tienes permiso para eliminarla.'}, status=status.HTTP_404_NOT_FOUND)

    dog_prediction.delete()
    return Response({'message': 'Publicación eliminada con éxito.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_dog_prediction(request, pk):
    try:
        dog_prediction = DogPrediction.objects.get(pk=pk, user=request.user)
    except DogPrediction.DoesNotExist:
        return Response({'error': 'Publicación no encontrada o no tienes permiso para actualizarla.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = DogPredictionSerializer(dog_prediction, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dog_prediction_shelter(request, pk):
    try:
        dog_prediction_shelter = DogPredictionShelter.objects.get(pk=pk, shelter_user=request.user)
    except DogPredictionShelter.DoesNotExist:
        return Response({'error': 'Publicación no encontrada o no tienes permiso para eliminarla.'}, status=status.HTTP_404_NOT_FOUND)

    dog_prediction_shelter.delete()
    return Response({'message': 'Publicación eliminada con éxito.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_dog_prediction_shelter(request, pk):
    try:
        dog_prediction_shelter = DogPredictionShelter.objects.get(pk=pk, shelter_user=request.user)
    except DogPredictionShelter.DoesNotExist:
        return Response({'error': 'Publicación no encontrada o no tienes permiso para actualizarla.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = DogPredictionShelterSerializer(dog_prediction_shelter, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
logger = logging.getLogger(__name__)

class SearchDogsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logger.info("SearchDogsView GET request received.")
        user = request.user
        breeds = request.query_params.get('breeds', '[]')
        colors = request.query_params.get('colors', '[]')

        logger.info(f"Parameters received: breeds={breeds}, colors={colors}")

        try:
            breeds = json.loads(breeds)  # Convertir a lista
            colors = json.loads(colors)
        except json.JSONDecodeError:
            logger.error("Error decoding parameters.")
            return JsonResponse({"message": "Error en el formato de los parámetros."}, status=400)

        queryset = DogPrediction.objects.all()

        # Filtrar por razas
        if breeds:
            breeds = breeds[:5]  
            queryset = queryset.filter(breeds__contains=breeds)

        # Filtrar por colores
        if colors:
            queryset = queryset.filter(color__contains=colors)

        # Excluir perros que ya fueron marcados como 'is mine' o 'not mine'
        marked_dogs_ids = user.marked_dogs.values_list('id', flat=True)
        queryset = queryset.exclude(id__in=marked_dogs_ids)

        logger.info(f"Filtered queryset: {queryset}")

        serializer = DogPredictionSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)


        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_dog(request, dog_id):
    user = request.user
    is_marked = request.data.get('is_marked', None)
    
    if is_marked is None:
        return Response({'error': 'El estado de marcado es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Lógica para marcar el perro como "es mío" o "no es mío"
        dog = DogPrediction.objects.get(id=dog_id)
        if is_marked:
            user.marked_dogs.add(dog)
        else:
            user.marked_dogs.remove(dog)
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    except DogPrediction.DoesNotExist:
        return Response({'error': 'Perro no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    

logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_event(request):
    if request.method == 'POST':
        try:
            # Verificar si el usuario es un refugio
            try:
                shelter_user = ShelterUser.objects.get(pk=request.user.pk)
            except ShelterUser.DoesNotExist:
                return JsonResponse({'error': 'ShelterUser instance not found'}, status=404)

            # Crear el evento
            event_advertisement = EventAdvertisement(
                nombre_evento=request.POST.get('nombre_evento', ''),
                descripcion_evento=request.POST.get('descripcion_evento', ''),
                lugar_evento=request.POST.get('lugar_evento', ''),
                motivo=request.POST.get('motivo',''),
                anfitrion_evento=request.POST.get('anfitrion_evento', ''),
                fecha_evento=request.POST.get('fecha_evento',''),
                hora_evento=request.POST.get('hora_evento',''),
                refUser=shelter_user
            )
            event_advertisement.save()

            # Serializar el evento registrado
            serializer = EventAdvertisementSerializer(event_advertisement)
            return JsonResponse({'message': 'Registro guardado exitosamente', 'event': serializer.data})

        except Exception as e:
            logger.error(f"Error al registrar el evento de refugio: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
            