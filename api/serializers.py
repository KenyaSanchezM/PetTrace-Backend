from rest_framework import serializers
from django.contrib.auth import authenticate
from api.models.user import User
from api.models.shelter_user import ShelterUser
from api.models.dog_prediction import DogPrediction
from api.models.dog_prediction_shelter import DogPredictionShelter
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Añadir información personalizada al token
        token['user_type'] = user.user_type
        
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'nombre', 'telefono', 'password', 'user_type']
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
        fields = ['email', 'nombre', 'telefono', 'password', 'estado', 'ciudad', 'direccion', 'codigoPostal']

    def create(self, validated_data):
        email = validated_data['email']
        # Verificar si el email ya está registrado
        if ShelterUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Este email ya está registrado.'})

        estado = validated_data.pop('estado', None)
        ciudad = validated_data.pop('ciudad', None)
        direccion = validated_data.pop('direccion', None)
        codigoPostal = validated_data.pop('codigoPostal', None)

        shelter_user = ShelterUser.objects.create_user(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            telefono=validated_data['telefono'],
            password=validated_data['password'],
            estado=estado,
            ciudad=ciudad,
            direccion=direccion,
            codigoPostal=codigoPostal
        )
        return ShelterUser




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class DogPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogPrediction
        fields = ['nombre', 'edad', 'color', 'user', 'ubicacion', 'tieneCollar', 'caracteristicas', 'fecha', 'form_type', 'image']

class DogPredictionShelterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogPredictionShelter  # Suponiendo que este es el modelo para las predicciones de refugios
        fields = ['shelter_user', 'breeds', 'image', 'nombre', 'edad', 'color', 'caracteristicas', 'sexo', 'tamanio', 'temperamento', 'vacunas', 'esterilizado']
