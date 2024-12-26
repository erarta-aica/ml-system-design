import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Tuple, Dict

class FoodEDA:
    def __init__(self, df: pd.DataFrame):
        """
        Инициализация анализа
        
        Args:
            df (pd.DataFrame): Датафрейм с данными
        """
        self.df = df
        self.setup_style()
        
    @staticmethod
    def setup_style():
        """Настройка стиля графиков"""
        plt.style.use('seaborn')
        sns.set_palette("husl")
        
    def analyze_calorie_distribution(self) -> Dict:
        """
        Анализ распределения калорий
        
        Returns:
            Dict: Статистические показатели
        """
        stats_dict = {
            'mean': self.df['calories'].mean(),
            'median': self.df['calories'].median(),
            'std': self.df['calories'].std(),
            'min': self.df['calories'].min(),
            'max': self.df['calories'].max()
        }
        
        # Создание визуализаций
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Гистограмма
        sns.histplot(data=self.df, x='calories', bins=30, ax=axes[0,0])
        axes[0,0].set_title('Распределение калорий')
        
        # Box plot
        sns.boxplot(data=self.df, x='category', y='calories', ax=axes[0,1])
        axes[0,1].set_title('Калории по категориям')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # QQ plot
        stats.probplot(self.df['calories'], dist="norm", plot=axes[1,0])
        axes[1,0].set_title('Q-Q график калорий')
        
        # Violin plot
        sns.violinplot(data=self.df, x='category', y='calories', ax=axes[1,1])
        axes[1,1].set_title('Violin plot калорий по категориям')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
        
        return stats_dict
    
    def analyze_image_properties(self) -> Dict:
        """
        Анализ характеристик изображений
        
        Returns:
            Dict: Статистика характеристик
        """
        feature_stats = {}
        for feature in ['width', 'height', 'aspect_ratio', 'brightness', 'saturation']:
            feature_stats[feature] = {
                'mean': self.df[feature].mean(),
                'std': self.df[feature].std(),
                'min': self.df[feature].min(),
                'max': self.df[feature].max()
            }
            
        # Создание визуализаций
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Scatter plot размеров
        sns.scatterplot(data=self.df, x='width', y='height', 
                       hue='category', alpha=0.5, ax=axes[0,0])
        axes[0,0].set_title('Размеры изображений')
        
        # Гистограмма соотношения сторон
        sns.histplot(data=self.df, x='aspect_ratio', bins=30, ax=axes[0,1])
        axes[0,1].set_title('Распределение соотношения сторон')
        
        # Корреляционная матрица
        corr_matrix = self.df[['calories', 'brightness', 'saturation', 'aspect_ratio']].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=axes[1,0])
        axes[1,0].set_title('Корреляционная матрица')
        
        # Scatter plot калории vs яркость
        sns.scatterplot(data=self.df, x='brightness', y='calories', 
                       hue='category', alpha=0.5, ax=axes[1,1])
        axes[1,1].set_title('Калории vs Яркость')
        
        plt.tight_layout()
        plt.show()
        
        return feature_stats
