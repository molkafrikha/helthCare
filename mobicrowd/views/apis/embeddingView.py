import json
import base64
from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io
from keras.models import load_model
#from mobicrowd.models.UNIQUE.ScoreModelUtils import load_score_model, evaluate

classes = ['Flood', 'Fire', 'Other']

@csrf_exempt
def receive_embedding(request):
    if request.method == 'POST':
        try:
            # Decode the JSON payload
            payload = json.loads(request.body)
            encoded = payload.get('encoded', [])

            if not encoded:
                return JsonResponse({'status': 'error', 'message': 'No encoded data found'}, status=400)

            encoded_array = np.array(encoded)
            decoder = load_model('mobicrowd/models/best_decoder.h5')
            decoded = decoder.predict(encoded_array)
            decoded_array = np.array(decoded)

            # Prepare the data for classification
            classification_model = load_model('mobicrowd/models/best_classif_model.h5')
            predicted_class = classification_model.predict(encoded_array)
            predicted_class_index = np.argmax(predicted_class, axis=1)[0]

            # Calculate quality score
            score_model = load_score_model()
            score, _ = evaluate(score_model, decoded_array[0][:64, :64, :])
            print(score,"///////////////")

            # Extract metadata from the decoded image
            reconstructed_metadata = decoded_array[0][:, 64:, :][0]
            final_metadata = []

            for i in range(0, 24, 3):
                value = np.mean(reconstructed_metadata[i:i+3])
                final_metadata.append(value)

            # Convert the image part of the decoded array to a PIL Image
            img_array = decoded_array[0][:64, :64, :]
            img_array = (img_array * 255).astype(np.uint8)
            img = Image.fromarray(img_array)

            # Convert the PIL Image to a base64-encoded string
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            return JsonResponse({
                'status': 'success',
                'image_base64': img_str,
                'metadata': final_metadata,
                'predicted_class': classes[int(predicted_class_index)],
                'reconstructed_image_score': score
            }, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
