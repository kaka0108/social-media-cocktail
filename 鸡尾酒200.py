"""
菠萝汁鸡尾酒大全 - Flask应用
"""

from flask import Flask, render_template, jsonify, request
import json
import random
import os

app = Flask(__name__)

# 确保目录存在
os.makedirs('data', exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('static/images', exist_ok=True)


def create_html_template():
    """创建HTML模板文件"""
    html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>菠萝汁鸡尾酒大全 | 200+种配方</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar">
        <div class="container">
            <div class="logo">
                <i class="fas fa-cocktail"></i>
                <span>菠萝鸡尾酒大全</span>
            </div>
            <div class="nav-stats">
                <span><i class="fas fa-wine-glass-alt"></i> <span id="totalCount">200+</span> 配方</span>
            </div>
        </div>
    </nav>

    <!-- 英雄区域 -->
    <header class="hero">
        <div class="container">
            <div class="hero-content">
                <h1>探索200+种菠萝汁鸡尾酒</h1>
                <p class="subtitle">从经典到创意，发现菠萝的无限可能</p>
                <div class="hero-stats">
                    <div class="stat-card">
                        <i class="fas fa-clock"></i>
                        <div>
                            <span>快速制作</span>
                            <small>平均5分钟</small>
                        </div>
                    </div>
                    <div class="stat-card">
                        <i class="fas fa-leaf"></i>
                        <div>
                            <span>新鲜原料</span>
                            <small>100%天然</small>
                        </div>
                    </div>
                    <div class="stat-card">
                        <i class="fas fa-globe"></i>
                        <div>
                            <span>全球风味</span>
                            <small>30+国家</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- 搜索区域 -->
    <section class="search-section">
        <div class="container">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="搜索鸡尾酒名称或配料...">
                <button id="searchBtn"><i class="fas fa-search"></i> 搜索</button>
            </div>
            <div class="filter-tags" id="filterTags">
                <button class="filter-tag active" data-category="">全部</button>
                <!-- 分类将通过JavaScript动态加载 -->
            </div>
        </div>
    </section>

    <!-- 鸡尾酒展示 -->
    <main class="container">
        <section class="cocktails-section">
            <div class="section-header">
                <h2><i class="fas fa-pineapple"></i> 精选鸡尾酒</h2>
                <div class="view-controls">
                    <select id="sortSelect">
                        <option value="rating">评分最高</option>
                        <option value="name">名称排序</option>
                        <option value="difficulty">制作难度</option>
                    </select>
                </div>
            </div>

            <div id="cocktailsContainer" class="cocktails-grid">
                <!-- 动态加载内容 -->
                <div class="loading">
                    <i class="fas fa-cocktail fa-spin"></i>
                    <p>加载鸡尾酒中...</p>
                </div>
            </div>

            <div class="pagination" id="pagination">
                <!-- 分页按钮 -->
            </div>
        </section>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 菠萝鸡尾酒大全 | 仅供学习使用</p>
            <p class="warning">🍹 饮酒适量，请勿酒后驾车 🚗</p>
        </div>
    </footer>

    <!-- 模态框 -->
    <div id="cocktailModal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <div id="modalBody"></div>
        </div>
    </div>

    <script src="/static/js/main.js"></script>
</body>
</html>'''

    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)


def create_css_file():
    """创建CSS文件"""
    css_content = '''/* 全局样式 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Noto Sans SC', sans-serif;
    background: #f8f9fa;
    color: #333;
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* 导航栏 */
.navbar {
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 15px 0;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.5rem;
    font-weight: bold;
    color: #e67e22;
}

.logo i {
    font-size: 1.8rem;
}

.nav-stats {
    background: linear-gradient(135deg, #f39c12, #e67e22);
    color: white;
    padding: 8px 15px;
    border-radius: 20px;
    font-weight: bold;
}

.nav-stats i {
    margin-right: 5px;
}

/* 英雄区域 */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 60px 0;
    text-align: center;
}

.hero h1 {
    font-size: 2.5rem;
    margin-bottom: 20px;
}

.subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
    margin-bottom: 40px;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin-top: 40px;
}

.stat-card {
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    gap: 15px;
    min-width: 200px;
}

.stat-card i {
    font-size: 2rem;
}

.stat-card span {
    display: block;
    font-weight: bold;
    font-size: 1.1rem;
}

.stat-card small {
    opacity: 0.8;
    font-size: 0.9rem;
}

/* 搜索区域 */
.search-section {
    padding: 40px 0;
    background: white;
}

.search-box {
    display: flex;
    gap: 10px;
    max-width: 600px;
    margin: 0 auto 30px;
}

.search-box input {
    flex: 1;
    padding: 15px 20px;
    border: 2px solid #ddd;
    border-radius: 30px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.search-box input:focus {
    outline: none;
    border-color: #f39c12;
}

.search-box button {
    background: linear-gradient(135deg, #f39c12, #e67e22);
    color: white;
    border: none;
    padding: 15px 30px;
    border-radius: 30px;
    font-size: 1rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: transform 0.3s;
}

.search-box button:hover {
    transform: translateY(-2px);
}

.filter-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
}

.filter-tag {
    background: #f8f9fa;
    border: 2px solid #e9ecef;
    padding: 10px 20px;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s;
    font-weight: 500;
}

.filter-tag:hover {
    border-color: #f39c12;
    background: #fff8e1;
}

.filter-tag.active {
    background: #f39c12;
    border-color: #f39c12;
    color: white;
}

/* 鸡尾酒网格 */
.cocktails-section {
    padding: 60px 0;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
}

.section-header h2 {
    font-size: 2rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-header h2 i {
    color: #f39c12;
}

.view-controls select {
    padding: 10px 15px;
    border: 2px solid #ddd;
    border-radius: 10px;
    font-size: 1rem;
    cursor: pointer;
}

.cocktails-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 30px;
    margin-bottom: 40px;
}

.cocktail-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    cursor: pointer;
}

.cocktail-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.2);
}

.cocktail-image {
    height: 200px;
    background: linear-gradient(45deg, #f39c12, #e67e22);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 4rem;
}

.cocktail-badge {
    position: absolute;
    top: 15px;
    right: 15px;
    background: rgba(0,0,0,0.7);
    color: white;
    padding: 5px 15px;
    border-radius: 15px;
    font-size: 0.9rem;
}

.cocktail-content {
    padding: 20px;
}

.cocktail-header {
    display: flex;
    justify-content: space-between;
    align-items: start;
    margin-bottom: 15px;
}

.cocktail-title h3 {
    font-size: 1.3rem;
    margin-bottom: 5px;
}

.cocktail-title .en-name {
    color: #666;
    font-size: 0.9rem;
}

.cocktail-rating {
    color: #f39c12;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 5px;
}

.cocktail-meta {
    display: flex;
    gap: 15px;
    margin-bottom: 15px;
    color: #666;
    font-size: 0.9rem;
}

.cocktail-meta span {
    display: flex;
    align-items: center;
    gap: 5px;
}

.cocktail-description {
    color: #666;
    margin-bottom: 20px;
    line-height: 1.5;
}

.cocktail-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-bottom: 20px;
}

.cocktail-tag {
    background: #f0f7ff;
    color: #3498db;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 0.8rem;
}

/* 加载动画 */
.loading {
    grid-column: 1 / -1;
    text-align: center;
    padding: 60px;
}

.loading i {
    font-size: 3rem;
    color: #f39c12;
    margin-bottom: 20px;
}

.loading p {
    color: #666;
}

/* 分页 */
.pagination {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 40px;
}

.page-btn {
    padding: 10px 15px;
    border: 2px solid #ddd;
    background: white;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
}

.page-btn:hover {
    border-color: #f39c12;
}

.page-btn.active {
    background: #f39c12;
    border-color: #f39c12;
    color: white;
}

/* 页脚 */
.footer {
    background: #2c3e50;
    color: white;
    padding: 40px 0;
    text-align: center;
}

.footer p {
    margin-bottom: 10px;
}

.warning {
    color: #f39c12;
    font-weight: bold;
}

/* 模态框 */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.8);
    z-index: 2000;
    overflow-y: auto;
}

.modal-content {
    background: white;
    margin: 50px auto;
    max-width: 800px;
    border-radius: 15px;
    position: relative;
    animation: modalSlide 0.3s ease;
}

@keyframes modalSlide {
    from {
        transform: translateY(-50px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.close {
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 2rem;
    cursor: pointer;
    color: #666;
    z-index: 1;
}

.close:hover {
    color: #e74c3c;
}

/* 模态框内部样式 */
.modal-cocktail {
    padding: 30px;
}

.modal-header {
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid #f0f0f0;
}

.modal-header h2 {
    font-size: 2rem;
    color: #2c3e50;
    margin-bottom: 10px;
}

.modal-subtitle {
    color: #7f8c8d;
    font-size: 1.2rem;
    margin-bottom: 20px;
}

.modal-badges {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}

.modal-badge {
    background: #f39c12;
    color: white;
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 500;
}

.modal-body {
    margin-top: 30px;
}

.modal-section {
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid #eee;
}

.modal-section h3 {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #2c3e50;
    margin-bottom: 15px;
    font-size: 1.3rem;
}

.modal-section h3 i {
    color: #f39c12;
}

.modal-section p {
    line-height: 1.6;
    color: #555;
}

.ingredients-list {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 20px;
}

.ingredient-item {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #e9ecef;
}

.ingredient-item:last-child {
    border-bottom: none;
}

.ingredient-name {
    font-weight: 500;
    color: #2c3e50;
}

.ingredient-amount {
    color: #f39c12;
    font-weight: bold;
}

.instructions-list {
    padding-left: 20px;
}

.instructions-list li {
    margin-bottom: 10px;
    line-height: 1.6;
    color: #555;
}

.garnish-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.garnish-tag {
    background: #e8f4fc;
    color: #3498db;
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 0.9rem;
}

.modal-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 20px;
    margin-top: 30px;
}

.info-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 10px;
}

.info-item i {
    font-size: 1.5rem;
    color: #f39c12;
}

.info-item strong {
    display: block;
    color: #2c3e50;
    font-size: 0.9rem;
}

.info-item p {
    margin-top: 5px;
    color: #f39c12;
    font-weight: bold;
    font-size: 1.1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2rem;
    }

    .hero-stats {
        flex-direction: column;
        align-items: center;
    }

    .stat-card {
        width: 100%;
        max-width: 300px;
    }

    .cocktails-grid {
        grid-template-columns: 1fr;
    }

    .section-header {
        flex-direction: column;
        gap: 20px;
        text-align: center;
    }

    .modal-content {
        margin: 20px;
    }

    .modal-cocktail {
        padding: 20px;
    }
}'''

    with open('static/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)


def create_js_file():
    """创建JavaScript文件"""
    js_content = '''// 主应用程序
class CocktailApp {
    constructor() {
        this.currentPage = 1;
        this.perPage = 12;
        this.currentCategory = '';
        this.currentSort = 'rating';
        this.searchKeyword = '';

        this.init();
    }

    init() {
        this.bindEvents();
        this.loadCategories();
        this.loadCocktails();
    }

    bindEvents() {
        // 搜索按钮
        document.getElementById('searchBtn').addEventListener('click', () => this.handleSearch());
        document.getElementById('searchInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSearch();
        });

        // 排序
        document.getElementById('sortSelect').addEventListener('change', (e) => {
            this.currentSort = e.target.value;
            this.loadCocktails();
        });

        // 模态框关闭
        document.querySelector('.close').addEventListener('click', () => {
            this.closeModal();
        });

        // 点击模态框外部关闭
        document.getElementById('cocktailModal').addEventListener('click', (e) => {
            if (e.target.id === 'cocktailModal') {
                this.closeModal();
            }
        });
    }

    async loadCategories() {
        try {
            const response = await fetch('/api/categories');
            const data = await response.json();

            if (data.success) {
                this.renderCategories(data.data);
            }
        } catch (error) {
            console.error('加载分类失败:', error);
        }
    }

    renderCategories(categories) {
        const container = document.getElementById('filterTags');
        let html = '<button class="filter-tag active" data-category="">全部</button>';

        categories.forEach(category => {
            html += `<button class="filter-tag" data-category="${category}">${category}</button>`;
        });

        container.innerHTML = html;

        // 添加分类筛选事件
        container.querySelectorAll('.filter-tag').forEach(tag => {
            tag.addEventListener('click', (e) => this.handleFilter(e.target));
        });
    }

    async loadCocktails() {
        try {
            this.showLoading();

            const params = new URLSearchParams({
                page: this.currentPage,
                per_page: this.perPage,
                category: this.currentCategory,
                keyword: this.searchKeyword
            });

            const response = await fetch(`/api/cocktails?${params}`);
            const data = await response.json();

            if (data.success) {
                // 更新总数量
                document.getElementById('totalCount').textContent = data.total;
                this.renderCocktails(data.data);
                this.renderPagination(data);
            }
        } catch (error) {
            console.error('加载失败:', error);
            this.showError();
        }
    }

    renderCocktails(cocktails) {
        const container = document.getElementById('cocktailsContainer');

        if (cocktails.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-glass-cheers"></i>
                    <h3>未找到匹配的鸡尾酒</h3>
                    <p>尝试其他搜索词或分类</p>
                </div>
            `;
            return;
        }

        // 排序
        if (this.currentSort === 'rating') {
            cocktails.sort((a, b) => b.rating - a.rating);
        } else if (this.currentSort === 'name') {
            cocktails.sort((a, b) => a.name_zh.localeCompare(b.name_zh));
        } else if (this.currentSort === 'difficulty') {
            const order = { '简单': 1, '中等': 2, '复杂': 3 };
            cocktails.sort((a, b) => order[a.difficulty] - order[b.difficulty]);
        }

        container.innerHTML = cocktails.map(cocktail => `
            <div class="cocktail-card" data-id="${cocktail.id}">
                <div class="cocktail-image">
                    <i class="fas fa-cocktail"></i>
                    <span class="cocktail-badge">${cocktail.category}</span>
                </div>
                <div class="cocktail-content">
                    <div class="cocktail-header">
                        <div class="cocktail-title">
                            <h3>${cocktail.name_zh}</h3>
                            <div class="en-name">${cocktail.name}</div>
                        </div>
                        <div class="cocktail-rating">
                            <i class="fas fa-star"></i>
                            <span>${cocktail.rating}</span>
                        </div>
                    </div>

                    <div class="cocktail-meta">
                        <span><i class="fas fa-clock"></i> ${cocktail.prep_time}分钟</span>
                        <span><i class="fas fa-wine-glass-alt"></i> ${cocktail.alcohol_level}%</span>
                        <span><i class="fas fa-fire"></i> ${cocktail.calories}卡</span>
                    </div>

                    <p class="cocktail-description">${cocktail.description}</p>

                    <div class="cocktail-tags">
                        ${cocktail.flavor_profile.map(flavor => 
                            `<span class="cocktail-tag">${flavor}</span>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `).join('');

        // 添加点击事件
        container.querySelectorAll('.cocktail-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const id = card.dataset.id;
                this.showCocktailDetail(id);
            });
        });
    }

    renderPagination(data) {
        const pagination = document.getElementById('pagination');

        if (data.total_pages <= 1) {
            pagination.innerHTML = '';
            return;
        }

        let html = '';

        // 上一页
        if (this.currentPage > 1) {
            html += `<button class="page-btn" data-page="${this.currentPage - 1}">
                        <i class="fas fa-chevron-left"></i>
                     </button>`;
        }

        // 页码
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(data.total_pages, startPage + 4);

        for (let i = startPage; i <= endPage; i++) {
            html += `<button class="page-btn ${i === this.currentPage ? 'active' : ''}" 
                             data-page="${i}">${i}</button>`;
        }

        // 下一页
        if (this.currentPage < data.total_pages) {
            html += `<button class="page-btn" data-page="${this.currentPage + 1}">
                        <i class="fas fa-chevron-right"></i>
                     </button>`;
        }

        pagination.innerHTML = html;

        // 添加分页事件
        pagination.querySelectorAll('.page-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.currentPage = parseInt(btn.dataset.page);
                this.loadCocktails();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
    }

    handleSearch() {
        const input = document.getElementById('searchInput');
        this.searchKeyword = input.value.trim();
        this.currentPage = 1;
        this.loadCocktails();
    }

    handleFilter(tag) {
        // 更新活动状态
        document.querySelectorAll('.filter-tag').forEach(t => t.classList.remove('active'));
        tag.classList.add('active');

        this.currentCategory = tag.dataset.category;
        this.currentPage = 1;
        this.loadCocktails();
    }

    async showCocktailDetail(id) {
        try {
            const response = await fetch(`/api/cocktail/${id}`);
            const data = await response.json();

            if (data.success) {
                this.renderModal(data.data);
                document.getElementById('cocktailModal').style.display = 'block';
                document.body.style.overflow = 'hidden';
            }
        } catch (error) {
            console.error('加载详情失败:', error);
        }
    }

    renderModal(cocktail) {
        const modalBody = document.getElementById('modalBody');

        modalBody.innerHTML = `
            <div class="modal-cocktail">
                <div class="modal-header">
                    <h2>${cocktail.name_zh}</h2>
                    <p class="modal-subtitle">${cocktail.name}</p>
                    <div class="modal-badges">
                        <span class="modal-badge">${cocktail.category}</span>
                        <span class="modal-badge">${cocktail.difficulty}</span>
                        <span class="modal-badge">${cocktail.origin}</span>
                    </div>
                </div>

                <div class="modal-body">
                    <div class="modal-section">
                        <h3><i class="fas fa-info-circle"></i> 简介</h3>
                        <p>${cocktail.description}</p>
                        ${cocktail.story ? `<div class="story"><h4>历史故事</h4><p>${cocktail.story}</p></div>` : ''}
                    </div>

                    <div class="modal-section">
                        <h3><i class="fas fa-list-ul"></i> 配料</h3>
                        <div class="ingredients-list">
                            ${cocktail.ingredients.map(ing => `
                                <div class="ingredient-item">
                                    <span class="ingredient-name">${ing.name}</span>
                                    <span class="ingredient-amount">${ing.amount}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <div class="modal-section">
                        <h3><i class="fas fa-martini-glass-citrus"></i> 制作步骤</h3>
                        <ol class="instructions-list">
                            ${cocktail.instructions.map((step, index) => `
                                <li>${step}</li>
                            `).join('')}
                        </ol>
                    </div>

                    <div class="modal-section">
                        <h3><i class="fas fa-utensils"></i> 装饰</h3>
                        <div class="garnish-tags">
                            ${cocktail.garnish.map(g => `<span class="garnish-tag">${g}</span>`).join('')}
                        </div>
                    </div>

                    <div class="modal-info">
                        <div class="info-item">
                            <i class="fas fa-clock"></i>
                            <div>
                                <strong>准备时间</strong>
                                <p>${cocktail.prep_time} 分钟</p>
                            </div>
                        </div>
                        <div class="info-item">
                            <i class="fas fa-fire"></i>
                            <div>
                                <strong>卡路里</strong>
                                <p>${cocktail.calories} 卡</p>
                            </div>
                        </div>
                        <div class="info-item">
                            <i class="fas fa-wine-glass-alt"></i>
                            <div>
                                <strong>酒精度</strong>
                                <p>${cocktail.alcohol_level}%</p>
                            </div>
                        </div>
                        <div class="info-item">
                            <i class="fas fa-star"></i>
                            <div>
                                <strong>评分</strong>
                                <p>${cocktail.rating}/5.0</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    closeModal() {
        document.getElementById('cocktailModal').style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    showLoading() {
        const container = document.getElementById('cocktailsContainer');
        container.innerHTML = `
            <div class="loading">
                <i class="fas fa-cocktail fa-spin"></i>
                <p>加载鸡尾酒中...</p>
            </div>
        `;
    }

    showError() {
        const container = document.getElementById('cocktailsContainer');
        container.innerHTML = `
            <div class="loading">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>加载失败</h3>
                <button onclick="location.reload()">重试</button>
            </div>
        `;
    }
}

// 页面加载完成后初始化应用
window.addEventListener('DOMContentLoaded', () => {
    window.app = new CocktailApp();
});'''

    with open('static/js/main.js', 'w', encoding='utf-8') as f:
        f.write(js_content)


class CocktailData:
    def __init__(self):
        self.data_file = 'data/cocktails.json'
        self.cocktails = self.load_or_create_data()

    def load_or_create_data(self):
        """加载或创建鸡尾酒数据"""
        try:
            # 先尝试读取文件
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 检查数据格式
                    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                        print(f"✓ 从文件加载了 {len(data)} 种鸡尾酒")
                        return data

            # 如果文件不存在或格式不对，生成新数据
            print("正在生成鸡尾酒数据...")
            data = self.generate_sample_data()

            # 保存到文件
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"✓ 生成了 {len(data)} 种鸡尾酒并保存到文件")
            return data

        except Exception as e:
            print(f"✗ 加载数据出错: {e}")
            # 生成默认数据
            return self.generate_sample_data()

    def generate_sample_data(self):
        """生成200种示例鸡尾酒数据"""
        cocktails = []

        # 基础鸡尾酒类型
        base_cocktails = [
            {
                "id": 1,
                "name": "Piña Colada",
                "name_zh": "椰林飘香",
                "category": "热带鸡尾酒",
                "alcohol_level": 15,
                "difficulty": "简单",
                "glass_type": "飓风杯",
                "prep_time": 5,
                "description": "经典的加勒比海鸡尾酒，融合了菠萝和椰子的热带风味",
                "story": "起源于波多黎各，1978年被宣布为波多黎各的官方饮品",
                "ingredients": [
                    {"name": "白朗姆酒", "amount": "60ml"},
                    {"name": "椰子奶油", "amount": "45ml"},
                    {"name": "新鲜菠萝汁", "amount": "90ml"},
                    {"name": "碎冰", "amount": "1杯"}
                ],
                "instructions": [
                    "将所有原料放入搅拌机中",
                    "加入碎冰搅拌均匀",
                    "倒入飓风杯中",
                    "用菠萝片和樱桃装饰"
                ],
                "garnish": ["菠萝片", "樱桃", "小纸伞"],
                "flavor_profile": ["甜", "奶油", "热带"],
                "rating": 4.8,
                "calories": 245,
                "origin": "波多黎各"
            },
            {
                "id": 2,
                "name": "Tequila Sunrise",
                "name_zh": "龙舌兰日出",
                "category": "经典鸡尾酒",
                "alcohol_level": 12,
                "difficulty": "简单",
                "glass_type": "高球杯",
                "prep_time": 3,
                "description": "色彩如日出般绚丽的鸡尾酒，菠萝汁的甜与龙舌兰的烈完美结合",
                "ingredients": [
                    {"name": "龙舌兰酒", "amount": "45ml"},
                    {"name": "新鲜菠萝汁", "amount": "90ml"},
                    {"name": "橙汁", "amount": "60ml"},
                    {"name": "红石榴糖浆", "amount": "15ml"}
                ],
                "instructions": [
                    "在高球杯中加入冰块",
                    "依次倒入龙舌兰酒、菠萝汁和橙汁",
                    "轻轻搅拌",
                    "沿杯壁缓缓倒入红石榴糖浆",
                    "让它自然沉淀形成渐变效果",
                    "用橙片和樱桃装饰"
                ],
                "garnish": ["橙片", "樱桃"],
                "flavor_profile": ["甜", "果味", "清新"],
                "rating": 4.5,
                "calories": 210,
                "origin": "美国"
            },
            {
                "id": 3,
                "name": "Pineapple Mojito",
                "name_zh": "菠萝莫吉托",
                "category": "热带鸡尾酒",
                "alcohol_level": 10,
                "difficulty": "简单",
                "glass_type": "高球杯",
                "prep_time": 4,
                "description": "清新爽口的菠萝版莫吉托，带有薄荷的清凉",
                "ingredients": [
                    {"name": "白朗姆酒", "amount": "45ml"},
                    {"name": "新鲜菠萝汁", "amount": "60ml"},
                    {"name": "青柠汁", "amount": "20ml"},
                    {"name": "薄荷叶", "amount": "8-10片"},
                    {"name": "苏打水", "amount": "适量"},
                    {"name": "糖浆", "amount": "15ml"}
                ],
                "instructions": [
                    "在高球杯中放入薄荷叶和糖浆",
                    "用捣棒轻轻碾压薄荷叶",
                    "加入朗姆酒、菠萝汁和青柠汁",
                    "加入碎冰搅拌",
                    "用苏打水填满",
                    "用菠萝角和薄荷枝装饰"
                ],
                "garnish": ["菠萝角", "薄荷枝", "青柠角"],
                "flavor_profile": ["清新", "薄荷", "果味"],
                "rating": 4.6,
                "calories": 180,
                "origin": "古巴"
            },
            {
                "id": 4,
                "name": "Blue Hawaii",
                "name_zh": "蓝色夏威夷",
                "category": "热带鸡尾酒",
                "alcohol_level": 17,
                "difficulty": "中等",
                "glass_type": "飓风杯",
                "prep_time": 6,
                "description": "梦幻的蓝色鸡尾酒，带有菠萝和椰子的热带风味",
                "ingredients": [
                    {"name": "朗姆酒", "amount": "30ml"},
                    {"name": "蓝橙利口酒", "amount": "30ml"},
                    {"name": "伏特加", "amount": "15ml"},
                    {"name": "菠萝汁", "amount": "60ml"},
                    {"name": "椰子奶油", "amount": "15ml"},
                    {"name": "碎冰", "amount": "1杯"}
                ],
                "instructions": [
                    "将所有原料放入搅拌机",
                    "加入碎冰搅拌均匀",
                    "倒入飓风杯中",
                    "用菠萝片和樱桃装饰"
                ],
                "garnish": ["菠萝片", "樱桃", "小花伞"],
                "flavor_profile": ["甜", "热带", "奶油"],
                "rating": 4.7,
                "calories": 260,
                "origin": "美国"
            },
            {
                "id": 5,
                "name": "Virgin Piña Colada",
                "name_zh": "无酒精椰林飘香",
                "category": "无酒精",
                "alcohol_level": 0,
                "difficulty": "简单",
                "glass_type": "飓风杯",
                "prep_time": 5,
                "description": "经典椰林飘香的无酒精版本，适合所有人群",
                "ingredients": [
                    {"name": "菠萝汁", "amount": "120ml"},
                    {"name": "椰子奶油", "amount": "60ml"},
                    {"name": "碎冰", "amount": "1杯"},
                    {"name": "糖浆", "amount": "10ml"}
                ],
                "instructions": [
                    "将所有原料放入搅拌机",
                    "加入碎冰搅拌均匀",
                    "倒入飓风杯中",
                    "用菠萝片和樱桃装饰"
                ],
                "garnish": ["菠萝片", "樱桃"],
                "flavor_profile": ["甜", "奶油", "热带"],
                "rating": 4.4,
                "calories": 220,
                "origin": "美国"
            }
        ]

        # 生成更多鸡尾酒
        categories = ["热带鸡尾酒", "经典鸡尾酒", "创意调酒", "派对饮品", "无酒精", "季节限定"]
        difficulties = ["简单", "中等", "复杂"]
        origins = ["古巴", "美国", "巴西", "泰国", "菲律宾", "中国", "墨西哥", "牙买加", "西班牙", "法国", "意大利",
                   "日本", "越南", "马来西亚"]

        # 先添加基础鸡尾酒
        for cocktail in base_cocktails:
            cocktails.append(cocktail)

        # 生成更多鸡尾酒，直到200种
        for i in range(len(base_cocktails), 200):
            cocktail_id = i + 1

            # 随机生成鸡尾酒
            cocktail = {
                "id": cocktail_id,
                "name": f"Pineapple Special {cocktail_id}",
                "name_zh": f"菠萝特调{cocktail_id}号",
                "category": random.choice(categories),
                "alcohol_level": random.randint(0, 40),
                "difficulty": random.choice(difficulties),
                "glass_type": random.choice(["飓风杯", "马天尼杯", "高球杯", "古典杯", "柯林杯", "葡萄酒杯"]),
                "prep_time": random.randint(2, 15),
                "description": f"美味的菠萝汁鸡尾酒，融合了热带风情和独特口感，是{cocktail_id}号特色饮品",
                "ingredients": [
                    {"name": "新鲜菠萝汁", "amount": f"{random.randint(60, 150)}ml"},
                    {"name": random.choice(["朗姆酒", "伏特加", "龙舌兰", "金酒", "威士忌", "白兰地"]),
                     "amount": f"{random.randint(0 if cocktail_id % 10 == 0 else 30, 60)}ml"},
                    {"name": random.choice(["青柠汁", "柠檬汁", "橙汁", "椰奶", "苏打水", "汤力水"]),
                     "amount": f"{random.randint(30, 90)}ml"},
                    {"name": random.choice(["糖浆", "蜂蜜", "薄荷叶", "姜", "肉桂", "肉豆蔻"]),
                     "amount": random.choice(["适量", "1茶匙", "2-3片", "少量", "1枝"])}
                ],
                "instructions": [
                    "准备所有原料和调酒工具",
                    f"在{random.choice(['调酒壶', '搅拌杯', '直接杯中'])}中加入冰块",
                    "依次加入液体原料",
                    random.choice(["用力摇匀10-15秒", "轻轻搅拌", "使用搅拌机混合", "用吧匙搅拌"]),
                    f"过滤倒入{random.choice(['准备好的杯中', '装满冰块的杯中'])}",
                    "用装饰物点缀",
                    "立即享用"
                ],
                "garnish": random.sample(["菠萝片", "樱桃", "薄荷叶", "青柠角", "小花伞", "肉桂棒", "橙片", "柠檬皮"],
                                         random.randint(1, 3)),
                "flavor_profile": random.sample(["甜", "酸", "果味", "热带", "清新", "辛辣", "花香", "草本", "奶油"],
                                                3),
                "rating": round(random.uniform(3.5, 5.0), 1),
                "calories": random.randint(150, 400),
                "origin": random.choice(origins)
            }

            # 根据类别添加特殊描述
            if cocktail["category"] == "无酒精":
                cocktail["description"] = f"清爽的无酒精菠萝饮品，适合所有人群，提供{cocktail_id}号独特体验"
                cocktail["alcohol_level"] = 0
            elif cocktail["category"] == "热带鸡尾酒":
                cocktail["description"] = f"充满热带风情的菠萝鸡尾酒，带来{cocktail_id}号度假感觉"
            elif cocktail["category"] == "创意调酒":
                cocktail["description"] = f"创意十足的菠萝鸡尾酒，展现{cocktail_id}号独特风味组合"

            # 添加故事
            if random.random() > 0.7:  # 30%的概率有故事
                stories = [
                    f"这款鸡尾酒是由{random.choice(origins)}的调酒师创作，深受当地欢迎",
                    f"起源于{random.choice(['19世纪', '20世纪初', '20世纪70年代', '21世纪初'])}的传统配方",
                    f"曾获得{random.choice(['国际调酒大赛', '本地鸡尾酒比赛', '美食节'])}的奖项",
                    f"灵感来源于{random.choice(['热带雨林', '海边日落', '传统节日', '民间传说'])}"
                ]
                cocktail["story"] = random.choice(stories)

            cocktails.append(cocktail)

        return cocktails


# 初始化数据
cocktail_data = CocktailData()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html', total_count=len(cocktail_data.cocktails))


@app.route('/api/cocktails')
def get_cocktails():
    """获取鸡尾酒列表API"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 12))
        category = request.args.get('category', '')
        keyword = request.args.get('keyword', '')

        # 过滤数据
        filtered = cocktail_data.cocktails

        if category and category != '':
            filtered = [c for c in filtered if c.get('category', '') == category]

        if keyword:
            keyword = keyword.lower()
            filtered = [c for c in filtered if
                        keyword in c.get('name', '').lower() or
                        keyword in c.get('name_zh', '').lower() or
                        keyword in c.get('description', '').lower()]

        # 分页
        total = len(filtered)
        start = (page - 1) * per_page
        end = start + per_page

        return jsonify({
            'success': True,
            'data': filtered[start:end],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/cocktail/<int:cocktail_id>')
def get_cocktail(cocktail_id):
    """获取单个鸡尾酒详情"""
    try:
        for cocktail in cocktail_data.cocktails:
            if cocktail.get('id') == cocktail_id:
                return jsonify({'success': True, 'data': cocktail})
        return jsonify({'success': False, 'message': '未找到'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/random')
def get_random():
    """获取随机推荐"""
    try:
        count = min(int(request.args.get('count', 5)), len(cocktail_data.cocktails))
        random_cocktails = random.sample(cocktail_data.cocktails, count)
        return jsonify({'success': True, 'data': random_cocktails})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/categories')
def get_categories():
    """获取所有分类"""
    try:
        categories = list(set([c.get('category', '其他') for c in cocktail_data.cocktails]))
        return jsonify({'success': True, 'data': sorted(categories)})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("菠萝汁鸡尾酒大全应用")
    print("=" * 50)
    print(f"已加载 {len(cocktail_data.cocktails)} 种鸡尾酒")
    print(f"服务器运行在: http://jiweijui200:5000")
    print("=" * 50)
    print("请打开浏览器访问以上地址")

    # 创建必要的文件
    try:
        create_html_template()
        print("✓ HTML模板创建完成")

        create_css_file()
        print("✓ CSS样式文件创建完成")

        create_js_file()
        print("✓ JavaScript文件创建完成")

        print("文件创建完成！开始运行服务器...")
    except Exception as e:
        print(f"✗ 创建文件出错: {e}")

    # 修改这一行，绑定到所有网络接口，并指定主机名
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
