# 注释，这是一个python文件，在Python中，使用#表示注释

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 赋值语句

major = "新闻学"

print(major)

# 函数

def say_hello(message):
    return f"你好,{message}"

print(say_hello('好好学习'))


def ds(sys_prompt="You are a helpful assistant",user_prompt="hello"):
    # Please install OpenAI SDK first: `pip3 install openai`
    # Please install python-dotenv: `pip3 install python-dotenv`

    from openai import OpenAI

    # 从环境变量读取API密钥
    api_key = os.getenv("DEEPSEEK_KEY")
    if not api_key:
        raise ValueError("DEEPSEEK_KEY环境变量未设置，请检查.env文件")

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ],
        stream=False
    )

    print(response.choices[0].message.content)

ds()

explain_prompt = '''请你扮演一位态度和善、知识渊博的教师，很有耐心地为学生提供概念的解释。'''
ds(explain_prompt,"python中函数的默认值")

# ========== 综合知识点示例 ==========

# 1. Python数据类型
print("\n=== Python数据类型 ===")
# 基本数据类型
name = "张三"           # 字符串 str
age = 20               # 整数 int
height = 175.5         # 浮点数 float
is_student = True      # 布尔值 bool

# 复合数据类型
scores = [85, 92, 78, 96]                    # 列表 list
student_info = {"name": "李四", "age": 19}    # 字典 dict
coordinates = (10, 20)                       # 元组 tuple
subjects = {"数学", "英语", "物理"}            # 集合 set

print(f"姓名: {name} (类型: {type(name)})")
print(f"年龄: {age} (类型: {type(age)})")
print(f"身高: {height} (类型: {type(height)})")
print(f"是否学生: {is_student} (类型: {type(is_student)})")
print(f"成绩列表: {scores} (类型: {type(scores)})")
print(f"学生信息: {student_info} (类型: {type(student_info)})")

# 2. 函数定义和使用
print("\n=== 函数 ===")

def calculate_average(score_list):
    """计算平均分的函数"""
    if not score_list:
        return 0
    return sum(score_list) / len(score_list)

def greet_student(name, grade="大一"):
    """问候学生的函数，带默认参数"""
    return f"你好，{name}同学！欢迎来到{grade}！"

# 函数调用
avg_score = calculate_average(scores)
greeting = greet_student(name)
print(f"平均分: {avg_score:.2f}")
print(greeting)

# 3. 类和对象
print("\n=== 类和对象 ===")

class Student:
    """学生类"""
    
    # 类变量
    school_name = "某某大学"
    
    def __init__(self, name, age, major):
        """构造函数"""
        self.name = name        # 实例变量
        self.age = age
        self.major = major
        self.scores = []
    
    def add_score(self, score):
        """添加成绩的方法"""
        if 0 <= score <= 100:
            self.scores.append(score)
            return True
        return False
    
    def get_average(self):
        """获取平均分的方法"""
        return calculate_average(self.scores)
    
    def introduce(self):
        """自我介绍的方法"""
        avg = self.get_average()
        return f"我是{self.name}，{self.age}岁，专业是{self.major}，平均分是{avg:.2f}"
    
    @classmethod
    def get_school_info(cls):
        """类方法"""
        return f"我们都来自{cls.school_name}"
    
    @staticmethod
    def is_pass(score):
        """静态方法"""
        return score >= 60

# 创建对象
student1 = Student("王五", 19, "计算机科学")
student2 = Student("赵六", 20, "数据科学")

# 使用对象方法
student1.add_score(85)
student1.add_score(92)
student1.add_score(78)

student2.add_score(88)
student2.add_score(95)
student2.add_score(82)

print(student1.introduce())
print(student2.introduce())
print(Student.get_school_info())
print(f"85分是否及格: {Student.is_pass(85)}")

# 4. 流程控制
print("\n=== 流程控制 ===")

# 条件判断
def evaluate_grade(score):
    """根据分数评定等级"""
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 70:
        return "中等"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"

# for循环
print("所有学生成绩评定:")
all_students = [student1, student2]
for student in all_students:
    print(f"{student.name}的成绩:")
    for i, score in enumerate(student.scores):
        grade = evaluate_grade(score)
        print(f"  第{i+1}次考试: {score}分 - {grade}")

# while循环
print("\n成绩统计:")
total_scores = []
for student in all_students:
    total_scores.extend(student.scores)

# 统计各等级人数
grade_count = {"优秀": 0, "良好": 0, "中等": 0, "及格": 0, "不及格": 0}
i = 0
while i < len(total_scores):
    grade = evaluate_grade(total_scores[i])
    grade_count[grade] += 1
    i += 1

for grade, count in grade_count.items():
    if count > 0:
        print(f"{grade}: {count}人次")

# 列表推导式（高级流程控制）
high_scores = [score for score in total_scores if score >= 85]
print(f"\n85分以上的成绩: {high_scores}")

# 异常处理
print("\n=== 异常处理 ===")
def safe_divide(a, b):
    """安全除法函数"""
    try:
        result = a / b
        return f"{a} ÷ {b} = {result}"
    except ZeroDivisionError:
        return "错误: 除数不能为零"
    except TypeError:
        return "错误: 参数类型不正确"
    finally:
        print("除法运算完成")

print(safe_divide(10, 2))
print(safe_divide(10, 0))

print("\n=== 程序结束 ===")
