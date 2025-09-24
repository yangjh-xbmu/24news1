import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

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

    # print(response.choices[0].message.content)
    return response.choices[0].message.content

提示词_解释概念 = """请为概念生成一个详细的解释文档。

请按照以下结构组织内容：

## 简明定义
用1-2句话简洁地定义这个概念。

## 核心思想/原理
详细解释概念的核心思想、工作原理或基本机制。

## 举例说明
提供2-3个具体的例子来说明这个概念的应用。

## 优点
列出使用这个概念的主要优势。

## 缺点
列出可能的局限性或缺点。

## 类比
用一个生活中的类比来帮助理解这个概念。

请确保内容准确、易懂，适合学习者理解。"""

def explains(concept):
    return ds(提示词_解释概念,concept)