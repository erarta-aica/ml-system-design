import gradio as gr
import tensorflow as tf
from PIL import Image
import numpy as np

def load_model():
    return tf.keras.models.load_model('results/main_model.keras')

def process_image(image):
    # Предобработка изображения
    img = tf.image.resize(image, [224, 224])
    img = tf.cast(img, tf.float32) / 255.0
    
    # Предсказание
    calories = model.predict(np.expand_dims(img, axis=0))[0][0]
    
    return f"Estimated calories: {calories:.0f} kcal"

model = load_model()
interface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(),
    outputs="text",
    title="Food Calorie Estimator"
)

interface.launch() 