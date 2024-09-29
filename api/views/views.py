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
from api.models.user import User
from api.serializers import UserSerializer, ShelterUserSerializer, LoginSerializer, DogPredictionSerializer,CustomTokenObtainPairSerializer, DogPredictionShelterSerializer, LostDogSerializer, EventAdvertisementSerializer
from api.models.dog_prediction import DogPrediction
from api.models.event_advertisement import EventAdvertisement
from api.models.dog_prediction_shelter import DogPredictionShelter
from api.models.user import UserDogRelationship
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
from datetime import date
from django.db import models
from django.db.models import OuterRef, Subquery, Exists
from rest_framework.generics import ListAPIView





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
    serializer = ShelterUserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Refugio registrado con éxito'}, status=status.HTTP_201_CREATED)
    else:
        # Imprime los errores del serializer para depuración
        print("Errores del serializer:", serializer.errors)
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
    serializer_class = DogPredictionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Subquery para verificar si hay una relación del usuario con el perro
        userdogrelationship_exists = UserDogRelationship.objects.filter(
            user=user,
            dog_id=OuterRef('id')
        )

        # Obtener todos los perros
        queryset = DogPrediction.objects.annotate(
            relationship_exists=Subquery(userdogrelationship_exists.values('id')[:1])
        ).filter(
            Q(userdogrelationship__user=user, userdogrelationship__is_mine=True) |
            Q(relationship_exists__isnull=True)
        ).order_by('-fecha')

        # Usar un conjunto para evitar duplicados
        seen_dogs = set()
        unique_dogs = []
        
        for dog in queryset:
            if dog.id not in seen_dogs:
                unique_dogs.append(dog)
                seen_dogs.add(dog.id)

        return unique_dogs

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
    
logger = logging.getLogger('api')

class SearchDogsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logger.info("SearchDogsView GET request received.")
        user = request.user

        # Obtener el parámetro 'search' de la URL
        search_params = request.query_params.get('search', '{}')
        logger.info(f"search_params received: {search_params}")  # Log del parámetro recibido

        # Manejo de JSON vacío o mal formado
        try:
            search_params = json.loads(search_params)
            logger.info(f"Decoded search_params: {search_params}")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding search params: {str(e)}")
            return JsonResponse({"message": "Error en el formato de los parámetros."}, status=400)

        # Obtener el ID del perro después de decodificar el JSON
        current_dog_id = search_params.get('current_dog_id')
        logger.info(f"current_dog_id received: {current_dog_id}")  # Log del ID del perro

        if not current_dog_id:
            logger.error("No se proporcionó el ID del perro.")
            return JsonResponse({"message": "Falta el ID del perro."}, status=400)

        try:
            # Buscar el perro con el ID proporcionado
            current_dog = DogPrediction.objects.get(id=current_dog_id)
        except DogPrediction.DoesNotExist:
            logger.error(f"El perro con ID {current_dog_id} no existe.")
            return JsonResponse({"message": "El perro no existe."}, status=404)

        # Normalizar las razas y colores
        breeds = [breed.strip().lower() for breed in current_dog.breeds.split(',')] if current_dog.breeds else []
        colors = [color.strip().lower() for color in current_dog.color.split(',')] if current_dog.color else []

        logger.info(f"Buscando coincidencias para el perro con ID {current_dog_id}: razas={breeds}, colores={colors}")

        # Filtrar perros que no sean el actual
        queryset = DogPrediction.objects.exclude(id=current_dog_id)

        # Filtrar por razas usando `Q`
        if breeds:
            breed_query = Q()
            for breed in breeds[:5]:  # Limitar a las primeras 5 razas
                breed_query |= Q(breeds__icontains=breed.lower())
            queryset = queryset.filter(breed_query)

        # Filtrar por colores usando `Q`
        if colors:
            color_query = Q()
            for color in colors:
                color_query |= Q(color__icontains=color.lower())
            queryset = queryset.filter(color_query)
        
        # Filtrar por tipo (perdido/encontrado)
        logger.info(f"tipo de perro:{current_dog.form_type}")
        if current_dog.form_type.lower() == "perdido":  # Asegúrate de que se usa minúsculas
            logger.info(f"Before filtering1: {queryset.count()} results")
            queryset = queryset.filter(form_type__iexact="encontrado", fecha__gte=current_dog.fecha)
            logger.info(f"After filtering1: {queryset.count()} results")
        elif current_dog.form_type.lower() == "encontrado":
            logger.info(f"Before filtering2: {queryset.count()} results")
            queryset = queryset.filter(form_type__iexact="perdido", fecha__lte=current_dog.fecha)
            logger.info(f"After filtering2: {queryset.count()} results")


        # Excluir perros marcados como 'no mío' para el usuario actual
        not_mine_ids = UserDogRelationship.objects.filter(user=user, is_mine=False).values_list('dog_id', flat=True)
        queryset = queryset.exclude(id__in=not_mine_ids)


        logger.info(f"Filtered queryset: {queryset}")

        # Serializar y devolver los resultados
        serializer = DogPredictionSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_dog(request, pk):  # pk en lugar de dog_id
    user = request.user
    is_marked = request.data.get('is_marked', None)

    if is_marked is None:
        return Response({'error': 'El estado de marcado es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        dog = DogPrediction.objects.get(id=pk)
        
        # Buscar o crear la relación entre el usuario y el perro
        relationship, created = UserDogRelationship.objects.get_or_create(user=user, dog=dog)
        
        # Actualizar si es "mío" o "no es mío"
        relationship.is_mine = is_marked
        relationship.save()

        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    
    except DogPrediction.DoesNotExist:
        return Response({'error': 'Perro no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

class PerfilUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user_data = UserSerializer(user).data
            
            # Obtén los perros asociados a este usuario
            perros = DogPrediction.objects.filter(user=user)
            perros_data = DogPredictionSerializer(perros, many=True).data
            
            # Agrega los perros a los datos del usuario
            user_data['predictions'] = perros_data
            
            return Response(user_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

logger = logging.getLogger('api')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dog_filter(request):
    logger.info(f"GET parameters: {request.GET}")

    user = request.user
    breeds = request.GET.get('breeds', None)
    colors = request.GET.get('colors', None)
    is_mine = request.GET.get('is_mine', None)
    sexo = request.GET.get('sex', None)
    fecha = request.GET.get('date', None)
    estado = request.GET.get('status', None)

    # Validar y convertir el valor de 'is_mine' de cadena a booleano
    if is_mine == 'true':
        is_mine = True
    elif is_mine == 'false':
        is_mine = False
    else:
        is_mine = None  # Si no está presente o es otro valor, lo consideramos como no seleccionado
    
    #print(f"Valor de is_mine recibido: {is_mine}")

    queryset = DogPrediction.objects.all()

    #logger.info(f"Valor de is mine recibido1: {is_mine}")
    #logger.info(f"Valor de : {sexo}")
    #logger.info(f"Valor de : {fecha}")
    #logger.info(f"Valor de : {estado}")

    if breeds:
        breeds_list = [breed.strip() for breed in breeds.split(',')][:5]  # Limpiar espacios y limitar a las primeras 5
        if len(breeds_list) > 0:
            breed_queries = Q()  # Inicializar Q para las razas

            # Añadir condiciones para cada raza
            for breed in breeds_list:
                breed_queries |= Q(breeds__icontains=breed)  # Usar 'icontains' para coincidir con el nombre en el registro

            # Filtrar el queryset usando la consulta construida
            queryset = queryset.filter(breed_queries)

    # Filtrar por colores
    if colors:
        colors_list = [colors.strip() for colors in colors.split(',')]
        if colors and len(colors_list) > 0:
            color_queries = Q()

            # Añadir condiciones para cada raza
            for color in colors_list:
                color_queries |= Q(color__icontains=color)  # Usar 'icontains' para coincidir con el nombre en el registro

            # Filtrar el queryset usando la consulta construida
            queryset = queryset.filter(color_queries)


    if is_mine is not None:
        is_mine = is_mine.lower() == 'true' if isinstance(is_mine, str) else is_mine  # Convertir a booleano si es string
        queryset = queryset.filter(userdogrelationship__user=user, userdogrelationship__is_mine=is_mine)

    # Filtrar por sexo
    if sexo:
        logger.info(f"Valor de sexo recibido: {sexo}")
        queryset = queryset.filter(sexo__iexact=sexo)  # Cambié a 'iexact' para hacer una comparación exacta sin importar mayúsculas

    # Filtrar por fecha
    if fecha:
        queryset = queryset.filter(fecha=fecha)

    # Filtrar por estado
    if estado:
        logger.info(f"Valor de estado recibido: {estado}")
        queryset = queryset.filter(form_type=estado)

    serializer = DogPredictionSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def primeros_seis_perros(request):
    perros = DogPrediction.objects.order_by('fecha')[:6]
    print(perros)  # Verifica qué registros se están obteniendo
    serializer = LostDogSerializer(perros, many=True)  # Usa el nuevo serializer
    return Response(serializer.data)


@permission_classes([AllowAny])
class Refugios(APIView):
    def get(self, request):
        estado = request.query_params.get('estado', None)
        ciudad = request.query_params.get('ciudad', None)

        refugios = ShelterUser.objects.all()

        if estado:
            refugios = refugios.filter(estado=estado)
        if ciudad:
            refugios = refugios.filter(ciudad=ciudad)

        refugios_serializados = ShelterUserSerializer(refugios, many=True)
        return Response(refugios_serializados.data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class perfil_shelter_presente(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener el ID del refugio desde la URL
            shelter_id = kwargs.get('id')  # Asegúrate de que 'id' está en la URL
            # Obtener el perfil del refugio
            shelter_user = ShelterUser.objects.get(pk=shelter_id)

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

logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_event(request):
    if request.method == 'POST':
        imagen_evento = request.FILES.get('imagen_evento')
        try:
            shelter_user = ShelterUser.objects.get(pk=request.user.pk)
        except ShelterUser.DoesNotExist:
            return JsonResponse({'error': 'ShelterUser instance not found'}, status=404)

        # Imprimir los datos recibidos
        print(request.POST)  # Agrega esto para verificar los datos recibidos

        # Crear el evento
        event_advertisement = EventAdvertisement(
            nombre_evento=request.POST.get('nombre_evento', ''),
            descripcion_evento=request.POST.get('descripcion_evento', ''),
            lugar_evento=request.POST.get('lugar_evento', ''),
            motivo=request.POST.get('motivo', ''),
            anfitrion_evento=request.POST.get('anfitrion_evento', ''),
            fecha_evento=request.POST.get('fecha_evento', ''),
            hora_evento=request.POST.get('hora_evento', ''),
            imagen_evento=imagen_evento,
            
            refUser=shelter_user
        )
        
        try:
            event_advertisement.save()
        except Exception as e:
            logger.error(f"Error al guardar el evento: {str(e)}")  # Manejo de errores al guardar
            return JsonResponse({'error': str(e)}, status=500)

        serializer = EventAdvertisementSerializer(event_advertisement)
        return JsonResponse({'message': 'Registro guardado exitosamente', 'event': serializer.data})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@permission_classes([AllowAny])
class Eventos(APIView):
    def get(self, request):
        
        eventos = EventAdvertisement.objects.all()

        eventos_serializados = EventAdvertisementSerializer(eventos, many=True)
        return Response(eventos_serializados.data, status=status.HTTP_200_OK)

