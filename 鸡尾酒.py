"""
菠萝汁鸡尾酒大全 - 极速版本
完全移除图片生成和复杂功能
"""

from flask import Flask, render_template, jsonify, request
import json
import os
import time

app = Flask(__name__)

# 确保目录存在
os.makedirs('data', exist_ok=True)
os.makedirs('templates', exist_ok=True)


# ==================== 极简数据加载 ====================
class FastCocktailData:
    def __init__(self):
        self.data_file = 'data/cocktails.json'
        self.cocktails = []
        self.categories = []
        self._load_data()

    def _load_data(self):
        """快速加载数据，不使用图片"""
        print("⚡ 快速加载数据...")
        start = time.time()

        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    raw_data = json.load(f)

                # 只取前100个，过滤掉"特调"
                raw_data = [c for c in raw_data[:100] if '特调' not in c.get('name_zh', '')]

                # 极简数据格式
                self.cocktails = []
                for item in raw_data:
                    cocktail = {
                        'id': item.get('id'),
                        'name': item.get('name', ''),
                        'name_zh': item.get('name_zh', ''),
                        'category': item.get('category', ''),
                        'rating': item.get('rating', 4.0),
                        'prep_time': item.get('prep_time', 5),
                        'description': item.get('description', '')[:80] + '...' if len(
                            item.get('description', '')) > 80 else item.get('description', ''),
                        # 不使用图片
                        'flavor_profile': item.get('flavor_profile', [])[:2]
                    }
                    self.cocktails.append(cocktail)

                # 提取分类
                self.categories = list(sorted(set([c['category'] for c in self.cocktails if c['category']])))

                load_time = time.time() - start
                print(f"✅ 加载完成: {len(self.cocktails)} 种鸡尾酒")
                print(f"⏱️  耗时: {load_time:.3f}秒")
            else:
                print("❌ 数据文件不存在")
                self._create_sample_data()

        except Exception as e:
            print(f"❌ 加载失败: {e}")
            self._create_sample_data()

    def _create_sample_data(self):
        """创建示例数据"""
        print("创建示例数据...")
        self.cocktails = []
        for i in range(1, 101):
            self.cocktails.append({
                'id': i,
                'name': f'Pineapple Cocktail {i}',
                'name_zh': f'菠萝鸡尾酒{i}',
                'category': '热带鸡尾酒',
                'rating': 4.0,
                'prep_time': 5,
                'description': '美味的菠萝鸡尾酒',
                'flavor_profile': ['甜', '热带']
            })
        self.categories = ['热带鸡尾酒', '经典鸡尾酒']


# 初始化数据
cocktail_data = FastCocktailData()


# ==================== 创建极简HTML模板 ====================
def create_simple_html():
    """创建极简HTML，所有CSS和JS内联"""
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>菠萝鸡尾酒大全</title>
    <style>
        /* 内联所有CSS */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa; 
            color: #333;
            line-height: 1.6;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        header { 
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 40px 0;
            text-align: center;
            margin-bottom: 30px;
        }
        h1 { 
            font-size: 2rem; 
            margin-bottom: 10px; 
        }
        .subtitle { 
            opacity: 0.9; 
            font-size: 1.1rem; 
        }
        .search-box { 
            display: flex; 
            gap: 10px; 
            margin-bottom: 20px;
            max-width: 600px;
            margin: 0 auto 30px;
        }
        .search-box input {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #ddd;
            border-radius: 30px;
            font-size: 1rem;
            outline: none;
        }
        .search-box input:focus {
            border-color: #667eea;
        }
        .search-box button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 30px;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.3s;
        }
        .search-box button:hover {
            background: #5a67d8;
        }
        .filter-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-bottom: 30px;
        }
        .filter-tag {
            background: white;
            border: 2px solid #e2e8f0;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .filter-tag:hover {
            border-color: #667eea;
        }
        .filter-tag.active {
            background: #667eea;
            border-color: #667eea;
            color: white;
        }
        .cocktails-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .cocktail-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .cocktail-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        }
        .cocktail-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 10px;
        }
        .cocktail-title h3 {
            font-size: 1.2rem;
            color: #2d3748;
        }
        .cocktail-rating {
            color: #f6ad55;
            font-weight: bold;
        }
        .cocktail-description {
            color: #718096;
            margin-bottom: 15px;
            font-size: 0.95rem;
        }
        .cocktail-meta {
            display: flex;
            gap: 15px;
            color: #a0aec0;
            font-size: 0.9rem;
            margin-bottom: 10px;
        }
        .cocktail-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }
        .cocktail-tag {
            background: #ebf8ff;
            color: #4299e1;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
        }
        footer {
            background: #2d3748;
            color: white;
            padding: 30px 0;
            text-align: center;
            margin-top: 50px;
        }
        .pagination {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-top: 40px;
        }
        .page-btn {
            padding: 8px 12px;
            border: 1px solid #cbd5e0;
            background: white;
            border-radius: 6px;
            cursor: pointer;
        }
        .page-btn:hover {
            border-color: #667eea;
        }
        .page-btn.active {
            background: #667eea;
            border-color: #667eea;
            color: white;
        }
        @media (max-width: 768px) {
            .cocktails-grid {
                grid-template-columns: 1fr;
            }
            h1 {
                font-size: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>菠萝汁鸡尾酒大全</h1>
            <p class="subtitle">100种精选配方，极速加载</p>
        </div>
    </header>

    <main class="container">
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="搜索鸡尾酒名称...">
            <button id="searchBtn">搜索</button>
        </div>

        <div class="filter-tags" id="filterTags">
            <button class="filter-tag active" data-category="">全部</button>
        </div>

        <div id="cocktailsContainer" class="cocktails-grid">
            <!-- 内容通过JavaScript动态加载 -->
            <div>加载中...</div>
        </div>

        <div class="pagination" id="pagination"></div>
    </main>

    <footer>
        <div class="container">
            <p>© 2024 菠萝鸡尾酒大全 | 极速版本</p>
            <p style="color: #f6ad55; margin-top: 10px;">饮酒适量，请勿酒后驾车</p>
        </div>
    </footer>

    <script>
        // 内联所有JavaScript
        class FastCocktailApp {
            constructor() {
                this.currentPage = 1;
                this.perPage = 12;
                this.currentCategory = '';
                this.searchKeyword = '';

                this.init();
            }

            init() {
                this.loadCategories();
                this.loadCocktails();

                // 绑定事件
                document.getElementById('searchBtn').addEventListener('click', () => this.handleSearch());
                document.getElementById('searchInput').addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') this.handleSearch();
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
                    console.log('加载分类失败');
                }
            }

            renderCategories(categories) {
                const container = document.getElementById('filterTags');
                categories.forEach(category => {
                    const button = document.createElement('button');
                    button.className = 'filter-tag';
                    button.textContent = category;
                    button.dataset.category = category;
                    button.addEventListener('click', () => {
                        document.querySelectorAll('.filter-tag').forEach(tag => tag.classList.remove('active'));
                        button.classList.add('active');
                        this.currentCategory = category;
                        this.currentPage = 1;
                        this.loadCocktails();
                    });
                    container.appendChild(button);
                });
            }

            async loadCocktails() {
                try {
                    const params = new URLSearchParams({
                        page: this.currentPage,
                        per_page: this.perPage,
                        category: this.currentCategory,
                        keyword: this.searchKeyword
                    });

                    const response = await fetch(`/api/cocktails?${params}`);
                    const data = await response.json();

                    if (data.success) {
                        this.renderCocktails(data.data);
                        this.renderPagination(data);
                    }
                } catch (error) {
                    console.log('加载失败');
                    document.getElementById('cocktailsContainer').innerHTML = '<div>加载失败，请刷新页面</div>';
                }
            }

            renderCocktails(cocktails) {
                const container = document.getElementById('cocktailsContainer');

                if (cocktails.length === 0) {
                    container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px;">未找到匹配的鸡尾酒</div>';
                    return;
                }

                // 按评分排序
                cocktails.sort((a, b) => b.rating - a.rating);

                let html = '';
                cocktails.forEach(cocktail => {
                    html += `
                        <div class="cocktail-card">
                            <div class="cocktail-header">
                                <div class="cocktail-title">
                                    <h3>${cocktail.name_zh}</h3>
                                    <div style="color: #718096; font-size: 0.9rem;">${cocktail.name}</div>
                                </div>
                                <div class="cocktail-rating">★ ${cocktail.rating}</div>
                            </div>
                            <div class="cocktail-meta">
                                <span>⏱️ ${cocktail.prep_time}分钟</span>
                                <span>🏷️ ${cocktail.category}</span>
                            </div>
                            <p class="cocktail-description">${cocktail.description}</p>
                            <div class="cocktail-tags">
                                ${(cocktail.flavor_profile || []).map(tag => 
                                    `<span class="cocktail-tag">${tag}</span>`
                                ).join('')}
                            </div>
                        </div>
                    `;
                });

                container.innerHTML = html;
            }

            renderPagination(data) {
                const pagination = document.getElementById('pagination');

                if (!data.total_pages || data.total_pages <= 1) {
                    pagination.innerHTML = '';
                    return;
                }

                let html = '';

                if (this.currentPage > 1) {
                    html += `<button class="page-btn" data-page="${this.currentPage - 1}">上一页</button>`;
                }

                const startPage = Math.max(1, this.currentPage - 2);
                const endPage = Math.min(data.total_pages, startPage + 4);

                for (let i = startPage; i <= endPage; i++) {
                    html += `<button class="page-btn ${i === this.currentPage ? 'active' : ''}" data-page="${i}">${i}</button>`;
                }

                if (this.currentPage < data.total_pages) {
                    html += `<button class="page-btn" data-page="${this.currentPage + 1}">下一页</button>`;
                }

                pagination.innerHTML = html;

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
        }

        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', () => {
            window.app = new FastCocktailApp();
        });
    </script>
</body>
</html>'''

    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html)


# ==================== Flask路由 ====================

@app.route('/')
def index():
    """主页 - 返回内联了所有资源的HTML"""
    return render_template('index.html')


@app.route('/api/cocktails')
def get_cocktails():
    """获取鸡尾酒列表 - 极简API"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 12))
        category = request.args.get('category', '')
        keyword = request.args.get('keyword', '')

        # 开始过滤
        filtered = cocktail_data.cocktails

        if category:
            filtered = [c for c in filtered if c['category'] == category]

        if keyword:
            keyword = keyword.lower()
            filtered = [
                c for c in filtered
                if keyword in c['name'].lower() or
                   keyword in c['name_zh'].lower() or
                   keyword in c['description'].lower()
            ]

        # 按评分排序
        filtered.sort(key=lambda x: x['rating'], reverse=True)

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


@app.route('/api/categories')
def get_categories():
    """获取分类 - 极简API"""
    return jsonify({
        'success': True,
        'data': cocktail_data.categories
    })


@app.route('/api/status')
def status():
    """状态检查"""
    return jsonify({
        'success': True,
        'status': 'running',
        'cocktail_count': len(cocktail_data.cocktails),
        'load_time': '极速加载'
    })


# ==================== 启动应用 ====================
if __name__ == '__main__':
    print("=" * 50)
    print("菠萝汁鸡尾酒大全 - 极速版本")
    print("=" * 50)
    print("特点:")
    print("  • 完全移除图片功能")
    print("  • 所有资源内联（无外部CSS/JS文件）")
    print("  • 极简数据格式")
    print("  • 无缓存，无复杂逻辑")
    print("=" * 50)

    # 创建HTML模板
    create_simple_html()
    print("✓ HTML模板创建完成")

    print(f"📊 已加载 {len(cocktail_data.cocktails)} 种鸡尾酒")
    print(f"🚀 服务器启动: http://jiweijui200:5000")
    print("=" * 50)
    print("💡 如果仍然卡顿，请检查:")
    print("  1. 服务器硬件资源")
    print("  2. 网络连接")
    print("  3. 浏览器缓存")
    print("=" * 50)

    # 使用最简单的配置运行
    app.run(
        debug=False,  # 关闭debug
        host='0.0.0.0',
        port=5000,
        threaded=True,  # 启用多线程
        use_reloader=False  # 禁用重载器
    )