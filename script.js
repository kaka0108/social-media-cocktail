// 全局变量
let allCocktails = [];

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    loadCocktails();
    setupEventListeners();
});

// 加载鸡尾酒数据
function loadCocktails() {
    fetch('data/cocktails.json')
        .then(response => response.json())
        .then(data => {
            allCocktails = data.cocktails;
            displayCocktails(allCocktails);
            updateStats();
        })
        .catch(error => {
            console.error('加载数据失败:', error);
            document.getElementById('cocktailContainer').innerHTML = 
                '<p class="error">无法加载数据，请确保 cocktails.json 文件存在。</p>';
        });
}

// 显示鸡尾酒
function displayCocktails(cocktails) {
    const container = document.getElementById('cocktailContainer');

    if (cocktails.length === 0) {
        container.innerHTML = '<p class="no-results">没有找到匹配的鸡尾酒。</p>';
        return;
    }

    const cards = cocktails.map(cocktail => `
        <div class="cocktail-card" data-category="${cocktail.base_spirit_category}">
            <div class="card-image">
                <img src="${cocktail.image_url}" alt="${cocktail.cocktail_name}" 
                     onerror="this.src='https://source.unsplash.com/400x300/?cocktail,pineapple'">
                <span class="category-tag">${cocktail.base_spirit_category.split('(')[0]}</span>
                <span class="country-badge">${cocktail.country}</span>
            </div>
            <div class="card-content">
                <h3 class="cocktail-name">${cocktail.cocktail_name}</h3>
                <div class="base-spirit">
                    <i class="fas fa-wine-bottle"></i>
                    ${cocktail.base_spirit}
                </div>
                <div class="rating">
                    ${getStarRating(cocktail.rating)}
                    <span style="color:#666; margin-left:5px;">${cocktail.rating}</span>
                </div>
                <div class="ingredients">
                    <h4>主要配料：</h4>
                    <div class="ingredients-list">
                        ${cocktail.ingredients.slice(0, 3).map(ing => 
                            `<span class="ingredient-tag">${ing}</span>`
                        ).join('')}
                        ${cocktail.ingredients.length > 3 ? 
                            `<span class="ingredient-tag">+${cocktail.ingredients.length - 3}种</span>` : 
                            ''}
                    </div>
                </div>
            </div>
        </div>
    `).join('');

    container.innerHTML = cards;
}

// 获取星标评分
function getStarRating(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5 ? 1 : 0;
    const emptyStars = 5 - fullStars - halfStar;

    return '★'.repeat(fullStars) + 
           (halfStar ? '½' : '') + 
           '☆'.repeat(emptyStars);
}

// 设置事件监听器
function setupEventListeners() {
    // 搜索功能
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', filterCocktails);

    // 分类过滤
    const categoryFilter = document.getElementById('categoryFilter');
    categoryFilter.addEventListener('change', filterCocktails);
}

// 过滤鸡尾酒
function filterCocktails() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const category = document.getElementById('categoryFilter').value;

    let filtered = allCocktails;

    // 按搜索词过滤
    if (searchTerm) {
        filtered = filtered.filter(cocktail => 
            cocktail.country.toLowerCase().includes(searchTerm) ||
            cocktail.cocktail_name.toLowerCase().includes(searchTerm) ||
            cocktail.base_spirit.toLowerCase().includes(searchTerm)
        );
    }

    // 按分类过滤
    if (category !== 'all') {
        filtered = filtered.filter(cocktail => 
            cocktail.base_spirit_category.includes(category)
        );
    }

    displayCocktails(filtered);
    updateStats(filtered.length);
}

// 更新统计信息
function updateStats(filteredCount) {
    const count = filteredCount || allCocktails.length;
    document.querySelector('.stat-card:nth-child(3) h3').textContent = count;
}

// 错误处理
window.addEventListener('error', function(e) {
    console.error('页面错误:', e.error);
});