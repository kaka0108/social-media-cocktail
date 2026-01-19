import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://data.eastmoney.com/xg/kzz/default_{}.html"  # 根据实际情况调整URL
all_data = []

for page in range(1, 21):  # 抓取第1至20页的数据
    print(f"正在抓取第{page}页...")
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 解析HTML，根据实际网页结构调整选择器
    table = soup.find('table', {'class': 'list-table'})  # 示例选择器，请根据实际情况调整
    if table:
        for row in table.find_all('tr')[1:]:  # 跳过表头行
            cols = row.find_all('td')
            cols_text = [ele.text.strip() for ele in cols]
            all_data.append(cols_text)

# 将数据转换为DataFrame
df = pd.DataFrame(all_data, columns=["列名1", "列名2", "列名3", "..."])  # 根据实际情况填写列名

# 导出到Excel
df.to_excel("all_pages_data.xlsx", index=False)
print("数据已保存到all_pages_data.xlsx")