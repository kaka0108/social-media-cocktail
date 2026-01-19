"""
生成HTML格式的社交媒体菠萝汁鸡尾酒大全
包含博主图片展示
"""

import json
from datetime import datetime
import os


class CocktailHTMLGenerator:
    def __init__(self):
        self.xiaohongshu_data = []
        self.douyin_data = []
        self.combined_data = []
        self.html_content = ""

    def load_sample_data(self):
        """加载示例数据，包含博主图片信息"""
        print("加载示例数据...")

        # 小红书数据 - 8种热门菠萝汁鸡尾酒（包含博主图片）
        self.xiaohongshu_data = [
            {
                "id": 1,
                "source": "小红书",
                "name_zh": "菠萝椰林飘香",
                "name_en": "Pineapple Piña Colada",
                "description": "比传统椰林飘香更突出菠萝风味，小红书热门配方",
                "ingredients": [
                    {"name": "新鲜菠萝汁", "amount": "90ml"},
                    {"name": "白朗姆酒", "amount": "60ml"},
                    {"name": "椰奶", "amount": "45ml"},
                    {"name": "椰子奶油", "amount": "15ml"},
                    {"name": "碎冰", "amount": "适量"}
                ],
                "instructions": [
                    "将新鲜菠萝切块榨汁",
                    "所有液体原料加入搅拌机",
                    "加入大量碎冰",
                    "高速搅拌至顺滑",
                    "倒入飓风杯，用菠萝片装饰"
                ],
                "popularity": 8500,
                "author": "酒鬼少女",
                "author_avatar": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=200&h=200&fit=crop&crop=face",
                "hashtags": ["菠萝鸡尾酒", "椰林飘香", "夏日饮品"],
                "blogger_images": [
                    {
                        "url": "https://images.unsplash.com/photo-1570598912132-0ba1dc952b7d?w=800&h=600&fit=crop",
                        "description": "博主实拍：菠萝椰林飘香成品",
                        "author": "酒鬼少女"
                    },
                    {
                        "url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w-800&h=600&fit=crop",
                        "description": "制作过程实拍",
                        "author": "酒鬼少女"
                    }
                ],
                "color": "#FFD700"
            },
            {
                "id": 2,
                "source": "小红书",
                "name_zh": "夏日菠萝莫吉托",
                "name_en": "Summer Pineapple Mojito",
                "description": "传统莫吉托的菠萝变种，小红书爆款",
                "ingredients": [
                    {"name": "新鲜菠萝汁", "amount": "60ml"},
                    {"name": "白朗姆酒", "amount": "45ml"},
                    {"name": "青柠汁", "amount": "20ml"},
                    {"name": "薄荷叶", "amount": "8-10片"},
                    {"name": "苏打水", "amount": "适量"},
                    {"name": "糖浆", "amount": "15ml"}
                ],
                "instructions": [
                    "杯中放入薄荷叶和糖浆",
                    "轻轻捣压出薄荷香气",
                    "加入朗姆酒、菠萝汁和青柠汁",
                    "加满碎冰",
                    "用苏打水补满",
                    "用菠萝角和薄荷枝装饰"
                ],
                "popularity": 7200,
                "author": "调酒师日记",
                "author_avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop&crop=face",
                "hashtags": ["莫吉托", "菠萝饮品", "自制鸡尾酒"],
                "blogger_images": [
                    {
                        "url": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=800&h=600&fit=crop",
                        "description": "夏日菠萝莫吉托成品展示",
                        "author": "调酒师日记"
                    }
                ],
                "color": "#32CD32"
            },
            {
                "id": 3,
                "source": "小红书",
                "name_zh": "菠萝得其利",
                "name_en": "Pineapple Daiquiri",
                "description": "经典得其利鸡尾酒的菠萝版本，在小红书很受欢迎",
                "ingredients": [
                    {"name": "新鲜菠萝汁", "amount": "60ml"},
                    {"name": "白朗姆酒", "amount": "60ml"},
                    {"name": "青柠汁", "amount": "20ml"},
                    {"name": "糖浆", "amount": "10ml"},
                    {"name": "碎冰", "amount": "适量"}
                ],
                "instructions": [
                    "将所有原料放入调酒壶",
                    "加入少量碎冰",
                    "用力摇匀15秒",
                    "过滤到冰镇的鸡尾酒杯",
                    "用菠萝片装饰"
                ],
                "popularity": 5300,
                "author": "酒吧在家",
                "author_avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&h=200&fit=crop&crop=face",
                "hashtags": ["得其利", "菠萝调酒", "经典改编"],
                "blogger_images": [
                    {
                        "url": "https://images.unsplash.com/photo-1583226566589-5af1df561055?w=800&h=600&fit=crop",
                        "description": "菠萝得其利家庭制作",
                        "author": "酒吧在家"
                    }
                ],
                "color": "#FF6347"
            },
            {
                "id": 4,
                "source": "小红书",
                "name_zh": "菠萝马提尼",
                "name_en": "Pineapple Martini",
                "description": "优雅的菠萝风味马提尼，适合派对场合",
                "ingredients": [
                    {"name": "菠萝汁", "amount": "60ml"},
                    {"name": "伏特加", "amount": "45ml"},
                    {"name": "菠萝利口酒", "amount": "15ml"},
                    {"name": "青柠汁", "amount": "10ml"}
                ],
                "instructions": [
                    "所有原料加冰摇匀",
                    "过滤到冰镇的马提尼杯中",
                    "用菠萝角装饰"
                ],
                "popularity": 4200,
                "author": "派对达人",
                "author_avatar": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=200&h=200&fit=crop&crop=face",
                "hashtags": ["马提尼", "派对饮品", "优雅调酒"],
                "blogger_images": [
                    {
                        "url": "https://images.unsplash.com/photo-1514361892635-6b07e31e75f9?w=800&h=600&fit=crop",
                        "description": "优雅的菠萝马提尼",
                        "author": "派对达人"
                    }
                ],
                "color": "#9370DB"
            },
            {
                "id": 5,
                "source": "小红书",
                "name_zh": "热带菠萝宾治",
                "name_en": "Tropical Pineapple Punch",
                "description": "适合多人派对的菠萝宾治，小红书分享很多",
                "ingredients": [
                    {"name": "菠萝汁", "amount": "500ml"},
                    {"name": "橙汁", "amount": "250ml"},
                    {"name": "朗姆酒", "amount": "200ml"},
                    {"name": "苏打水", "amount": "250ml"},
                    {"name": "青柠汁", "amount": "60ml"},
                    {"name": "糖浆", "amount": "30ml"}
                ],
                "instructions": [
                    "在大容器中混合所有液体原料",
                    "加入大量冰块",
                    "轻轻搅拌",
                    "用菠萝片、橙片和薄荷装饰"
                ],
                "popularity": 6100,
                "author": "派对策划师",
                "author_avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&h=200&fit=crop&crop=face",
                "hashtags": ["宾治", "派对酒", "多人饮品"],
                "blogger_images": [
                    {
                        "url": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&h=600&fit=crop",
                        "description": "派对菠萝宾治大合影",
                        "author": "派对策划师"
                    }
                ],
                "color": "#FF8C00"
            }
        ]

        # 抖音数据 - 7种热门菠萝汁鸡尾酒（包含博主图片）
        self.douyin_data = [
            {
                "id": 101,
                "source": "抖音",
                "name_zh": "菠萝冰沙鸡尾酒",
                "name_en": "Pineapple Smoothie Cocktail",
                "description": "抖音爆款！菠萝冰沙与鸡尾酒的完美结合，视觉味觉双重享受",
                "ingredients": [
                    {"name": "冷冻菠萝块", "amount": "200g"},
                    {"name": "伏特加", "amount": "45ml"},
                    {"name": "椰子水", "amount": "60ml"},
                    {"name": "蜂蜜", "amount": "10ml"},
                    {"name": "柠檬汁", "amount": "15ml"}
                ],
                "instructions": [
                    "冷冻菠萝块提前解冻10分钟",
                    "所有原料放入搅拌机",
                    "搅拌至顺滑冰沙状",
                    "倒入宽口玻璃杯",
                    "用新鲜菠萝叶和吸管装饰"
                ],
                "popularity": 120000,
                "author": "调酒师阿明",
                "author_avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&h=200&fit=crop&crop=face",
                "hashtags": ["菠萝冰沙", "创意调酒", "抖音爆款"],
                "blogger_images": [
                    {
                        "url": "https://images.unsplash.com/photo-1570598912132-0ba1dc952b7d?w=800&h=600&fit=crop",
                        "description": "抖音爆款菠萝冰沙鸡尾酒",
                        "author": "调酒师阿明"
                    },
                    {
                        "url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=600&fit=crop",
                        "description": "制作过程视频截图",
                        "author": "调酒师阿明"
                    }
                ],
                "color": "#FFD700"
            },
            {
                "id": 102,
                "source": "抖音",
                "name_zh": "彩虹菠萝鸡尾酒",
                "name_en": "Rainbow Pineapple Cocktail",
                "description": "抖音热门分层鸡尾酒，色彩绚丽，制作简单",
                "ingredients": [
                    {"name": "菠萝汁", "amount": "60ml"},
                    {"name": "蓝橙利口酒", "amount": "30ml"},
                    {"name": "椰奶", "amount": "30ml"},
                    {"name": "红石榴糖浆", "amount": "15ml"},
                    {"name": "冰块", "amount": "适量"}
                ],
                "instructions": [
                    "杯中加满冰块",
                    "沿吧匙缓缓倒入红石榴糖浆（沉底）",
                    "轻轻倒入椰奶",
                    "再倒入菠萝汁",
                    "最后加入蓝橙利口酒（浮顶）",
                    "不要搅拌，保持分层效果"
                ],
                "popularity": 89000,
                "author": "饮品实验室",
                "author_avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop&crop=face",
                "hashtags": ["彩虹鸡尾酒", "分层饮品", "抖音教程"],
                "blogger_images": [
                    {
                        "url": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&h=600&fit=crop",
                        "description": "彩虹分层效果展示",
                        "author": "饮品实验室"
                    }
                ],
                "color": "#FF1493"
            },
            {
                "id": 103,
                "source": "抖音",
                "name_zh": "烧烤配菠萝啤酒",
                "name_en": "BBQ Pineapple Beer Cocktail",
                "description": "抖音男士最爱，烧烤必备的菠萝啤酒鸡尾酒",
                "ingredients": [
                    {"name": "新鲜菠萝汁", "amount": "150ml"},
                    {"name": "淡色啤酒", "amount": "330ml"},
                    {"name": "伏特加", "amount": "30ml"},
                    {"name": "青柠角", "amount": "2个"},
                    {"name": "薄荷叶", "amount": "少许"}
                ],
                "instructions": [
                    "大啤酒杯中加冰块",
                    "倒入菠萝汁和伏特加",
                    "轻轻搅拌",
                    "缓慢倒入啤酒",
                    "挤入青柠汁",
                    "用青柠角和薄荷装饰"
                ],
                "popularity": 65000,
                "author": "户外美食家",
                "author_avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&h=200&fit=crop&crop=face",
                "hashtags": ["烧烤伴侣", "啤酒调酒", "男士饮品"],
                "blogger_images": [
                    {
                        "url": "https://images.unsplash.com/photo-1546171753-97d7676e4602?w=800&h=600&fit=crop",
                        "description": "烧烤配菠萝啤酒实拍",
                        "author": "户外美食家"
                    }
                ],
                "color": "#8B4513"
            },
            {
                "id": 104,
                "source": "抖音",
                "name_zh": "菠萝泡泡鸡尾酒",
                "name_en": "Pineapple Bubble Cocktail",
                "description": "抖音创意饮品，加入泡泡糖风味，童年回忆",
                "ingredients": [
                    {"name": "菠萝汁", "amount": "80ml"},
                    {"name": "朗姆酒", "amount": "50ml"},
                    {"name": "泡泡糖糖浆", "amount": "20ml"},
                    {"name": "苏打水", "amount": "适量"},
                    {"name": "蛋白", "amount": "1个（可选）"}
                ],
                "instructions": [
                    "摇酒壶中加入除苏打水外的所有原料",
                    "加冰用力摇匀（如用蛋白，需干摇后再加冰摇）",
                    "过滤到加冰的杯中",
                    "用苏打水补满",
                    "装饰泡泡糖和彩色糖粒"
                ],
                "popularity": 78000,
                "author": "创意调酒师",
                "author_avatar": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=200&h=200&fit=crop&crop=face",
                "hashtags": ["创意饮品", "泡泡糖", "抖音热门"],
                "blogger_images": [
                    {
                        "url": "https://images.unsplash.com/photo-1514361892635-6b07e31e75f9?w=800&h=600&fit=crop",
                        "description": "创意泡泡鸡尾酒展示",
                        "author": "创意调酒师"
                    }
                ],
                "color": "#FF69B4"
            },
            {
                "id": 105,
                "source": "抖音",
                "name_zh": "抖音特调菠萝饮",
                "name_en": "Douyin Special Pineapple Drink",
                "description": "抖音网红特调，简单易学，10秒完成",
                "ingredients": [
                    {"name": "菠萝汁", "amount": "100ml"},
                    {"name": "雪碧", "amount": "150ml"},
                    {"name": "蓝莓", "amount": "10颗"},
                    {"name": "薄荷叶", "amount": "5片"},
                    {"name": "冰块", "amount": "适量"}
                ],
                "instructions": [
                    "杯中放入蓝莓和薄荷叶",
                    "轻轻捣压出汁",
                    "加满冰块",
                    "倒入菠萝汁",
                    "用雪碧补满",
                    "轻轻搅拌即可"
                ],
                "popularity": 95000,
                "author": "网红饮品店",
                "author_avatar": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=200&h=200&fit=crop&crop=face",
                "hashtags": ["抖音特调", "网红饮品", "简单调酒"],
                "blogger_images": [
                    {
                        "url": "https://images.unsplash.com/photo-1583226566589-5af1df561055?w=800&h=600&fit=crop",
                        "description": "网红特调菠萝饮",
                        "author": "网红饮品店"
                    }
                ],
                "color": "#00BFFF"
            }
        ]

        print(f"✓ 加载完成：小红书 {len(self.xiaohongshu_data)} 种，抖音 {len(self.douyin_data)} 种")

    def combine_data(self):
        """整合数据"""
        print("整合数据...")
        self.combined_data = self.xiaohongshu_data + self.douyin_data
        print(f"✓ 整合完成，共 {len(self.combined_data)} 种鸡尾酒")

    def generate_html(self):
        """生成包含博主图片的HTML页面"""
        print("生成HTML页面...")

        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>社交媒体菠萝汁鸡尾酒大全 | 小红书 & 抖音热门配方</title>

    <!-- 内联CSS -->
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #333;
            line-height: 1.6;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}

        /* 头部样式 */
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            color: white;
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('https://images.unsplash.com/photo-1570598912132-0ba1dc952b7d?w=1200&h=400&fit=crop') center/cover;
            opacity: 0.2;
            z-index: 0;
        }}

        .header-content {{
            position: relative;
            z-index: 1;
        }}

        .header h1 {{
            font-size: 3rem;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .header .subtitle {{
            font-size: 1.3rem;
            opacity: 0.9;
            margin-bottom: 30px;
        }}

        /* 统计信息 */
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 30px;
        }}

        .stat-card {{
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            min-width: 180px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }}

        .stat-card .number {{
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 5px;
            color: #667eea;
        }}

        .stat-card .label {{
            font-size: 1rem;
            opacity: 0.8;
        }}

        /* 筛选标签 */
        .filter-tags {{
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
            margin: 30px 0;
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}

        .filter-tag {{
            padding: 12px 28px;
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 30px;
            cursor: pointer;
            font-weight: 500;
            font-size: 1rem;
            transition: all 0.3s;
        }}

        .filter-tag:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }}

        .filter-tag.active {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-color: transparent;
            color: white;
        }}

        /* 鸡尾酒网格 */
        .cocktails-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }}

        .cocktail-card {{
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
        }}

        .cocktail-card:hover {{
            transform: translateY(-15px) scale(1.02);
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        }}

        /* 博主图片轮播 */
        .blogger-carousel {{
            position: relative;
            height: 250px;
            overflow: hidden;
            border-radius: 20px 20px 0 0;
        }}

        .carousel-images {{
            display: flex;
            transition: transform 0.5s ease;
            height: 100%;
        }}

        .carousel-image {{
            flex: 0 0 100%;
            height: 100%;
            position: relative;
        }}

        .carousel-image img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .image-overlay {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0,0,0,0.7));
            color: white;
            padding: 15px;
            font-size: 0.9rem;
        }}

        .carousel-nav {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255, 255, 255, 0.8);
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            z-index: 10;
            transition: all 0.3s;
        }}

        .carousel-nav:hover {{
            background: white;
            transform: translateY(-50%) scale(1.1);
        }}

        .carousel-prev {{
            left: 15px;
        }}

        .carousel-next {{
            right: 15px;
        }}

        .carousel-dots {{
            position: absolute;
            bottom: 10px;
            left: 0;
            right: 0;
            display: flex;
            justify-content: center;
            gap: 8px;
            z-index: 10;
        }}

        .carousel-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            cursor: pointer;
            transition: all 0.3s;
        }}

        .carousel-dot.active {{
            background: white;
            transform: scale(1.3);
        }}

        /* 卡片内容 */
        .card-header {{
            padding: 25px 25px 15px;
            position: relative;
        }}

        .platform-badge {{
            position: absolute;
            top: -15px;
            right: 25px;
            padding: 8px 18px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: bold;
            color: white;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}

        .xiaohongshu {{
            background: linear-gradient(135deg, #FF2442, #FF6B9D);
        }}

        .douyin {{
            background: linear-gradient(135deg, #69C9D0, #EE1D52);
        }}

        .author-info {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 15px;
        }}

        .author-avatar {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #f0f0f0;
        }}

        .author-details {{
            flex: 1;
        }}

        .author-name {{
            font-weight: bold;
            color: #333;
            margin-bottom: 3px;
        }}

        .author-platform {{
            font-size: 0.85rem;
            color: #666;
        }}

        .cocktail-name {{
            font-size: 1.6rem;
            color: #2c3e50;
            margin-bottom: 5px;
            font-weight: 600;
        }}

        .cocktail-name-en {{
            font-size: 1rem;
            color: #7f8c8d;
            margin-bottom: 15px;
            font-style: italic;
        }}

        .popularity {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #f39c12;
            font-weight: bold;
            margin-bottom: 20px;
            font-size: 1.1rem;
        }}

        .card-body {{
            padding: 0 25px 25px;
        }}

        .description {{
            color: #555;
            margin-bottom: 25px;
            line-height: 1.7;
            font-size: 1rem;
        }}

        .ingredients-section {{
            margin-bottom: 25px;
        }}

        .section-title {{
            font-size: 1.2rem;
            color: #2c3e50;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
        }}

        .section-title i {{
            color: #667eea;
        }}

        .ingredients-list {{
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 12px;
            padding: 20px;
            border-left: 4px solid #667eea;
        }}

        .ingredient-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }}

        .ingredient-item:last-child {{
            border-bottom: none;
        }}

        .instructions-section {{
            margin-bottom: 25px;
        }}

        .instructions-list {{
            padding-left: 25px;
        }}

        .instructions-list li {{
            margin-bottom: 12px;
            color: #555;
            line-height: 1.6;
            position: relative;
        }}

        .instructions-list li::before {{
            content: '🍍';
            position: absolute;
            left: -25px;
        }}

        .hashtags {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}

        .hashtag {{
            background: linear-gradient(135deg, #e8f4fc, #d4e7fa);
            color: #3498db;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
        }}

        /* 响应式设计 */
        @media (max-width: 768px) {{
            .cocktails-grid {{
                grid-template-columns: 1fr;
            }}

            .header h1 {{
                font-size: 2.2rem;
            }}

            .stats {{
                flex-direction: column;
                align-items: center;
                gap: 15px;
            }}

            .stat-card {{
                width: 100%;
                max-width: 300px;
            }}

            .filter-tags {{
                padding: 15px;
            }}

            .filter-tag {{
                padding: 10px 20px;
                font-size: 0.9rem;
            }}
        }}

        /* 动画效果 */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .cocktail-card {{
            animation: fadeInUp 0.6s ease forwards;
            opacity: 0;
        }}

        /* 页脚 */
        .footer {{
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            border-radius: 20px;
            margin-top: 50px;
        }}

        .footer p {{
            margin-bottom: 10px;
        }}

        .warning {{
            color: #f39c12;
            font-weight: bold;
            font-size: 1.1rem;
            margin: 15px 0;
        }}

        .disclaimer {{
            font-size: 0.9rem;
            opacity: 0.7;
            margin-top: 20px;
        }}

        /* 加载动画 */
        .loading {{
            text-align: center;
            padding: 60px;
            grid-column: 1 / -1;
        }}

        .loading-spinner {{
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }}

        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <header class="header">
            <div class="header-content">
                <h1>🍍 社交媒体菠萝汁鸡尾酒大全</h1>
                <p class="subtitle">收集自小红书 & 抖音平台的12种热门配方，含博主实拍图片</p>

                <div class="stats">
                    <div class="stat-card">
                        <div class="number" id="totalCount">{len(self.combined_data)}</div>
                        <div class="label">总配方数量</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{len(self.xiaohongshu_data)}</div>
                        <div class="label">小红书配方</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{len(self.douyin_data)}</div>
                        <div class="label">抖音配方</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{sum(c['popularity'] for c in self.combined_data):,}</div>
                        <div class="label">总热度</div>
                    </div>
                </div>
            </div>
        </header>

        <!-- 筛选标签 -->
        <div class="filter-tags">
            <button class="filter-tag active" data-platform="all">全部展示 ({len(self.combined_data)})</button>
            <button class="filter-tag" data-platform="xiaohongshu">
                <i class="fas fa-heart" style="color: #FF2442; margin-right: 8px;"></i>
                小红书博主 ({len(self.xiaohongshu_data)})
            </button>
            <button class="filter-tag" data-platform="douyin">
                <i class="fas fa-music" style="color: #69C9D0; margin-right: 8px;"></i>
                抖音博主 ({len(self.douyin_data)})
            </button>
        </div>

        <!-- 鸡尾酒网格 -->
        <div id="cocktailsContainer" class="cocktails-grid">
'''

        # 添加每个鸡尾酒卡片
        for i, cocktail in enumerate(self.combined_data, 1):
            platform_class = "xiaohongshu" if cocktail['source'] == '小红书' else "douyin"
            platform_text = "小红书" if cocktail['source'] == '小红书' else "抖音"

            # 生成博主图片轮播HTML
            carousel_html = ""
            dots_html = ""
            if cocktail.get('blogger_images'):
                for j, image in enumerate(cocktail['blogger_images']):
                    active_class = "active" if j == 0 else ""
                    carousel_html += f'''
                    <div class="carousel-image">
                        <img src="{image['url']}" alt="{image['description']}" loading="lazy">
                        <div class="image-overlay">
                            <div>{image['description']}</div>
                            <div style="font-size: 0.8rem; opacity: 0.9;">by {image['author']}</div>
                        </div>
                    </div>'''
                    dots_html += f'<div class="carousel-dot {active_class}" data-index="{j}"></div>'

                carousel_nav = f'''
                <button class="carousel-nav carousel-prev" onclick="prevSlide(this)">‹</button>
                <button class="carousel-nav carousel-next" onclick="nextSlide(this)">›</button>
                <div class="carousel-dots">
                    {dots_html}
                </div>'''
            else:
                carousel_html = f'''
                <div class="carousel-image">
                    <div style="width: 100%; height: 100%; background: linear-gradient(135deg, {cocktail.get('color', '#667eea')}, #764ba2); 
                         display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem;">
                        <div style="text-align: center;">
                            <i class="fas fa-cocktail" style="font-size: 3rem; margin-bottom: 15px;"></i>
                            <div>{cocktail['name_zh']}</div>
                        </div>
                    </div>
                </div>'''
                carousel_nav = ""

            # 生成配料HTML
            ingredients_html = ""
            for ing in cocktail['ingredients']:
                ingredients_html += f'''
                <div class="ingredient-item">
                    <span>{ing["name"]}</span>
                    <span style="color: #667eea; font-weight: bold;">{ing["amount"]}</span>
                </div>'''

            # 生成步骤HTML
            instructions_html = ""
            for j, step in enumerate(cocktail['instructions'], 1):
                instructions_html += f'<li>{step}</li>'

            # 生成标签HTML
            hashtags_html = ""
            for tag in cocktail['hashtags']:
                hashtags_html += f'<span class="hashtag">#{tag}</span>'

            # 博主头像
            avatar = cocktail.get('author_avatar',
                                  'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=200&h=200&fit=crop&crop=face')

            html += f'''
            <div class="cocktail-card" data-platform="{platform_class}" style="animation-delay: {i * 0.1}s">
                <!-- 博主图片轮播 -->
                <div class="blogger-carousel">
                    <div class="carousel-images" id="carousel-{cocktail['id']}">
                        {carousel_html}
                    </div>
                    {carousel_nav}
                </div>

                <div class="card-header">
                    <span class="platform-badge {platform_class}">
                        <i class="{'fas fa-heart' if platform_class == 'xiaohongshu' else 'fas fa-music'}"></i>
                        {platform_text}
                    </span>

                    <div class="author-info">
                        <img src="{avatar}" alt="{cocktail['author']}" class="author-avatar">
                        <div class="author-details">
                            <div class="author-name">{cocktail['author']}</div>
                            <div class="author-platform">{platform_text}博主</div>
                        </div>
                    </div>

                    <h2 class="cocktail-name">{cocktail['name_zh']}</h2>
                    <p class="cocktail-name-en">{cocktail['name_en']}</p>

                    <div class="popularity">
                        <i class="fas fa-fire"></i>
                        <span>{cocktail['popularity']:,} 热度</span>
                        <i class="fas fa-eye" style="margin-left: 15px;"></i>
                        <span>{(cocktail['popularity'] // 10):,} 浏览</span>
                    </div>
                </div>

                <div class="card-body">
                    <p class="description">{cocktail['description']}</p>

                    <div class="ingredients-section">
                        <h3 class="section-title">
                            <i class="fas fa-list-ul"></i>
                            配料表
                        </h3>
                        <div class="ingredients-list">
                            {ingredients_html}
                        </div>
                    </div>

                    <div class="instructions-section">
                        <h3 class="section-title">
                            <i class="fas fa-martini-glass-citrus"></i>
                            制作步骤
                        </h3>
                        <ol class="instructions-list">
                            {instructions_html}
                        </ol>
                    </div>

                    <div class="hashtags">
                        {hashtags_html}
                    </div>
                </div>
            </div>'''

        html += '''
        </div>

        <!-- 页脚 -->
        <footer class="footer">
            <p>© 2024 社交媒体菠萝汁鸡尾酒大全 | 数据来源：小红书、抖音平台热门内容</p>
            <p class="warning">🚨 温馨提示：图片来源于网络示例，实际请参考博主原帖 🚗</p>
            <p class="warning">🍹 饮酒适量，请勿酒后驾车 🚫</p>
            <p class="disclaimer">
                免责声明：本页面展示的图片仅为示例，版权归原作者所有<br>
                数据更新时间：''' + datetime.now().strftime("%Y年%m月%d日 %H:%M") + '''
            </p>
        </footer>
    </div>

    <!-- JavaScript -->
    <script>
        // 图片轮播功能
        function initCarousel(carouselId, imagesCount) {
            if (imagesCount <= 1) return;

            let currentIndex = 0;
            const carousel = document.getElementById(carouselId);
            const images = carousel.querySelector('.carousel-images');
            const dots = carousel.querySelectorAll('.carousel-dot');

            function updateCarousel() {
                images.style.transform = `translateX(-${currentIndex * 100}%)`;
                dots.forEach((dot, index) => {
                    dot.classList.toggle('active', index === currentIndex);
                });
            }

            // 下一张
            window.nextSlide = function(btn) {
                const carousel = btn.closest('.blogger-carousel');
                const images = carousel.querySelector('.carousel-images');
                const dots = carousel.querySelectorAll('.carousel-dot');
                const totalImages = images.children.length;

                currentIndex = (currentIndex + 1) % totalImages;
                images.style.transform = `translateX(-${currentIndex * 100}%)`;
                dots.forEach((dot, index) => {
                    dot.classList.toggle('active', index === currentIndex);
                });
            }

            // 上一张
            window.prevSlide = function(btn) {
                const carousel = btn.closest('.blogger-carousel');
                const images = carousel.querySelector('.carousel-images');
                const dots = carousel.querySelectorAll('.carousel-dot');
                const totalImages = images.children.length;

                currentIndex = (currentIndex - 1 + totalImages) % totalImages;
                images.style.transform = `translateX(-${currentIndex * 100}%)`;
                dots.forEach((dot, index) => {
                    dot.classList.toggle('active', index === currentIndex);
                });
            }

            // 点击圆点切换
            dots.forEach((dot, index) => {
                dot.addEventListener('click', () => {
                    currentIndex = index;
                    updateCarousel();
                });
            });

            // 自动轮播
            setInterval(() => {
                currentIndex = (currentIndex + 1) % imagesCount;
                updateCarousel();
            }, 5000);
        }

        // 筛选功能
        document.addEventListener('DOMContentLoaded', function() {
            const filterTags = document.querySelectorAll('.filter-tag');
            const cocktailCards = document.querySelectorAll('.cocktail-card');

            // 初始化所有轮播
            cocktailCards.forEach(card => {
                const carouselId = 'carousel-' + card.querySelector('.blogger-carousel').closest('.cocktail-card').getAttribute('data-platform') + card.querySelector('.cocktail-name').textContent;
                const imagesCount = card.querySelectorAll('.carousel-image').length;
                if (imagesCount > 1) {
                    initCarousel(carouselId, imagesCount);
                }
            });

            filterTags.forEach(tag => {
                tag.addEventListener('click', function() {
                    // 更新活动状态
                    filterTags.forEach(t => t.classList.remove('active'));
                    this.classList.add('active');

                    const platform = this.dataset.platform;

                    // 筛选卡片
                    cocktailCards.forEach((card, index) => {
                        if (platform === 'all' || card.dataset.platform === platform) {
                            card.style.display = 'block';
                            setTimeout(() => {
                                card.style.opacity = '1';
                                card.style.transform = 'translateY(0) scale(1)';
                            }, index * 50);
                        } else {
                            card.style.opacity = '0';
                            card.style.transform = 'translateY(20px) scale(0.95)';
                            setTimeout(() => {
                                card.style.display = 'none';
                            }, 300);
                        }
                    });
                });
            });

            // 卡片点击效果
            cocktailCards.forEach(card => {
                card.addEventListener('click', function(e) {
                    if (!e.target.closest('.carousel-nav') && !e.target.closest('.carousel-dot')) {
                        this.style.transform = 'scale(0.98)';
                        setTimeout(() => {
                            this.style.transform = '';
                        }, 150);
                    }
                });
            });

            // 图片懒加载
            const images = document.querySelectorAll('img[loading="lazy"]');
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src || img.src;
                        imageObserver.unobserve(img);
                    }
                });
            });

            images.forEach(img => imageObserver.observe(img));
        });

        // 添加平滑滚动
        window.addEventListener('scroll', function() {
            const cards = document.querySelectorAll('.cocktail-card');
            cards.forEach(card => {
                const rect = card.getBoundingClientRect();
                if (rect.top < window.innerHeight * 0.8) {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }
            });
        });
    </script>
</body>
</html>'''

        self.html_content = html
        print("✓ HTML内容生成完成")

    def save_html(self):
        """保存HTML文件"""
        print("保存HTML文件...")

        filename = 'social_media_cocktails_with_images.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.html_content)

        print(f"✓ HTML文件已保存: {filename}")
        print(f"📁 文件位置: {os.path.abspath(filename)}")

    def generate_and_save(self):
        """生成并保存HTML"""
        self.load_sample_data()
        self.combine_data()
        self.generate_html()
        self.save_html()


# 主程序
if __name__ == "__main__":
    print("=" * 60)
    print("开始生成带博主图片的菠萝汁鸡尾酒HTML页面...")
    print("=" * 60)

    try:
        generator = CocktailHTMLGenerator()
        generator.generate_and_save()

        print("=" * 60)
        print("🎉 HTML页面生成完成！")
        print("=" * 60)
        print("📸 页面特色功能：")
        print("  1. 展示12种热门菠萝汁鸡尾酒（5种小红书 + 7种抖音）")
        print("  2. 博主实拍图片轮播展示")
        print("  3. 博主头像和详细信息")
        print("  4. 平台筛选功能（全部/小红书/抖音）")
        print("  5. 图片懒加载和自动轮播")
        print("  6. 响应式设计，适配各种设备")
        print("  7. 丰富的动画效果和交互功能")
        print("=" * 60)
        print("💡 使用说明：")
        print("  1. 点击左右箭头切换博主图片")
        print("  2. 点击底部圆点直接跳转图片")
        print("  3. 使用筛选标签查看特定平台内容")
        print("  4. 图片支持懒加载，提升加载速度")
        print("=" * 60)
        print("📂 打开 social_media_cocktails_with_images.html 查看效果")
        print("=" * 60)

    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        import traceback

        traceback.print_exc()