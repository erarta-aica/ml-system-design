# Импортируем необходимые модули
from models.baseline_model import build_baseline_model
from models.main_model import build_main_model
from training.train import cross_validate_model
from data_processing.data_loader import FoodDataLoader
import asyncio
import tensorflow as tf
import numpy as np
import os

async def load_and_preprocess_data():
    """Загрузка и предобработка данных"""
    loader = FoodDataLoader()
    
    # Уменьшаем количество примеров и добавляем отладку
    result = await loader.load_dataset(num_examples=100)  # Уменьшили до 100
    print(f"\nТип возвращаемого значения: {type(result)}")
    if isinstance(result, tuple):
        print(f"Длина кортежа: {len(result)}")
    
    df, raw_images = result
    
    print("\nСтруктура датафрейма:")
    print(df.columns)
    print("\nКоличество изображений:", len(raw_images))
    print("\nПример данных:")
    print(df.head())
    
    # Предобработка изображений
    def preprocess_image(img):
        # Изменение размера и нормализация
        img = tf.image.resize(img, [224, 224])
        img = tf.cast(img, tf.float32) / 255.0
        return img

    # Подготовка данных
    print("\nПредобработка изображений...")
    images = np.array([preprocess_image(img) for img in raw_images])
    calories = df['calories'].values.astype(np.float32)
    
    print(f"\nРазмерность данных:")
    print(f"Изображения: {images.shape}")
    print(f"Калории: {calories.shape}")
    
    return images, calories

async def main():
    print("Загрузка и подготовка данных...")
    X, y = await load_and_preprocess_data()
    
    print(f"\nФорма входных данных:")
    print(f"X shape: {X.shape}")
    print(f"y shape: {y.shape}")
    
    # Разделение на обучающую и валидационную выборки
    train_size = int(0.8 * len(X))
    X_train, X_val = X[:train_size], X[train_size:]
    y_train, y_val = y[:train_size], y[train_size:]
    
    # Создаем callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=3,
            min_lr=1e-6,
            verbose=1
        ),
        tf.keras.callbacks.ModelCheckpoint(
            'results/best_model_{epoch:02d}.h5',
            monitor='val_loss',
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Создание и обучение бейзлайн модели
    print("\nОбучение базовой модели (бейзлайн)...")
    baseline_model = build_baseline_model(input_shape=(224, 224, 3))
    baseline_history = baseline_model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=30,  # Увеличили количество эпох
        batch_size=32,
        callbacks=callbacks,
        verbose=2
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
        epochs=30,  # Увеличили количество эпох
        batch_size=32,
        callbacks=callbacks,
        verbose=2
    )
    
    # Оценка основной модели
    main_metrics = main_model.evaluate(X_val, y_val)
    print("\nМетрики основной модели:")
    print(f"MSE: {main_metrics[0]:.2f}")
    print(f"MAE: {main_metrics[1]:.2f}")
    
    # Сохранение результатов обучения
    try:
        os.makedirs('results', exist_ok=True)
        
        # Сохраняем историю обучения
        history_data = {
            'baseline': {
                'loss': baseline_history.history['loss'],
                'val_loss': baseline_history.history['val_loss'],
                'mae': baseline_history.history['mae'],
                'val_mae': baseline_history.history['val_mae']
            },
            'main': {
                'loss': main_history.history['loss'],
                'val_loss': main_history.history['val_loss'],
                'mae': main_history.history['mae'],
                'val_mae': main_history.history['val_mae']
            }
        }
        
        import json
        with open('results/training_history.json', 'w') as f:
            json.dump(history_data, f)
        
        # Сохраняем веса моделей
        baseline_model.save_weights('results/baseline_weights.h5')
        main_model.save_weights('results/main_weights.h5')
        
        print("\nМодели и история обучения успешно сохранены в директории results/")
        
    except Exception as e:
        print(f"\nОшибка при сохранении результатов: {e}")
        print("Продолжаем выполнение...")
    
    # Выводим итоговые метрики
    print("\nИтоговые результаты:")
    print("Базовая модель (бейзлайн):")
    print(f"MSE: {baseline_metrics[0]:.2f}")
    print(f"MAE: {baseline_metrics[1]:.2f}")
    print("\nОсновная модель:")
    print(f"MSE: {main_metrics[0]:.2f}")
    print(f"MAE: {main_metrics[1]:.2f}")

if __name__ == "__main__":
    asyncio.run(main())