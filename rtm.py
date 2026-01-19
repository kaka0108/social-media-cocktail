import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches
from matplotlib.table import Table

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建数据
data = {
    'Channel': ['现代渠道', '现代渠道', '现代渠道', '现代渠道', '现代渠道', '现代渠道', '现代渠道', '现代渠道',
                '线上渠道', '餐饮渠道', '餐饮渠道', '餐饮渠道'],
    'subchannel': ['HM/SM', 'Sams', 'CVS', 'Costco', 'HM/SM', 'Sams', 'CVS', 'Costco',
                   '直营EC', 'PRIVATE LABEL', 'hOREKA', 'BAKERY'],
    'Category': ['罐头', '罐头', '罐头', '罐头', '果干', '果干', '果干', '果干',
                 '碳酸饮料', '罐头', '罐头', '罐头'],
    'Store_Count': [25000, 25000, 18000, 22000, 800, 1000, 2000, 3000,
                    85000, 22000, 100, 2000]
}

df = pd.DataFrame(data)

# 数据汇总
channel_totals = df.groupby('Channel')['Store_Count'].sum()
subchannel_totals = df.groupby(['Channel', 'subchannel'])['Store_Count'].sum()
category_totals = df.groupby('Category')['Store_Count'].sum()

# 获取所有子渠道列表（按渠道分组）
subchannels_by_channel = {}
for channel in channel_totals.index:
    subchannels = df[df['Channel'] == channel]['subchannel'].unique()
    subchannels_by_channel[channel] = subchannels

# 获取所有品类列表
categories = category_totals.index.tolist()

# 设置颜色
channel_colors = {
    '现代渠道': '#1f77b4',  # 蓝色
    '线上渠道': '#2ca02c',  # 绿色
    '餐饮渠道': '#ff7f0e'  # 橙色
}

subchannel_colors = {
    'HM/SM': '#4c72b0', 'Sams': '#55a868', 'CVS': '#c44e52', 'Costco': '#8172b2',
    '直营EC': '#2ca02c', 'PRIVATE LABEL': '#ff7f0e', 'hOREKA': '#ffbb78', 'BAKERY': '#ff9896'
}

# 创建组合图表
fig = plt.figure(figsize=(20, 16))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.2], hspace=0.1)

# 上半部分：渠道-子渠道层级结构
ax1 = fig.add_subplot(gs[0])

# 第一层：渠道
channel_level = 8
channel_positions = {}
channel_width = 4

# 计算渠道位置
total_subchannels = sum(len(subchannels) for subchannels in subchannels_by_channel.values())
x_positions = np.linspace(2, 18, len(channel_totals))

for i, (channel, total) in enumerate(channel_totals.items()):
    x_pos = x_positions[i]
    channel_positions[channel] = x_pos

    # 绘制渠道框
    box = FancyBboxPatch((x_pos - channel_width / 2, channel_level),
                         channel_width, 1.0,
                         boxstyle="round,pad=0.3",
                         facecolor=channel_colors[channel],
                         edgecolor='black',
                         alpha=0.9,
                         linewidth=2)
    ax1.add_patch(box)

    # 添加渠道文本
    ax1.text(x_pos, channel_level + 0.5, channel,
             ha='center', va='center', fontweight='bold', fontsize=14, color='white')
    ax1.text(x_pos, channel_level + 0.1, f'{total:,}家',
             ha='center', va='center', fontsize=12, color='white', fontweight='bold')

# 第二层：子渠道
subchannel_level = 4
subchannel_positions = {}

for channel in channel_totals.index:
    base_x = channel_positions[channel]
    subchannels = subchannels_by_channel[channel]

    # 计算子渠道位置（均匀分布）
    subchannel_x_positions = np.linspace(base_x - 3, base_x + 3, len(subchannels))

    for j, subchannel in enumerate(subchannels):
        x_pos = subchannel_x_positions[j]
        total = subchannel_totals[(channel, subchannel)]
        subchannel_positions[(channel, subchannel)] = x_pos

        # 绘制连接线
        ax1.plot([base_x, x_pos], [channel_level - 0.5, subchannel_level + 0.6],
                 'k-', alpha=0.7, linewidth=2, color='gray')

        # 绘制子渠道框
        box_width = 2.8
        box = FancyBboxPatch((x_pos - box_width / 2, subchannel_level),
                             box_width, 0.8,
                             boxstyle="round,pad=0.2",
                             facecolor=subchannel_colors[subchannel],
                             edgecolor='black',
                             alpha=0.8,
                             linewidth=1.5)
        ax1.add_patch(box)

        # 添加子渠道文本
        ax1.text(x_pos, subchannel_level + 0.5, subchannel,
                 ha='center', va='center', fontweight='bold', fontsize=11, color='white')
        ax1.text(x_pos, subchannel_level + 0.2, f'{total:,}家',
                 ha='center', va='center', fontsize=10, color='white', fontweight='bold')

# 设置层级图范围
ax1.set_xlim(0, 20)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title('销售渠道组织架构层级图', fontsize=18, fontweight='bold', pad=20)

# 下半部分：品类门店数分布表格（与上半部分对齐）
ax2 = fig.add_subplot(gs[1])
ax2.axis('off')

# 准备表格数据
# 列头：渠道 + 子渠道（与上半部分顺序一致）
table_columns = ['品类']
for channel in channel_totals.index:
    for subchannel in subchannels_by_channel[channel]:
        table_columns.append(f'{channel}\n{subchannel}')
table_columns.append('品类总计')

# 行数据：每个品类在各子渠道的门店数
table_data = []
for category in categories:
    row_data = [category]
    total_category = 0

    for channel in channel_totals.index:
        for subchannel in subchannels_by_channel[channel]:
            # 获取该子渠道该品类的门店数
            count = df[(df['Channel'] == channel) &
                       (df['subchannel'] == subchannel) &
                       (df['Category'] == category)]['Store_Count'].sum()
            row_data.append(f'{count:,}' if count > 0 else '-')
            total_category += count

    row_data.append(f'{total_category:,}')
    table_data.append(row_data)

# 添加总计行
total_row = ['渠道总计']
total_overall = 0

for channel in channel_totals.index:
    for subchannel in subchannels_by_channel[channel]:
        total = subchannel_totals[(channel, subchannel)]
        total_row.append(f'{total:,}')
        total_overall += total

total_row.append(f'{total_overall:,}')
table_data.append(total_row)

# 创建表格
table = ax2.table(cellText=table_data,
                  colLabels=table_columns,
                  cellLoc='center',
                  loc='center',
                  bbox=[0, 0.1, 1, 0.9])

# 设置表格样式
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.8)

# 设置表头样式
for j in range(len(table_columns)):
    table[(0, j)].set_facecolor('#2E86AB')
    table[(0, j)].set_text_props(weight='bold', color='white', size=10)

# 设置数据行样式
for i in range(1, len(table_data)):
    for j in range(len(table_columns)):
        if j == 0:  # 品类列
            table[(i, j)].set_facecolor('#E8F4F8')
            table[(i, j)].set_text_props(weight='bold')
        elif j == len(table_columns) - 1:  # 总计列
            table[(i, j)].set_facecolor('#FFE66D')
            table[(i, j)].set_text_props(weight='bold')
        else:  # 数据单元格
            # 根据渠道设置背景色
            col_header = table_columns[j]
            for channel, color in channel_colors.items():
                if channel in col_header:
                    table[(i, j)].set_facecolor(color + '40')  # 40表示透明度
                    break

        # 设置总计行样式
        if i == len(table_data) - 1:
            table[(i, j)].set_facecolor('#FFD700')
            table[(i, j)].set_text_props(weight='bold')

# 添加表格标题
ax2.set_title('各子渠道品类门店数分布表', fontsize=16, fontweight='bold', pad=20, y=0.95)

# 添加总体统计信息
total_stores = df['Store_Count'].sum()
fig.text(0.5, 0.02, f'总计覆盖门店数: {total_stores:,}家 | 数据统计时间: 2024年',
         ha='center', fontsize=12,
         bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.8))

plt.tight_layout()

# 显示图表
plt.show()

# 保存图表
plt.savefig('销售渠道层级与品类分布对应图.png', dpi=300, bbox_inches='tight', facecolor='white')

# 输出统计摘要
print("=" * 70)
print("销售渠道层级与品类分布统计摘要")
print("=" * 70)
print(f"总覆盖门店数: {total_stores:,}家")

print(f"\n🏪 渠道统计:")
for channel, total in channel_totals.items():
    percentage = (total / total_stores) * 100
    print(f"  {channel}: {total:,}家 ({percentage:.1f}%)")

print(f"\n📊 子渠道统计:")
for (channel, subchannel), total in subchannel_totals.items():
    percentage = (total / total_stores) * 100
    print(f"  {channel} - {subchannel}: {total:,}家 ({percentage:.1f}%)")

print(f"\n📦 品类统计:")
for category, total in category_totals.items():
    percentage = (total / total_stores) * 100
    print(f"  {category}: {total:,}家 ({percentage:.1f}%)")