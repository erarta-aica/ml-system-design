# Импортируем необходимые модули
from models.baseline_model import build_baseline_model
from models.main_model import build_main_model
from training.train import cross_validate_model
from data_processing.data_loader import FoodDataLoader
import asyncio

# Функция для загрузки данных
async def load_data():
    loader = FoodDataLoader()
    df = await loader.load_dataset(num_examples=1000)  # Загрузите 1000 примеров
    # Преобразуем данные в формат, подходящий для обучения
    data = df.drop(columns=['category']).values
    labels = df['category'].values
    return data, labels

# Основная функция для запуска обучения
async def main():
    # Загрузка данных
    data, labels = await load_data()

    # Создание и обучение бейзлайн модели
    baseline_model = build_baseline_model(input_shape=(224, 224, 3), num_classes=101)
    cross_validate_model(baseline_model, data, labels)

    # Создание и обучение основной модели
    main_model = build_main_model(input_shape=(224, 224, 3), num_classes=101)
    cross_validate_model(main_model, data, labels)

# Запуск основной функции
asyncio.run(main())