import asyncio
import os
import pandas as pd
from data_processing.data_loader import FoodDataLoader
from analysis.eda import FoodEDA

async def main():
    # Инициализация загрузчика данных
    loader = FoodDataLoader()
    
    # Загрузка данных
    print("Начинаем загрузку и обработку данных...")
    df = await loader.load_dataset(num_examples=1000)  # Загружаем 1000 примеров
    
    # Вывод базовой информации
    print("\nОбщая информация о датасете:")
    print(f"Количество образцов: {len(df)}")
    print(f"Количество категорий: {df['category'].nunique()}")
    print("\nРаспределение по категориям:")
    print(df['category'].value_counts())
    
    # Создание объекта для анализа
    eda = FoodEDA(df)
    
    # Проведение анализа
    print("\nАнализ распределения калорий...")
    calorie_stats = eda.analyze_calorie_distribution()
    
    print("\nСтатистика по калориям:")
    for key, value in calorie_stats.items():
        print(f"{key}: {value:.2f}")
    
    print("\nАнализ характеристик изображений...")
    image_stats = eda.analyze_image_properties()
    
    # Сохранение результатов
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    
    # Сохранение датафрейма
    df.to_csv(os.path.join(results_dir, 'food_data.csv'), index=False)
    print(f"\nДанные сохранены в {os.path.join(results_dir, 'food_data.csv')}")

if __name__ == "__main__":
    asyncio.run(main())
