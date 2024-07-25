from rest_framework import serializers
from django.contrib.auth import authenticate
from api.models.user import User
from api.models.shelter_user import ShelterUser

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
        fields = ['nombre', 'email', 'telefono', 'estado', 'ciudad', 'direccion', 'codigoPostal', 'password_R']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = ShelterUser(
            nombre=validated_data['nombre'],
            email=validated_data['email'],
            telefono=validated_data['telefono'],
            estado=validated_data['estado'],
            ciudad=validated_data['ciudad'],
            direccion=validated_data['direccion'],
            CP=validated_data['codigoPostal']
        )
        user.set_password(validated_data['password_r'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
