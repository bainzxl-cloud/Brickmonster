"""
MiniMax Image Generation - Test different auth formats
"""

import os
import requests

def get_api_key():
    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", ".clawdbot", ".env")
        try:
            with open(config_path, 'r') as f:
                for line in f:
                    if line.startswith("MINIMAX_API_KEY="):
                        return line.strip().split("=", 1)[1]
        except:
            pass
    return api_key

def test_auth_format(api_key, format_name, extra_prefix=""):
    url = "https://api.minimax.io/v1/image_generation"
    
    auth_header = f"{extra_prefix}{api_key}".strip()
    
    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "image-01",
        "prompt": "A cute bunny",
        "aspect_ratio": "1:1",
        "response_format": "url"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"{format_name}: Status {response.status_code}")
        print(f"  Response: {response.text[:200]}")
        return response.status_code, response.text
    except Exception as e:
        print(f"{format_name}: Error - {e}")
        return None, str(e)

if __name__ == "__main__":
    api_key = get_api_key()
    
    if not api_key:
        print("API key not found!")
        exit(1)
    
    print(f"Testing API key: {api_key[:15]}...")
    print()
    
    # Test different formats
    test_auth_format(api_key, "1. Just key (no prefix)")
    test_auth_format(api_key, "2. Bearer key", "Bearer ")
    test_auth_format(api_key, "3. MiniMax key", "MiniMax ")
    test_auth_format(api_key, "4. API-Key key", "API-Key ")
