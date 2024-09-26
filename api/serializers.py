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
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email', 'nombre', 'telefono', 'password', 'user_type', 'profile_image']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_image = validated_data.pop('profile_image', None)  # Extraer la imagen si existe
        user = User(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            telefono=validated_data['telefono'],
            user_type=validated_data['user_type']
        )
        if profile_image:
            user.profile_image = profile_image
        user.set_password(validated_data['password'])
        user.save()
        return user

class ShelterUserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = ShelterUser
        fields = ['email', 'nombre', 'telefono', 'user_type', 'profile_image', 'password', 'estado', 'ciudad', 'direccion', 'codigoPostal']
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_image': {'required': False}
        }

    def create(self, validated_data):
        email = validated_data['email']
        if ShelterUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Este email ya está registrado.'})

        # Extraer imagen de perfil si existe
        profile_image = validated_data.pop('profile_image', None)

        shelter_user = ShelterUser(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            telefono=validated_data['telefono'],
            estado=validated_data.get('estado', None),
            ciudad=validated_data.get('ciudad', None),
            direccion=validated_data.get('direccion', None),
            codigoPostal=validated_data.get('codigoPostal', None),
            user_type=validated_data['user_type'],
        )
        shelter_user.set_password(validated_data['password'])

        # Asignar la imagen de perfil si está presente
        if profile_image:
            shelter_user.profile_image = profile_image

        shelter_user.save()
        return shelter_user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class DogPredictionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Cambia este campo para incluir los datos completos del usuario
    user_id = serializers.IntegerField(source='user.id', read_only=True)  # Agrega esta línea

    class Meta:
        model = DogPrediction
        fields = ['id','nombre', 'edad', 'color', 'user', 'ubicacion', 'tieneCollar','breeds', 
                  'caracteristicas', 'fecha', 'form_type', 'image', 'profile_image1', 'profile_image2', 'sexo','user_id']

                  
class DogPredictionShelterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogPredictionShelter  # Suponiendo que este es el modelo para las predicciones de refugios
        fields = ['id','shelter_user', 'breeds', 'image', 'nombre', 'edad', 'color',
         'caracteristicas', 'sexo', 'tamanio', 'temperamento', 'vacunas', 'esterilizado', 'profile_image1', 'profile_image2']

