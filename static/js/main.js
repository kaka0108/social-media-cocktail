// 主应用程序
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
});