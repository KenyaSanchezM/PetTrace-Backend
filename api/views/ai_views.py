#api/models/views.py
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from api.models.dog_prediction import DogPrediction
from django.core.files.storage import default_storage
#from django.contrib.auth.models import User
import logging

from django.contrib.auth import get_user_model
User = get_user_model()


# Configurar logging
logger = logging.getLogger('api')

# Cargar el modelo de IA
model_path = os.path.join(settings.MODEL_ROOT, 'model.h5')
model = load_model(model_path)

# Mapeo de las razas
breed_map = {
    0: 'Afgano', 1: 'Akita', 2: 'AlaskanMalamute', 3: 'Basenji', 4: 'BassetHound',
    5: 'Beagle', 6: 'BeardedCollie', 7: 'BichonFrise', 8: 'BorderCollie', 9: 'BorderTerrier',
    10: 'Borzoi', 11: 'BostonTerrier', 12: 'Boxer', 13: 'Bulldog', 14: 'Bullmastiff',
    15: 'CairnTerrier', 16: 'CaneCorso', 17: 'Caniche', 18: 'CavalierKingCharlesSpaniel', 19: 'Chihuahua',
    20: 'ChowChow', 21: 'CockerSpaniel', 22: 'Collie', 23: 'Dalmata', 24: 'DobermanPinscher',
    25: 'DogoArgentino', 26: 'DogueDeBourdeaux', 27: 'FoxTerrier', 28: 'GalgoEspanol', 29: 'GoldenRetriver',
    30: 'GranDanes', 31: 'Greyhound', 32: 'GrifonDeBruselas', 33: 'Havanese', 34: 'Husky',
    35: 'IrishSetter', 36: 'JackRusselTerrier', 37: 'Keeshond', 38: 'KerryBlueTerrier', 39: 'Komondor',
    40: 'Kuvasz', 41: 'LabradorRetriever', 42: 'LhasaApso', 43: 'Maltes', 44: 'MastinNapolitano',
    45: 'MastinTibetano', 46: 'NorfolkTerrier', 47: 'NorwichTerrier', 48: 'Papillon', 49: 'PastorAleman',
    50: 'Pequines', 51: 'PerroDeAguaPortugues', 52: 'PerroDeMontanaDeBerna', 53: 'PerroLoboDeSaarloos', 54: 'PinscherMiniatura',
    55: 'PitBull', 56: 'Pomerania', 57: 'PresaCanario', 58: 'Pug', 59: 'RatTerrier',
    60: 'Rottweiler', 61: 'Saluki', 62: 'Samoyedo', 63: 'SanBernardo', 64: 'Schipperke',
    65: 'Schnauzer', 66: 'SetterInglés', 67: 'SharPei', 68: 'ShibaInu', 69: 'ShihTzu',
    70: 'StaffordshireBullTerrier', 71: 'YorkshireTerrier'
}

@csrf_exempt
def predict_breed(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            img_file = request.FILES['file']
            img_name = img_file.name
            img_path = os.path.join(settings.MEDIA_ROOT, 'dog_images', img_name)

            # Crear la carpeta si no existe
            os.makedirs(os.path.dirname(img_path), exist_ok=True)

            # Guardar la imagen temporalmente
            with open(img_path, 'wb+') as destination:
                for chunk in img_file.chunks():
                    destination.write(chunk)

            # Preprocesar y predecir
            img = image.load_img(img_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0  # Normalizar la imagen

            predictions = model.predict(img_array)[0]
            top_10_indices = predictions.argsort()[-10:][::-1]
            top_10_breeds = [breed_map.get(i, 'Unknown') for i in top_10_indices]

            return JsonResponse({'top_10_breeds': top_10_breeds})

        except FileNotFoundError as e:
            return JsonResponse({'error': 'File not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
