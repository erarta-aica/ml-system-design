import tensorflow as tf
from tensorflow.keras import layers, models

def build_baseline_model(input_shape):
    """
    Создает базовую модель (бейзлайн) для предсказания калорий.
    Простая CNN архитектура с регуляризацией.
    """
    model = models.Sequential([
        # Входной слой
        layers.Input(shape=input_shape),
        
        # Сверточные слои
        layers.Conv2D(32, (3, 3), activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        layers.MaxPooling2D((2, 2)),
        
        # Полносвязные слои
        layers.Flatten(),
        layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        layers.Dropout(0.5),
        layers.Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        layers.Dropout(0.3),
        layers.Dense(1)  # Выходной слой для предсказания калорий
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='mse',
        metrics=['mae']
    )
    
    return model
