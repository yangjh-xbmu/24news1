import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import sys

# ==========================================
# 1. 配置区域 (Design Tokens)
# ==========================================
# 视觉风格定义 - 复刻演示文稿的 Dark Theme
STYLE = {
    'bg_color': '#111111',       # 背景色
    'text_primary': '#FFFFFF',   # 主要文字
    'text_secondary': '#AAAAAA', # 次要文字
    'accent_birth': '#FF6B6B',   # 出生率颜色 (红色系-警示)
    'accent_pet': '#00FF88',     # 宠物经济颜色 (绿色系-增长)
    'font_size_title': 16,
    'font_size_label': 12
}

# 数据准备 (Data Preparation)
years = [2018, 2019, 2020, 2021, 2022, 2023]
birth_rate = [10.94, 10.48, 8.52, 7.52, 6.77, 6.39]    # 左轴：出生率 (‰)
pet_market = [1708, 2024, 2953, 3942, 4936, 5928]      # 右轴：市场规模 (亿元)

# ==========================================
# 2. 字体适配逻辑 (OS Adaption)
# ==========================================
def set_chinese_font():
    """
    自动检测系统环境，优先使用微软雅黑/黑体，防止中文乱码
    """
    os_fonts = [
        'Microsoft YaHei',  # Windows
        'SimHei',           # Windows
        'PingFang SC',      # macOS
        'Heiti TC',         # macOS
        'Arial Unicode MS'  # Linux/Universal
    ]
    
    found_font = None
    for font in os_fonts:
        if font in [f.name for f in fm.fontManager.ttflist]:
            found_font = font
            break
            
    if not found_font:
        # 如果找不到常用字体，尝试设置通用 sans-serif
        plt.rcParams['font.sans-serif'] = ['SimHei'] 
        print("⚠️ 未检测到标准中文字体，尝试强制使用 SimHei，如乱码请手动安装字体。")
    else:
        plt.rcParams['font.sans-serif'] = [found_font]
        
    plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

# ==========================================
# 3. 绘图核心逻辑 (Visual Narrative)
# ==========================================
def draw_chart():
    set_chinese_font()
    
    # 创建画布，启用暗色模式
    fig, ax1 = plt.subplots(figsize=(12, 7), facecolor=STYLE['bg_color'])
    ax1.set_facecolor(STYLE['bg_color'])

    # --- 绘制左轴：出生率 (折线图) ---
    color_left = STYLE['accent_birth']
    ax1.set_xlabel('年份', color=STYLE['text_primary'], fontsize=12)
    ax1.set_ylabel('出生率 (‰)', color=color_left, fontsize=12, fontweight='bold')
    
    # 绘制折线
    line = ax1.plot(years, birth_rate, color=color_left, marker='o', 
                   linewidth=4, markersize=8, label='出生率')
    
    # 设置左轴刻度样式
    ax1.tick_params(axis='x', colors=STYLE['text_secondary'])
    ax1.tick_params(axis='y', colors=color_left, labelsize=10)
    ax1.spines['bottom'].set_color(STYLE['text_secondary'])
    ax1.spines['top'].set_color('none') 
    ax1.spines['left'].set_color(color_left)
    ax1.spines['right'].set_visible(False) # 暂时隐藏右脊柱，交给ax2

    # --- 绘制右轴：宠物经济 (柱状图) ---
    # 关键步骤：实例化共享X轴的第二个坐标系
    ax2 = ax1.twinx() 
    color_right = STYLE['accent_pet']
    
    ax2.set_ylabel('宠物市场规模 (亿元)', color=color_right, fontsize=12, fontweight='bold')
    
    # 绘制柱状图 (使用透明度 alpha=0.3 防止遮挡折线)
    bars = ax2.bar(years, pet_market, color=color_right, alpha=0.2, 
                  width=0.5, label='宠物市场')
    
    # 设置右轴刻度样式
    ax2.tick_params(axis='y', colors=color_right, labelsize=10)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set_color(color_right)

    # --- 数据标注 (Data Ink) ---
    # 为折线图添加数值标签
    for x, y in zip(years, birth_rate):
        ax1.text(x, y + 0.3, f"{y}", color=color_left, 
                 ha='center', fontsize=10, fontweight='bold')

    # 为柱状图添加数值标签 (顶部)
    for x, y in zip(years, pet_market):
        ax2.text(x, y + 100, f"{y}", color=color_right, 
                 ha='center', fontsize=9, alpha=0.8)

    # --- 叙事元素 (Storytelling) ---
    # 标题
    plt.title("此消彼长：家庭结构的“一增一减”趋势分析", 
              color=STYLE['text_primary'], 
              fontsize=STYLE['font_size_title'], 
              pad=30, fontweight='bold')
    
    # 来源标注
    fig.text(0.13, 0.02, 
             "数据来源: 国家统计局 / 2023中国宠物行业白皮书", 
             color=STYLE['text_secondary'], 
             fontsize=9, style='italic')

    # 关键洞察标注 (Annotation)
    # 在交叉点附近添加注解
    ax1.annotate('趋势剪刀差', 
                 xy=(2020.5, 8.0),  # 指向的位置
                 xytext=(2019.5, 5.0), # 文字的位置
                 color=STYLE['text_primary'],
                 arrowprops=dict(arrowstyle="->", color='white', connectionstyle="arc3,rad=.2"))

    # 调整布局
    plt.tight_layout()
    
    # 显示图表
    plt.show()

# ==========================================
# 4. 执行入口
# ==========================================
if __name__ == "__main__":
    print("正在生成可视化图表...")
    draw_chart()
    print("图表已生成。")