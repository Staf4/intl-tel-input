"""
Тесты для вспомогательных функций
AI Assistant Functionality Test
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import (
    create_sample_data,
    statistical_summary,
    clean_data,
    calculate_metrics,
    validate_data
)


class TestCreateSampleData:
    """Тесты для функции create_sample_data"""
    
    def test_default_sample_size(self):
        """Тест создания данных с размером по умолчанию"""
        data = create_sample_data()
        assert len(data) == 1000
        
    def test_custom_sample_size(self):
        """Тест создания данных с кастомным размером"""
        data = create_sample_data(num_records=100)
        assert len(data) == 100
        
    def test_data_structure(self):
        """Тест структуры созданных данных"""
        data = create_sample_data(num_records=10)
        
        # Проверяем, что все записи имеют нужные поля
        required_fields = ['date', 'product', 'category', 'region', 'price', 'quantity', 'sales', 'customer_id']
        for record in data:
            for field in required_fields:
                assert field in record
                
    def test_data_types(self):
        """Тест типов данных"""
        data = create_sample_data(num_records=10)
        
        for record in data:
            assert isinstance(record['date'], datetime)
            assert isinstance(record['product'], str)
            assert isinstance(record['category'], str)
            assert isinstance(record['region'], str)
            assert isinstance(record['price'], (int, float))
            assert isinstance(record['quantity'], int)
            assert isinstance(record['sales'], (int, float))
            assert isinstance(record['customer_id'], str)
            
    def test_sales_calculation(self):
        """Тест корректности расчета продаж"""
        data = create_sample_data(num_records=10)
        
        for record in data:
            # Проверяем, что sales приблизительно равны price * quantity
            # (с учетом сезонности может быть немного больше)
            base_sales = record['price'] * record['quantity']
            assert record['sales'] >= base_sales
            assert record['sales'] <= base_sales * 1.5  # максимальная сезонность
            
    def test_date_range(self):
        """Тест диапазона дат"""
        data = create_sample_data(num_records=100)
        
        base_date = datetime(2023, 1, 1)
        end_date = base_date + timedelta(days=365)
        
        for record in data:
            assert base_date <= record['date'] <= end_date


class TestStatisticalSummary:
    """Тесты для функции statistical_summary"""
    
    @pytest.fixture
    def sample_df(self):
        """Создает тестовый DataFrame"""
        data = create_sample_data(num_records=100)
        return pd.DataFrame(data)
    
    def test_summary_structure(self, sample_df):
        """Тест структуры статистической сводки"""
        summary = statistical_summary(sample_df)
        
        assert 'total_records' in summary
        assert 'date_range' in summary
        assert 'numeric_summary' in summary
        assert 'categorical_summary' in summary
        
    def test_record_count(self, sample_df):
        """Тест подсчета записей"""
        summary = statistical_summary(sample_df)
        assert summary['total_records'] == len(sample_df)
        
    def test_numeric_summary(self, sample_df):
        """Тест числовой статистики"""
        summary = statistical_summary(sample_df)
        
        # Проверяем, что есть статистика для числовых колонок
        assert 'price' in summary['numeric_summary']
        assert 'quantity' in summary['numeric_summary']
        assert 'sales' in summary['numeric_summary']
        
        # Проверяем наличие всех статистических показателей
        price_stats = summary['numeric_summary']['price']
        required_stats = ['mean', 'median', 'std', 'min', 'max']
        for stat in required_stats:
            assert stat in price_stats
            
    def test_categorical_summary(self, sample_df):
        """Тест категориальной статистики"""
        summary = statistical_summary(sample_df)
        
        # Проверяем, что есть статистика для категориальных колонок
        assert 'product' in summary['categorical_summary']
        assert 'region' in summary['categorical_summary']
        
        # Проверяем структуру
        product_stats = summary['categorical_summary']['product']
        assert 'unique_values' in product_stats
        assert 'top_values' in product_stats


class TestCleanData:
    """Тесты для функции clean_data"""
    
    def test_duplicate_removal(self):
        """Тест удаления дубликатов"""
        # Создаем DataFrame с дубликатами
        data = [
            {'date': datetime(2023, 1, 1), 'product': 'A', 'sales': 100},
            {'date': datetime(2023, 1, 1), 'product': 'A', 'sales': 100},  # дубликат
            {'date': datetime(2023, 1, 2), 'product': 'B', 'sales': 200}
        ]
        df = pd.DataFrame(data)
        
        cleaned_df = clean_data(df)
        assert len(cleaned_df) == 2  # дубликат должен быть удален
        
    def test_negative_sales_handling(self):
        """Тест обработки отрицательных продаж"""
        data = [
            {'date': datetime(2023, 1, 1), 'product': 'A', 'sales': -100},
            {'date': datetime(2023, 1, 2), 'product': 'B', 'sales': 200}
        ]
        df = pd.DataFrame(data)
        
        cleaned_df = clean_data(df)
        assert (cleaned_df['sales'] >= 0).all()
        
    def test_date_conversion(self):
        """Тест конверсии дат"""
        data = [
            {'date': '2023-01-01', 'product': 'A', 'sales': 100},
            {'date': '2023-01-02', 'product': 'B', 'sales': 200}
        ]
        df = pd.DataFrame(data)
        
        cleaned_df = clean_data(df)
        assert pd.api.types.is_datetime64_any_dtype(cleaned_df['date'])


class TestCalculateMetrics:
    """Тесты для функции calculate_metrics"""
    
    @pytest.fixture
    def sample_df(self):
        """Создает тестовый DataFrame"""
        data = create_sample_data(num_records=50)
        return pd.DataFrame(data)
    
    def test_revenue_metrics(self, sample_df):
        """Тест метрик дохода"""
        metrics = calculate_metrics(sample_df)
        
        assert 'total_revenue' in metrics
        assert 'average_order_value' in metrics
        assert 'median_order_value' in metrics
        
        # Проверяем корректность расчетов
        assert metrics['total_revenue'] == round(sample_df['sales'].sum(), 2)
        assert metrics['average_order_value'] == round(sample_df['sales'].mean(), 2)
        
    def test_quantity_metrics(self, sample_df):
        """Тест метрик количества"""
        metrics = calculate_metrics(sample_df)
        
        assert 'total_items_sold' in metrics
        assert 'average_items_per_order' in metrics
        
        assert metrics['total_items_sold'] == sample_df['quantity'].sum()
        
    def test_customer_metrics(self, sample_df):
        """Тест метрик клиентов"""
        metrics = calculate_metrics(sample_df)
        
        assert 'unique_customers' in metrics
        assert 'orders_per_customer' in metrics
        
        assert metrics['unique_customers'] == sample_df['customer_id'].nunique()
        
    def test_product_metrics(self, sample_df):
        """Тест метрик продуктов"""
        metrics = calculate_metrics(sample_df)
        
        assert 'unique_products' in metrics
        assert metrics['unique_products'] == sample_df['product'].nunique()


class TestValidateData:
    """Тесты для функции validate_data"""
    
    def test_basic_validation(self):
        """Тест базовой валидации"""
        data = create_sample_data(num_records=20)
        df = pd.DataFrame(data)
        
        report = validate_data(df)
        
        # Проверяем структуру отчета
        assert 'total_rows' in report
        assert 'total_columns' in report
        assert 'missing_values' in report
        assert 'data_types' in report
        assert 'duplicates' in report
        assert 'memory_usage' in report
        assert 'issues' in report
        
    def test_missing_values_detection(self):
        """Тест обнаружения пропущенных значений"""
        data = [
            {'date': datetime(2023, 1, 1), 'product': 'A', 'sales': 100},
            {'date': datetime(2023, 1, 2), 'product': None, 'sales': 200}
        ]
        df = pd.DataFrame(data)
        
        report = validate_data(df)
        
        # Должны быть обнаружены пропущенные значения
        assert 'Найдены пропущенные значения' in report['issues']
        assert report['missing_values']['product'] == 1
        
    def test_duplicates_detection(self):
        """Тест обнаружения дубликатов"""
        data = [
            {'date': datetime(2023, 1, 1), 'product': 'A', 'sales': 100},
            {'date': datetime(2023, 1, 1), 'product': 'A', 'sales': 100}  # дубликат
        ]
        df = pd.DataFrame(data)
        
        report = validate_data(df)
        
        # Должны быть обнаружены дубликаты
        assert 'Найдены дубликаты' in report['issues']
        assert report['duplicates'] == 1
        
    def test_outliers_detection(self):
        """Тест обнаружения выбросов"""
        # Создаем данные с явными выбросами
        data = [100, 200, 150, 180, 120, 10000]  # 10000 - выброс
        df = pd.DataFrame({'sales': data})
        
        report = validate_data(df)
        
        # Должны быть обнаружены выбросы
        outlier_issues = [issue for issue in report['issues'] if 'выбросы' in issue]
        assert len(outlier_issues) > 0


class TestIntegration:
    """Интеграционные тесты"""
    
    def test_full_pipeline(self):
        """Тест полного пайплайна обработки данных"""
        # Создаем данные
        data = create_sample_data(num_records=100)
        df = pd.DataFrame(data)
        
        # Получаем статистику
        summary = statistical_summary(df)
        
        # Очищаем данные
        clean_df = clean_data(df)
        
        # Вычисляем метрики
        metrics = calculate_metrics(clean_df)
        
        # Валидируем данные
        report = validate_data(clean_df)
        
        # Проверяем, что все операции прошли успешно
        assert summary['total_records'] == 100
        assert len(clean_df) <= 100  # может быть меньше из-за очистки
        assert len(metrics) > 0
        assert report['total_rows'] == len(clean_df)
        
    def test_empty_dataframe(self):
        """Тест обработки пустого DataFrame"""
        df = pd.DataFrame()
        
        # Все функции должны корректно обрабатывать пустой DataFrame
        summary = statistical_summary(df)
        clean_df = clean_data(df)
        metrics = calculate_metrics(df)
        report = validate_data(df)
        
        assert summary['total_records'] == 0
        assert len(clean_df) == 0
        assert len(metrics) == 0
        assert report['total_rows'] == 0


# Запуск тестов
if __name__ == "__main__":
    pytest.main([__file__, "-v"])