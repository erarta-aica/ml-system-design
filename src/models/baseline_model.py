import tensorflow as tf
from tensorflow.keras import layers, models

def build_baseline_model(input_shape):
    """
    Создает базовую модель (бейзлайн) для предсказания калорий.
    Простая CNN архитектура.
    """
    model = models.Sequential([
        # Входной слой
        layers.Input(shape=input_shape),
        
        # Сверточные слои
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Полносвязные слои
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1)  # Выходной слой для предсказания калорий
    ])
    
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    
    return model
