import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from .models import DogPrediction

# Cargar el modelo de IA desde el archivo model.h5
model = load_model('models\model.h5')

# Mapeo de las razas
breed_map = {
    0: 'Afgano', 1: 'Akita', 2: 'Alaskan Malamute', 3: 'Basenji', 4: 'Basset Hound',
    5: 'Beagle', 6: 'Bearded Collie', 7: 'Bichon Frise', 8: 'Border Collie', 9: 'Border Terrier',
    10: 'Borzoi', 11: 'Boston terrier', 12: 'Boxer', 13: 'Bulldog', 14: 'Bullmastiff',
    15: 'Cairn Terrier', 16: 'Cane Corso', 17: 'Caniche', 18: 'Cavalier King Charles Spaniel', 19: 'Chihuahua',
    20: 'Chow chow', 21: 'Cocker spaniel', 22: 'Collie', 23: 'Dalmata', 24: 'Doberman pinscher',
    25: 'Dogo Argentino', 26: 'Dogue de Bourdeaux', 27: 'Fox Terrier', 28: 'Galgo espanol', 29: 'GoldenRetriver',
    30: 'GranDanes', 31: 'Greyhound', 32: 'Grifon de Bruselas', 33: 'Havanese', 34: 'Husky',
    35: 'Irish Setter', 36: 'Jack russel terrier', 37: 'Keeshond', 38: 'Kerry Blue Terrier', 39: 'Komondor',
    40: 'Kuvasz', 41: 'Labrador retriever', 42: 'Lhasa Apso', 43: 'Maltes', 44: 'Mastin Napolitano',
    45: 'Mastin tibetano', 46: 'Norfolk terrier', 47: 'Norwich Terrier', 48: 'Papillon', 49: 'Pastor Aleman',
    50: 'Pequines', 51: 'Perro de agua portugues', 52: 'Perro de montana de Berna', 53: 'Perro lobo de saarloos', 54: 'Pinscher miniatura',
    55: 'PitBull', 56: 'Pomerania', 57: 'Presa canario', 58: 'Pug', 59: 'Rat terrier',
    60: 'Rottweiler', 61: 'Saluki', 62: 'Samoyedo', 63: 'San bernardo', 64: 'Schipperke',
    65: 'Schnauzer', 66: 'Setter Inglés', 67: 'Shar pei', 68: 'Shiba inu', 69: 'Shih Tzu',
    70: 'Staffordshire bull terrier', 71: 'Yorkshire terrier'
}

@csrf_exempt
def predict_breed(request):
    if request.method == 'POST' and request.FILES.get('file'):
        img = request.FILES['file']
        img_path = 'temp_image.jpg'
        
        # Guardar la imagen temporalmente
        with open(img_path, 'wb+') as destination:
            for chunk in img.chunks():
                destination.write(chunk)

        # Cargar y preprocesar la imagen para la predicción
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalizar la imagen

        # Realizar la predicción
        predictions = model.predict(img_array)[0]
        top_10_indices = predictions.argsort()[-10:][::-1]
        top_10_breeds = [breed_map.get(i, 'Unknown') for i in top_10_indices]

        # Guardar las predicciones en la base de datos (ejemplo)
        dog_prediction = DogPrediction(
            breeds=top_10_breeds,
            ubicacion=request.POST.get('ubicacion', ''),
            tieneCollar=request.POST.get('tieneCollar', ''),
            nombre=request.POST.get('nombre', ''),
            edad=request.POST.get('edad', ''),
            color=request.POST.get('color', ''),
            caracteristicas=request.POST.get('caracteristicas', ''),
            fecha=request.POST.get('fecha', ''),
            form_type=request.POST.get('form_type', '')
        )
        dog_prediction.save()

        return JsonResponse({'top_10_breeds': top_10_breeds})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def index_to_breed(index):
    return breed_map.get(index, 'Unknown')

