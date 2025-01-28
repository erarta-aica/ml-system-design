# Импортируем необходимые модули
from models.baseline_model import build_baseline_model
from models.main_model import build_main_model
from training.train import cross_validate_model
from data_processing.data_loader import FoodDataLoader
import asyncio
import tensorflow as tf
import numpy as np

async def load_and_preprocess_data():
    """Загрузка и предобработка данных"""
    loader = FoodDataLoader()
    df = await loader.load_dataset(num_examples=1000)
    
    # Предобработка изображений
    def preprocess_image(img):
        # Изменение размера и нормализация
        img = tf.image.resize(img, [224, 224])
        img = tf.cast(img, tf.float32) / 255.0
        return img

    # Подготовка данных
    images = np.array([preprocess_image(img) for img in df['image']])
    calories = df['calories'].values.astype(np.float32)
    
    return images, calories

async def main():
    print("Загрузка и подготовка данных...")
    X, y = await load_and_preprocess_data()
    
    # Разделение на обучающую и валидационную выборки
    train_size = int(0.8 * len(X))
    X_train, X_val = X[:train_size], X[train_size:]
    y_train, y_val = y[:train_size], y[train_size:]
    
    # Создание и обучение бейзлайн модели
    print("\nОбучение базовой модели (бейзлайн)...")
    baseline_model = build_baseline_model(input_shape=(224, 224, 3))
    baseline_history = baseline_model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=10,
        batch_size=32
    )
    
    # Оценка бейзлайна
    baseline_metrics = baseline_model.evaluate(X_val, y_val)
    print("\nМетрики базовой модели:")
    print(f"MSE: {baseline_metrics[0]:.2f}")
    print(f"MAE: {baseline_metrics[1]:.2f}")
    
    # Создание и обучение основной модели
    print("\nОбучение основной модели...")
    main_model = build_main_model(input_shape=(224, 224, 3))
    main_history = main_model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=10,
        batch_size=32
    )
    
    # Оценка основной модели
    main_metrics = main_model.evaluate(X_val, y_val)
    print("\nМетрики основной модели:")
    print(f"MSE: {main_metrics[0]:.2f}")
    print(f"MAE: {main_metrics[1]:.2f}")
    
    # Сохранение моделей
    baseline_model.save('results/baseline_model')
    main_model.save('results/main_model')
    print("\nМодели сохранены в директории results/")

if __name__ == "__main__":
    asyncio.run(main())