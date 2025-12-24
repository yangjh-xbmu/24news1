import os
import sys
import json
import argparse
import requests

# Configuration
API_KEY = "sk-72698f79f7e3434ea4c77928c22d0774"
API_URL = "https://api.deepseek.com/chat/completions"

class PromptOptimizer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _call_api(self, messages):
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "stream": False
        }
        try:
            response = requests.post(API_URL, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            sys.exit(1)

    def process(self, prompt_text):
        # We combine the modules into a comprehensive system prompt
        system_prompt = """
你是一个高级提示词工程助手。你的目标是优化用户的输入提示词。
你需要应用以下优化模块：

1. **语法分析 (Syntax Analysis)**：修正语法错误，解决歧义，确保清晰度。
2. **语义增强 (Semantic Enhancement)**：扩展提示词以更好地捕捉用户意图，添加必要的上下文。
3. **结构优化 (Structure Optimization)**：将提示词重组为清晰的结构（例如：角色、背景、任务、约束/要求、输出格式）。
4. **关键词强化 (Keyword Reinforcement)**：注入相关的技术术语或领域特定关键词，以更好地引导模型。

请仅以以下 JSON 格式返回响应，不要在 JSON 周围包含 markdown 格式：
{
    "original_prompt": "...",
    "optimized_prompt": "...",
    "changes": {
        "syntax_analysis": "语法修改说明...",
        "semantic_enhancement": "语义增强说明...",
        "structure_optimization": "结构优化说明...",
        "keyword_reinforcement": "关键词添加说明..."
    }
}
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_text}
        ]

        result = self._call_api(messages)
        
        try:
            content = result['choices'][0]['message']['content']
        except (KeyError, IndexError):
            print("Unexpected API response structure.")
            print(json.dumps(result, indent=2))
            sys.exit(1)
        
        # Clean up code blocks if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        try:
            return json.loads(content.strip())
        except json.JSONDecodeError:
            print("Failed to parse API response as JSON. Raw response:")
            print(content)
            # Fallback: try to just return the content as optimized prompt if JSON fails
            return {
                "original_prompt": prompt_text,
                "optimized_prompt": content,
                "changes": {}
            }

def main():
    parser = argparse.ArgumentParser(description="Optimize prompts using DeepSeek API.")
    parser.add_argument("input_file", help="Path to the markdown file containing the input prompt.")
    parser.add_argument("-o", "--output", help="Path to save the optimized prompt (markdown).")
    parser.add_argument("--json", action="store_true", help="Output detailed JSON info to stdout.")
    
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)

    with open(args.input_file, 'r', encoding='utf-8') as f:
        input_prompt = f.read()

    optimizer = PromptOptimizer(API_KEY)
    print("Optimizing prompt...")
    result = optimizer.process(input_prompt)

    optimized_prompt = result.get("optimized_prompt", "")
    
    print("\n" + "="*50)
    print("OPTIMIZED PROMPT")
    print("="*50)
    print(optimized_prompt)
    print("="*50 + "\n")

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(optimized_prompt)
        print(f"Optimized prompt saved to: {args.output}")

if __name__ == "__main__":
    main()
