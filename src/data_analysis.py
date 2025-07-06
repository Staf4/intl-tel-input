#!/usr/bin/env python3
"""
Демонстрация анализа данных с использованием Python
AI Assistant Functionality Test
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os
from utils import create_sample_data, statistical_summary

def analyze_sales_data():
    """Анализ данных о продажах"""
    print("🚀 Начинаем анализ данных о продажах...")
    
    # Создаем тестовые данные
    data = create_sample_data()
    df = pd.DataFrame(data)
    
    print(f"📊 Загружено {len(df)} записей")
    print(f"📅 Период данных: {df['date'].min()} - {df['date'].max()}")
    
    # Базовая статистика
    print("\n📈 Базовая статистика:")
    print(statistical_summary(df))
    
    # Визуализация
    create_visualizations(df)
    
    # Анализ трендов
    analyze_trends(df)
    
    return df

def create_visualizations(df):
    """Создание графиков и визуализаций"""
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # График продаж по времени
    df_monthly = df.groupby(df['date'].dt.to_period('M'))['sales'].sum()
    axes[0, 0].plot(df_monthly.index.astype(str), df_monthly.values, marker='o')
    axes[0, 0].set_title('Продажи по месяцам')
    axes[0, 0].set_xlabel('Месяц')
    axes[0, 0].set_ylabel('Продажи')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Распределение по регионам
    region_sales = df.groupby('region')['sales'].sum()
    axes[0, 1].bar(region_sales.index, region_sales.values)
    axes[0, 1].set_title('Продажи по регионам')
    axes[0, 1].set_xlabel('Регион')
    axes[0, 1].set_ylabel('Продажи')
    
    # Корреляция между количеством и ценой
    axes[1, 0].scatter(df['quantity'], df['price'], alpha=0.6)
    axes[1, 0].set_title('Корреляция: Количество vs Цена')
    axes[1, 0].set_xlabel('Количество')
    axes[1, 0].set_ylabel('Цена')
    
    # Гистограмма продаж
    axes[1, 1].hist(df['sales'], bins=30, alpha=0.7, color='skyblue')
    axes[1, 1].set_title('Распределение продаж')
    axes[1, 1].set_xlabel('Продажи')
    axes[1, 1].set_ylabel('Частота')
    
    plt.tight_layout()
    plt.savefig('sales_analysis.png', dpi=300, bbox_inches='tight')
    print("📊 Графики сохранены в sales_analysis.png")

def analyze_trends(df):
    """Анализ трендов и паттернов"""
    print("\n🔍 Анализ трендов:")
    
    # Топ продукты
    top_products = df.groupby('product')['sales'].sum().sort_values(ascending=False).head(5)
    print("🏆 Топ-5 продуктов по продажам:")
    for product, sales in top_products.items():
        print(f"   {product}: ${sales:,.2f}")
    
    # Сезонность
    seasonal_data = df.groupby(df['date'].dt.month)['sales'].mean()
    peak_month = seasonal_data.idxmax()
    print(f"\n📅 Пиковый месяц: {peak_month} (средние продажи: ${seasonal_data[peak_month]:,.2f})")
    
    # Рост по сравнению с предыдущим периодом
    df_sorted = df.sort_values('date')
    recent_sales = df_sorted.tail(30)['sales'].sum()
    previous_sales = df_sorted.head(30)['sales'].sum()
    growth_rate = ((recent_sales - previous_sales) / previous_sales) * 100
    print(f"📈 Рост продаж: {growth_rate:.1f}%")

def export_results(df):
    """Экспорт результатов анализа"""
    # Создаем отчет
    report = {
        'summary': {
            'total_records': len(df),
            'total_sales': float(df['sales'].sum()),
            'average_sales': float(df['sales'].mean()),
            'date_range': {
                'start': df['date'].min().strftime('%Y-%m-%d'),
                'end': df['date'].max().strftime('%Y-%m-%d')
            }
        },
        'top_products': df.groupby('product')['sales'].sum().sort_values(ascending=False).head(10).to_dict(),
        'regional_breakdown': df.groupby('region')['sales'].sum().to_dict(),
        'generated_at': datetime.now().isoformat()
    }
    
    # Сохраняем в JSON
    with open('analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("📄 Отчет сохранен в analysis_report.json")

def main():
    """Основная функция"""
    print("🤖 AI Assistant - Демонстрация анализа данных")
    print("=" * 50)
    
    try:
        # Выполняем анализ
        df = analyze_sales_data()
        
        # Экспортируем результаты
        export_results(df)
        
        print("\n✅ Анализ завершен успешно!")
        print("📁 Результаты:")
        print("   - sales_analysis.png (графики)")
        print("   - analysis_report.json (отчет)")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        raise

if __name__ == "__main__":
    main()