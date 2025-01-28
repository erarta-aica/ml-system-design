import tensorflow_datasets as tfds
import pandas as pd
import numpy as np
import asyncio
import aiohttp
import tensorflow as tf
from tqdm import tqdm
from PIL import Image
import io

class FoodDataLoader:
    def __init__(self):
        """Инициализация загрузчика данных"""
        # Примерные калории для каждой категории (среднее значение)
        self.category_calories = {
            'apple_pie': 300,
            'baby_back_ribs': 600,
            'baklava': 350,
            'beef_carpaccio': 200,
            'beef_tartare': 250,
            'beet_salad': 150,
            'beignets': 400,
            'bibimbap': 500,
            'bread_pudding': 450,
            'breakfast_burrito': 550
        }

    async def download_and_process_image(self, image_tensor, session):
        """Обработка отдельного изображения"""
        try:
            # Преобразование тензора в массив numpy
            image_array = image_tensor.numpy()
            
            # Извлечение характеристик изображения
            features = {
                'width': image_array.shape[1],
                'height': image_array.shape[0],
                'aspect_ratio': image_array.shape[1] / image_array.shape[0],
                'brightness': np.mean(image_array) / 255.0,
                'saturation': np.std(image_array) / 255.0
            }
            
            return features
            
        except Exception as e:
            print(f"Ошибка при обработке изображения: {e}")
            return None

    async def load_dataset(self, num_examples=1000):
        """
        Асинхронная загрузка датасета
        
        Args:
            num_examples (int): Количество примеров для загрузки
            
        Returns:
            tuple: (pd.DataFrame, list) - Датафрейм с данными и список изображений
        """
        print("Загрузка датасета Food101...")
        
        builder = tfds.builder('food101')
        builder.download_and_prepare()
        info = builder.info
        dataset = builder.as_dataset(split='train')

        data = []
        images = []  # Список для хранения изображений
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            # Создаем задачи для обработки изображений
            for i, example in enumerate(dataset.take(num_examples)):
                image = example['image']
                label = example['label'].numpy()
                category = tfds.features.ClassLabel(names=info.features['label'].names).int2str(label)
                
                if category in self.category_calories:
                    # Добавляем случайное отклонение к базовой калорийности (±20%)
                    base_calories = self.category_calories[category]
                    calories = np.random.normal(base_calories, base_calories * 0.1)
                    
                    task = asyncio.ensure_future(self.download_and_process_image(image, session))
                    tasks.append((task, category, calories, image))  # Добавляем image в кортеж
            
            # Обработка изображений с progress bar
            print("Обработка изображений...")
            for task, category, calories, image in tqdm(tasks, total=len(tasks)):
                features = await task
                if features is not None:
                    data_entry = {
                        'category': category,
                        'calories': max(50, min(1500, calories)),  # Ограничиваем разумным диапазоном
                        **features
                    }
                    data.append(data_entry)
                    images.append(image)  # Сохраняем изображение
        
        return pd.DataFrame(data), images  # Возвращаем и датафрейм, и список изображений

    def get_category_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Получение статистики по категориям
        
        Args:
            df (pd.DataFrame): Входной датафрейм
            
        Returns:
            pd.DataFrame: Статистика по категориям
        """
        return df.groupby('category').agg({
            'calories': ['mean', 'std', 'count'],
            'brightness': 'mean',
            'saturation': 'mean',
            'aspect_ratio': 'mean'
        }).round(2)
