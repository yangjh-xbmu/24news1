import requests
import json

def inspect_rank_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.bilibili.com/v/popular/rank/kichiku',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': "buvid3=infoc;"
    }
    
    # Using RID 119 (Ghost Animal) as established
    url = "https://api.bilibili.com/x/web-interface/ranking/v2"
    params = {
        'rid': 119,
        'type': 'all',
        'ps': 5,  # Fetch a small number to avoid overwhelming output, though structure is same
    }
    
    try:
        print("Requesting Bilibili Ranking API (RID: 119)...")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        print("\n" + "="*50)
        print("Full Response Structure (First Item Example)")
        print("="*50)
        
        # If there is a list, we'll print the general structure and one full item
        if 'data' in data and 'list' in data['data']:
            rank_list = data['data']['list']
            print(f"Total items in list: {len(rank_list)}")
            
            if rank_list:
                print("\n--- First Video Item Structure ---")
                print(json.dumps(rank_list[0], indent=4, ensure_ascii=False))
                
                # Also print the outer structure without the huge list
                print("\n--- Outer Response Structure (excluding list content) ---")
                data_copy = data.copy()
                data_copy['data'] = data['data'].copy()
                data_copy['data']['list'] = ["<List of items...>"] 
                print(json.dumps(data_copy, indent=4, ensure_ascii=False))
        else:
            # Fallback if structure is different
            print(json.dumps(data, indent=4, ensure_ascii=False))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_rank_data()
