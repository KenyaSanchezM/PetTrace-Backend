from rest_framework import serializers
from django.contrib.auth import authenticate
from api.models.user import User
from api.models.shelter_user import ShelterUser
from api.models.dog_prediction import DogPrediction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Añadir email al token
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Añadir email al refresh_token en la respuesta
        refresh = self.get_token(self.user)
        data['email'] = refresh['email']
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'nombre', 'telefono', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            telefono=validated_data['telefono']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ShelterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelterUser
        fields = ['nombre', 'email', 'telefono', 'estado', 'ciudad', 'direccion', 'codigoPostal', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # La contraseña no debe ser leída en las respuestas
        }

    def create(self, validated_data):
        # Crear y guardar el usuario utilizando el método 'create_user' si está disponible en tu modelo
        user = ShelterUser.objects.create_user(
            nombre=validated_data['nombre'],
            email=validated_data['email'],
            telefono=validated_data['telefono'],
            estado=validated_data['estado'],
            ciudad=validated_data['ciudad'],
            direccion=validated_data['direccion'],
            codigoPostal=validated_data['codigoPostal'],
            password=validated_data['password']
        )
        return user

    def validate_email(self, value):
        # Validar que el correo electrónico sea único
        if ShelterUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class DogPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogPrediction
        fields = ['nombre', 'edad', 'color', 'user', 'ubicacion', 'tieneCollar', 'caracteristicas', 'fecha', 'form_type', 'image']

