from rest_framework.decorators import api_view, permission_classes  # Asegúrate de importar permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  # Asegúrate de importar IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token

from api.models.user import User
from api.models.shelter_user import ShelterUser
from api.serializers import UserSerializer, ShelterUserSerializer, LoginSerializer

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        print("Datos validados:", serializer.validated_data)
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        print("Usuario autenticado:", user)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "Inicio de sesión exitoso",'token': token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
