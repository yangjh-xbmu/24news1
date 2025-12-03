import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 获取绝对路径
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '../data/csv/GDP.csv')

# 读取GDP数据
df = pd.read_csv(file_path)

# 提取年份列
year_columns = df.columns[3:]
for col in year_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 绘制折线图
plt.figure(figsize=(12, 8))
for index, row in df.iterrows():
    country = row['Country Name']
    gdp = row[year_columns]
    plt.plot(year_columns, gdp, label=country)

plt.title('各国GDP折线图')
plt.xlabel('年份')
plt.ylabel('GDP')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()