import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import time
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FoodCalorieEstimator:
    def __init__(self):
        self.model = None
        self.cache = {}
        self.load_model()
        
    def load_model(self):
        try:
            self.model = tf.keras.models.load_model('results/main_model.keras')
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def preprocess_image(self, image):
        try:
            # Конвертация в numpy array если это PIL Image
            if isinstance(image, Image.Image):
                image = np.array(image)
            
            # Изменение размера и нормализация
            img = tf.image.resize(image, [224, 224])
            img = tf.cast(img, tf.float32) / 255.0
            return img
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise

    def get_cache_key(self, image):
        # Создаем уникальный ключ для кэширования
        return hash(image.tobytes())

    def predict(self, image):
        try:
            start_time = time.time()
            
            # Проверяем кэш
            cache_key = self.get_cache_key(image)
            if cache_key in self.cache:
                logger.info("Result found in cache")
                return self.cache[cache_key]
            
            # Предобработка
            processed_img = self.preprocess_image(image)
            
            # Предсказание
            calories = self.model.predict(
                np.expand_dims(processed_img, axis=0)
            )[0][0]
            
            # Формируем результат
            result = {
                "calories": float(calories),
                "timestamp": datetime.now().isoformat(),
                "processing_time": time.time() - start_time
            }
            
            # Сохраняем в кэш
            self.cache[cache_key] = result
            
            logger.info(f"Prediction made: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise

# Инициализация
estimator = FoodCalorieEstimator()

def process_image(image):
    try:
        result = estimator.predict(image)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error processing image: {str(e)}"

# Создание интерфейса
interface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(),
    outputs=gr.Textbox(label="Prediction Results"),
    title="Food Calorie Estimator",
    description="Upload a food image to estimate calories",
    examples=[["example1.jpg"], ["example2.jpg"]]
)

# Запуск
interface.launch() 