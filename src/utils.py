"""
Вспомогательные функции для анализа данных
AI Assistant Functionality Test
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Any

def create_sample_data(num_records: int = 1000) -> List[Dict[str, Any]]:
    """
    Создает тестовые данные для анализа
    
    Args:
        num_records: количество записей для генерации
        
    Returns:
        List[Dict]: список записей с данными о продажах
    """
    # Настройка для воспроизводимости
    random.seed(42)
    np.random.seed(42)
    
    # Базовые данные
    products = ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse', 'Headphones', 'Speaker']
    regions = ['North', 'South', 'East', 'West', 'Central']
    categories = ['Electronics', 'Accessories', 'Computing', 'Audio']
    
    data = []
    base_date = datetime(2023, 1, 1)
    
    for i in range(num_records):
        # Генерируем случайную дату
        days_offset = random.randint(0, 365)
        record_date = base_date + timedelta(days=days_offset)
        
        # Генерируем остальные данные
        product = random.choice(products)
        region = random.choice(regions)
        category = random.choice(categories)
        
        # Цена зависит от продукта
        price_ranges = {
            'Laptop': (800, 2000),
            'Phone': (300, 1200),
            'Tablet': (200, 800),
            'Monitor': (150, 500),
            'Keyboard': (20, 150),
            'Mouse': (10, 100),
            'Headphones': (50, 300),
            'Speaker': (30, 200)
        }
        
        min_price, max_price = price_ranges.get(product, (50, 500))
        price = round(random.uniform(min_price, max_price), 2)
        
        # Количество
        quantity = random.randint(1, 20)
        
        # Общая сумма продаж
        sales = price * quantity
        
        # Добавляем сезонность (больше продаж в конце года)
        if record_date.month in [11, 12]:
            sales *= random.uniform(1.1, 1.5)
        
        # Добавляем запись
        data.append({
            'date': record_date,
            'product': product,
            'category': category,
            'region': region,
            'price': price,
            'quantity': quantity,
            'sales': round(sales, 2),
            'customer_id': f'C{i:04d}'
        })
    
    return data

def statistical_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Создает статистическую сводку данных
    
    Args:
        df: DataFrame с данными
        
    Returns:
        Dict: словарь со статистикой
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    summary = {
        'total_records': len(df),
        'date_range': {
            'start': df['date'].min().strftime('%Y-%m-%d') if 'date' in df.columns else 'N/A',
            'end': df['date'].max().strftime('%Y-%m-%d') if 'date' in df.columns else 'N/A'
        },
        'numeric_summary': {}
    }
    
    for col in numeric_cols:
        summary['numeric_summary'][col] = {
            'mean': round(df[col].mean(), 2),
            'median': round(df[col].median(), 2),
            'std': round(df[col].std(), 2),
            'min': round(df[col].min(), 2),
            'max': round(df[col].max(), 2),
            'total': round(df[col].sum(), 2) if col in ['sales', 'quantity'] else None
        }
    
    # Категориальные переменные
    categorical_cols = df.select_dtypes(include=['object']).columns
    summary['categorical_summary'] = {}
    
    for col in categorical_cols:
        if col != 'date':
            summary['categorical_summary'][col] = {
                'unique_values': df[col].nunique(),
                'top_values': df[col].value_counts().head(3).to_dict()
            }
    
    return summary

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Очищает данные от пропусков и аномалий
    
    Args:
        df: исходный DataFrame
        
    Returns:
        pd.DataFrame: очищенный DataFrame
    """
    # Копируем DataFrame
    cleaned_df = df.copy()
    
    # Удаляем дубликаты
    cleaned_df = cleaned_df.drop_duplicates()
    
    # Обрабатываем пропущенные значения
    if 'sales' in cleaned_df.columns:
        # Заменяем отрицательные продажи на 0
        cleaned_df.loc[cleaned_df['sales'] < 0, 'sales'] = 0
        
        # Удаляем аномально большие значения (выше 99-го перцентиля)
        sales_99th = cleaned_df['sales'].quantile(0.99)
        cleaned_df = cleaned_df[cleaned_df['sales'] <= sales_99th]
    
    # Обрабатываем даты
    if 'date' in cleaned_df.columns:
        cleaned_df['date'] = pd.to_datetime(cleaned_df['date'])
    
    return cleaned_df

def calculate_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Вычисляет бизнес-метрики
    
    Args:
        df: DataFrame с данными
        
    Returns:
        Dict: словарь с метриками
    """
    metrics = {}
    
    if 'sales' in df.columns:
        metrics['total_revenue'] = df['sales'].sum()
        metrics['average_order_value'] = df['sales'].mean()
        metrics['median_order_value'] = df['sales'].median()
    
    if 'quantity' in df.columns:
        metrics['total_items_sold'] = df['quantity'].sum()
        metrics['average_items_per_order'] = df['quantity'].mean()
    
    if 'customer_id' in df.columns:
        metrics['unique_customers'] = df['customer_id'].nunique()
        metrics['orders_per_customer'] = len(df) / df['customer_id'].nunique()
    
    if 'product' in df.columns:
        metrics['unique_products'] = df['product'].nunique()
    
    # Конверсия и другие метрики
    if 'date' in df.columns:
        # Продажи по дням
        daily_sales = df.groupby(df['date'].dt.date)['sales'].sum()
        metrics['best_day_sales'] = daily_sales.max()
        metrics['worst_day_sales'] = daily_sales.min()
        metrics['average_daily_sales'] = daily_sales.mean()
    
    return {k: round(v, 2) for k, v in metrics.items()}

def export_to_csv(df: pd.DataFrame, filename: str = 'processed_data.csv'):
    """
    Экспортирует данные в CSV файл
    
    Args:
        df: DataFrame для экспорта
        filename: имя файла
    """
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"📁 Данные экспортированы в {filename}")

def validate_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Валидирует данные и возвращает отчет о качестве
    
    Args:
        df: DataFrame для валидации
        
    Returns:
        Dict: отчет о качестве данных
    """
    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'data_types': df.dtypes.astype(str).to_dict(),
        'duplicates': df.duplicated().sum(),
        'memory_usage': df.memory_usage(deep=True).sum(),
        'issues': []
    }
    
    # Проверяем проблемы
    if df.isnull().sum().sum() > 0:
        report['issues'].append('Найдены пропущенные значения')
    
    if df.duplicated().sum() > 0:
        report['issues'].append('Найдены дубликаты')
    
    # Проверяем числовые столбцы на аномалии
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if col in df.columns:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            if len(outliers) > 0:
                report['issues'].append(f'Найдены выбросы в столбце {col}: {len(outliers)} значений')
    
    return report