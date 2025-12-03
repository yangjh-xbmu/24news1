import jieba
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import random
import platform
import os

# ==========================================
# 1. 模拟数据 (直接定义清洗后的词频趋势)
# ==========================================
# 相比于拼接字符串，直接定义权重能更精准地控制"舆论风向"
# 这模拟了 jieba 分词 + 停用词过滤后的最终统计结果
frequency_data = {
    # --- 核心高频词 (Core) ---
    "黑神话": 100,
    "悟空": 95,
    "国产之光": 88,
    "游戏科学": 85,
    "西游记": 80,
    
    # --- 正面评价 (Positive) ---
    "文化输出": 75,
    "美术": 72,
    "震撼": 70,
    "3A大作": 68,
    "天命人": 65,
    "细节": 60,
    "BGM": 58,
    "陕北说书": 55,
    "第一章": 50,
    "杨奇": 48,
    
    # --- 负面/争议/硬件 (Negative/Tech) ---
    "显卡": 45,      # 关注度高
    "优化": 42,
    "空气墙": 40,    # 核心槽点
    "掉帧": 38,
    "晕3D": 35,
    "迷路": 32,
    "难度": 30,
    "虎先锋": 28,
    "闪退": 25,
    
    # --- 中性/其他 (Neutral) ---
    "Steam": 40,
    "销量": 38,
    "剧情": 35,
    "虚幻5": 30,
    "打击感": 28,
    "冯骥": 25,
    "配置": 22,
    "PS5": 20,
    "手柄": 18,
    "直面天命": 15
}

# ==========================================
# 2. 视觉风格定义 (Neon Style)
# ==========================================
COLOR_PALETTE = [
    "#00ff88", # 核心亮绿 (高频)
    "#00cc77", # 中绿
    "#66ffaa", # 浅绿
    "#ffffff", # 纯白 (强调)
    "#eeeeee", # 灰白
    "#cccccc"  # 浅灰 (低频)
]

def neon_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """
    根据词频大小动态调整颜色策略（可选高级玩法）：
    这里为了保持视觉统一，依然采用随机霓虹色
    """
    return random.choice(COLOR_PALETTE)

# ==========================================
# 3. 系统字体路径获取
# ==========================================
def get_font_path():
    system = platform.system()
    if system == "Windows":
        paths = ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/simhei.ttf"]
    elif system == "Darwin": # macOS
        paths = ["/System/Library/Fonts/PingFang.ttc", "/Library/Fonts/Arial Unicode.ttf"]
    else:
        paths = ["/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"]
    
    for p in paths:
        if os.path.exists(p): return p
    return None

# ==========================================
# 4. 核心生成逻辑 (From Frequencies)
# ==========================================
def generate_precise_cloud():
    font_path = get_font_path()
    if not font_path:
        print("❌ 未找到中文字体，请手动指定路径")
        return

    print("正在生成高精度词云...")

    # 创建圆形遮罩
    x, y = np.ogrid[:800, :800]
    mask = (x - 400) ** 2 + (y - 400) ** 2 > 380 ** 2
    mask = 255 * mask.astype(int)

    # 实例化 WordCloud
    wc = WordCloud(
        font_path=font_path,
        background_color="black", # 适配 PPT 深色背景
        width=1000,
        height=1000,
        max_words=200,
        mask=mask,
        
        # --- 关键优化参数 ---
        repeat=False,             # 严格禁止重复单词
        collocations=False,       # 🚫 关闭二元词组统计 (彻底解决重复问题的核心)
        prefer_horizontal=0.9,    # 90% 的词横向排版，提高可读性
        min_font_size=10,
        max_font_size=150,
        relative_scaling=0.6,     # 词频与字号的相关性 (0.5-1.0之间)
        
        # --- 视觉修饰 ---
        contour_width=2,
        contour_color='#333333',  # 淡淡的边框
        color_func=neon_color_func
    )

    # 【关键步骤】使用 generate_from_frequencies 代替 generate
    # 这跳过了 wordcloud 内部的分词和统计步骤，直接渲染我们给定的结果
    wc.generate_from_frequencies(frequency_data)

    # ==========================================
    # 5. 绘图展示
    # ==========================================
    plt.figure(figsize=(10, 10), facecolor='#111111') # 窗口背景
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    
    print("✅ 词云已生成！(已去除所有重复词)")
    plt.show()

if __name__ == "__main__":
    generate_precise_cloud()