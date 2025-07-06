/**
 * Веб-компоненты для интерактивной визуализации данных
 * AI Assistant Functionality Test
 */

class DataVisualization {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.data = null;
        this.charts = {};
        this.init();
    }

    init() {
        this.createLayout();
        this.bindEvents();
        this.loadSampleData();
    }

    createLayout() {
        this.container.innerHTML = `
            <div class="dashboard">
                <header class="dashboard-header">
                    <h1>🤖 AI Assistant - Демонстрация веб-компонентов</h1>
                    <div class="controls">
                        <button id="refreshData" class="btn btn-primary">🔄 Обновить данные</button>
                        <button id="exportData" class="btn btn-secondary">📥 Экспорт</button>
                    </div>
                </header>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>Общий доход</h3>
                        <div class="stat-value" id="totalRevenue">$0</div>
                    </div>
                    <div class="stat-card">
                        <h3>Количество заказов</h3>
                        <div class="stat-value" id="totalOrders">0</div>
                    </div>
                    <div class="stat-card">
                        <h3>Средний чек</h3>
                        <div class="stat-value" id="avgOrderValue">$0</div>
                    </div>
                    <div class="stat-card">
                        <h3>Товаров продано</h3>
                        <div class="stat-value" id="totalItems">0</div>
                    </div>
                </div>
                
                <div class="charts-grid">
                    <div class="chart-container">
                        <h3>Продажи по месяцам</h3>
                        <canvas id="salesChart"></canvas>
                    </div>
                    <div class="chart-container">
                        <h3>Продажи по регионам</h3>
                        <canvas id="regionChart"></canvas>
                    </div>
                    <div class="chart-container">
                        <h3>Топ продукты</h3>
                        <canvas id="productChart"></canvas>
                    </div>
                    <div class="chart-container">
                        <h3>Тренд продаж</h3>
                        <canvas id="trendChart"></canvas>
                    </div>
                </div>
                
                <div class="data-table-container">
                    <h3>Таблица данных</h3>
                    <div class="table-controls">
                        <input type="text" id="searchInput" placeholder="Поиск..." class="search-input">
                        <select id="filterRegion" class="filter-select">
                            <option value="">Все регионы</option>
                        </select>
                    </div>
                    <div class="table-wrapper">
                        <table id="dataTable" class="data-table">
                            <thead>
                                <tr>
                                    <th>Дата</th>
                                    <th>Продукт</th>
                                    <th>Регион</th>
                                    <th>Цена</th>
                                    <th>Количество</th>
                                    <th>Сумма</th>
                                </tr>
                            </thead>
                            <tbody></tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
    }

    bindEvents() {
        document.getElementById('refreshData').addEventListener('click', () => {
            this.loadSampleData();
        });

        document.getElementById('exportData').addEventListener('click', () => {
            this.exportToJSON();
        });

        document.getElementById('searchInput').addEventListener('input', (e) => {
            this.filterTable(e.target.value);
        });

        document.getElementById('filterRegion').addEventListener('change', (e) => {
            this.filterByRegion(e.target.value);
        });
    }

    async loadSampleData() {
        // Симулируем загрузку данных
        this.showLoading();
        
        // Генерируем тестовые данные
        this.data = this.generateSampleData();
        
        // Обновляем интерфейс
        this.updateStats();
        this.updateCharts();
        this.updateTable();
        this.populateFilters();
        
        this.hideLoading();
    }

    generateSampleData() {
        const products = ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse'];
        const regions = ['North', 'South', 'East', 'West', 'Central'];
        const data = [];
        
        for (let i = 0; i < 100; i++) {
            const product = products[Math.floor(Math.random() * products.length)];
            const region = regions[Math.floor(Math.random() * regions.length)];
            const price = Math.floor(Math.random() * 1000) + 50;
            const quantity = Math.floor(Math.random() * 10) + 1;
            const date = new Date();
            date.setDate(date.getDate() - Math.floor(Math.random() * 365));
            
            data.push({
                id: i + 1,
                date: date,
                product: product,
                region: region,
                price: price,
                quantity: quantity,
                sales: price * quantity
            });
        }
        
        return data;
    }

    updateStats() {
        const totalRevenue = this.data.reduce((sum, item) => sum + item.sales, 0);
        const totalOrders = this.data.length;
        const avgOrderValue = totalRevenue / totalOrders;
        const totalItems = this.data.reduce((sum, item) => sum + item.quantity, 0);
        
        document.getElementById('totalRevenue').textContent = `$${totalRevenue.toLocaleString()}`;
        document.getElementById('totalOrders').textContent = totalOrders.toLocaleString();
        document.getElementById('avgOrderValue').textContent = `$${avgOrderValue.toFixed(2)}`;
        document.getElementById('totalItems').textContent = totalItems.toLocaleString();
    }

    updateCharts() {
        this.createSalesChart();
        this.createRegionChart();
        this.createProductChart();
        this.createTrendChart();
    }

    createSalesChart() {
        const ctx = document.getElementById('salesChart').getContext('2d');
        
        // Группировка по месяцам
        const monthlyData = {};
        this.data.forEach(item => {
            const month = item.date.toISOString().slice(0, 7);
            monthlyData[month] = (monthlyData[month] || 0) + item.sales;
        });
        
        const labels = Object.keys(monthlyData).sort();
        const data = labels.map(month => monthlyData[month]);
        
        if (this.charts.sales) {
            this.charts.sales.destroy();
        }
        
        this.charts.sales = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Продажи',
                    data: data,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    createRegionChart() {
        const ctx = document.getElementById('regionChart').getContext('2d');
        
        const regionData = {};
        this.data.forEach(item => {
            regionData[item.region] = (regionData[item.region] || 0) + item.sales;
        });
        
        if (this.charts.region) {
            this.charts.region.destroy();
        }
        
        this.charts.region = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(regionData),
                datasets: [{
                    data: Object.values(regionData),
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    createProductChart() {
        const ctx = document.getElementById('productChart').getContext('2d');
        
        const productData = {};
        this.data.forEach(item => {
            productData[item.product] = (productData[item.product] || 0) + item.sales;
        });
        
        const sortedProducts = Object.entries(productData)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 6);
        
        if (this.charts.product) {
            this.charts.product.destroy();
        }
        
        this.charts.product = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: sortedProducts.map(item => item[0]),
                datasets: [{
                    label: 'Продажи',
                    data: sortedProducts.map(item => item[1]),
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    createTrendChart() {
        const ctx = document.getElementById('trendChart').getContext('2d');
        
        // Группировка по дням
        const dailyData = {};
        this.data.forEach(item => {
            const day = item.date.toISOString().slice(0, 10);
            dailyData[day] = (dailyData[day] || 0) + item.sales;
        });
        
        const labels = Object.keys(dailyData).sort();
        const data = labels.map(day => dailyData[day]);
        
        if (this.charts.trend) {
            this.charts.trend.destroy();
        }
        
        this.charts.trend = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Дневные продажи',
                    data: data,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    updateTable() {
        const tbody = document.querySelector('#dataTable tbody');
        tbody.innerHTML = '';
        
        this.data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.date.toLocaleDateString()}</td>
                <td>${item.product}</td>
                <td>${item.region}</td>
                <td>$${item.price.toFixed(2)}</td>
                <td>${item.quantity}</td>
                <td>$${item.sales.toFixed(2)}</td>
            `;
            tbody.appendChild(row);
        });
    }

    populateFilters() {
        const regionSelect = document.getElementById('filterRegion');
        const regions = [...new Set(this.data.map(item => item.region))];
        
        regionSelect.innerHTML = '<option value="">Все регионы</option>';
        regions.forEach(region => {
            const option = document.createElement('option');
            option.value = region;
            option.textContent = region;
            regionSelect.appendChild(option);
        });
    }

    filterTable(searchTerm) {
        const rows = document.querySelectorAll('#dataTable tbody tr');
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm.toLowerCase()) ? '' : 'none';
        });
    }

    filterByRegion(region) {
        const rows = document.querySelectorAll('#dataTable tbody tr');
        rows.forEach(row => {
            const regionCell = row.cells[2].textContent;
            row.style.display = (!region || regionCell === region) ? '' : 'none';
        });
    }

    exportToJSON() {
        const dataStr = JSON.stringify(this.data, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = 'sales_data.json';
        link.click();
        
        URL.revokeObjectURL(url);
    }

    showLoading() {
        const overlay = document.createElement('div');
        overlay.id = 'loadingOverlay';
        overlay.innerHTML = `
            <div class="loading-content">
                <div class="spinner"></div>
                <p>Загрузка данных...</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.remove();
        }
    }
}

// Инициализация компонента при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new DataVisualization('app');
});

// Утилитарные функции
const Utils = {
    formatCurrency: (amount) => {
        return new Intl.NumberFormat('ru-RU', {
            style: 'currency',
            currency: 'RUB'
        }).format(amount);
    },

    formatDate: (date) => {
        return date.toLocaleDateString('ru-RU');
    },

    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};