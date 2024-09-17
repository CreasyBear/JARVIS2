import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
from transformers import ViTForImageClassification, ViTImageProcessor

# Load pre-trained models
cnn_model = load_model('path/to/cnn_model.h5')
vit_processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
vit_model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

def preprocess_image(image_path, model_type='cnn'):
    image = Image.open(image_path).resize((224, 224))
    if model_type == 'cnn':
        image_array = np.array(image) / 255.0
        return np.expand_dims(image_array, axis=0)
    elif model_type == 'vit':
        encoding = vit_processor(images=image, return_tensors="pt")
        return encoding

def analyze_image(image_path, model_type='cnn'):
    if model_type == 'cnn':
        image = preprocess_image(image_path, model_type)
        predictions = cnn_model.predict(image)
        return predictions.tolist()
    elif model_type == 'vit':
        encoding = preprocess_image(image_path, model_type)
        outputs = vit_model(**encoding)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        return vit_model.config.id2label[predicted_class_idx]