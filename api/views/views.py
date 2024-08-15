from rest_framework.decorators import api_view, permission_classes  # Asegúrate de importar permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  # Asegúrate de importar IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from api.models.shelter_user import ShelterUser
from api.serializers import UserSerializer, ShelterUserSerializer, LoginSerializer, DogPredictionSerializer
from api.models.dog_prediction import DogPrediction
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

logger = logging.getLogger('api')

User = get_user_model()


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Usuario registrado con éxito'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_shelter(request):
    serializer = ShelterUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Refugio registrado con éxito'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = None
    
    # Intenta autenticar como usuario común
    user = authenticate(request, email=email, password=password)
    print(f"Intentando autenticar como usuario común: {user}")
    
    if user is None:
        # Si no encuentra el usuario en la tabla de usuarios comunes, busca en la de refugios
        refresh = RefreshToken.for_user(user)
        try:
            shelter_user = ShelterUser.objects.get(email=email)
            print(f"Shelter user encontrado: {shelter_user}")
            if shelter_user.check_password(password):
                user = shelter_user
                print(f"Autenticado como refugio: {user}")
            else:
                print("Contraseña incorrecta para el refugio")
        except ShelterUser.DoesNotExist:
            print("Shelter user no encontrado")
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': 'shelter' if isinstance(user, ShelterUser) else 'user'
        })
    
    print("No se encontró al usuario o las credenciales son inválidas")
    return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


class perfil_usuario(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Determine if the user is a shelter user or a regular user and get the predictions accordingly
        if hasattr(user, 'shelteruser'):
            predictions = DogPrediction.objects.filter(shelter_user=user)
            user_serializer = ShelterUserSerializer(user.shelteruser)
        else:
            predictions = DogPrediction.objects.filter(user=user)
            user_serializer = UserSerializer(user)
        
        # Serialize the predictions, if any
        prediction_serializer = DogPredictionSerializer(predictions, many=True)

        # Always return the user data, along with any predictions if available
        return Response({
            'user': user_serializer.data,
            'predictions': prediction_serializer.data if predictions.exists() else []
        })

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_dog(request):
    if request.method == 'POST':
        try:
            # Verifica si el usuario está autenticado
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=403)

            img_file = request.FILES.get('file')
            img_name = img_file.name if img_file else None
            img_path = os.path.join(settings.MEDIA_ROOT, 'dog_images', img_name) if img_file else None

            if img_file:
                os.makedirs(os.path.dirname(img_path), exist_ok=True)
                with open(img_path, 'wb+') as destination:
                    for chunk in img_file.chunks():
                        destination.write(chunk)

            # Guardar el registro del perro
            dog_prediction_shelter = DogPrediction(
                breeds=request.POST.get('breeds', ''),
                image='dog_images/' + img_name if img_file else None,
                ubicacion=request.POST.get('ubicacion', ''),
                tieneCollar=request.POST.get('tieneCollar', ''),
                nombre=request.POST.get('nombre', ''),
                edad=request.POST.get('edad', ''),
                color=request.POST.get('color', ''),
                caracteristicas=request.POST.get('caracteristicas', ''),
                fecha=request.POST.get('fecha', ''),
                form_type=request.POST.get('form_type', ''),
                estatus=request.POST.get('estatus', ''),
                user=request.user  # Asignar el usuario autenticado
            )
            dog_prediction.save()

            return JsonResponse({'message': 'Registro guardado exitosamente'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_dog_shelter(request):
    if request.method == 'POST':
        try:
            # Verifica si el usuario está autenticado
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=403)

            img_file = request.FILES.get('file')
            img_name = img_file.name if img_file else None
            img_path = os.path.join(settings.MEDIA_ROOT, 'dog_images', img_name) if img_file else None

            if img_file:
                os.makedirs(os.path.dirname(img_path), exist_ok=True)
                with open(img_path, 'wb+') as destination:
                    for chunk in img_file.chunks():
                        destination.write(chunk)

            # Guardar el registro del perro
            dog_prediction_shelter = DogPredictionShelter(
                breeds=request.POST.get('breeds', ''),
                image='dog_images/' + img_name if img_file else None,
                sexo=request.POST.get('sexo', ''),
                tamanio=request.POST.get('tamanio', ''),
                nombre=request.POST.get('nombre', ''),
                edad=request.POST.get('edad', ''),
                color=request.POST.get('color', ''),
                caracteristicas=request.POST.get('caracteristicas', ''),
                temperamento=request.POST.get('temperamento', ''),
                vacunas=request.POST.get('vacunas', ''),
                esterilizado=request.POST.get('esterilizado', ''),
                user=request.user  # Asignar el usuario autenticado
            )
            dog_prediction.save()

            return JsonResponse({'message': 'Registro guardado exitosamente'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)