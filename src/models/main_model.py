import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50V2

def build_main_model(input_shape):
    """
    Создает основную модель на базе ResNet50V2 для предсказания калорий
    """
    # Загружаем предобученную ResNet50V2 без верхних слоев
    base_model = ResNet50V2(
        include_top=False,
        weights='imagenet',
        input_shape=input_shape
    )
    
    # Замораживаем веса базовой модели
    base_model.trainable = False
    
    model = models.Sequential([
        # Базовая модель
        base_model,
        
        # Добавляем свои слои
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.Dense(1)  # Выходной слой для предсказания калорий
    ])
    
    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )
    
    return model
