#api/views/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from api.models import user, shelter_user, dog_prediction, event_advertisement
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = request.POST
        nombre = data.get('nombre')
        email = data.get('email')
        contraseña = data.get('contraseña')
        telefono = data.get('telefono')
        publicaciones = data.get('publicaciones')
        
        # Crear usuario
        user = User.objects.create(
            nombre=nombre,
            correo_electronico=email,
            contrasena=contraseña,
            telefono_user=telefono,
            # publicaciones=publicaciones  # Aquí debes manejar la relación ManyToMany correctamente
        )
        
        # Si publicaciones es una lista de IDs de DogPrediction:
        if publicaciones:
            for publicacion_id in publicaciones:
                dog_prediction = DogPrediction.objects.get(id=publicacion_id)
                user.publicaciones.add(dog_prediction)
        
        user.save()
        
        return JsonResponse({'message': 'Usuario registrado con éxito'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def register_shelter(request):
    if request.method == 'POST':
        data = request.POST
        nombre = data.get('nombre')
        email = data.get('email')
        contraseña = data.get('contraseña')
        telefono = data.get('telefono')
        
        # Crear usuario
        shelter_user = ShelterUser.objects.create(
            nombre=nombre,
            correo_electronico=email,
            contrasena=contraseña,
            telefono_shelter=telefono
        )
        shelter_user.save()
        
        return JsonResponse({'message': 'Usuario de refugio registrado con éxito'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)
