"""
MiniMax Image Generation - Test without Bearer
"""

import os
import base64
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

def generate_image(prompt, output_path, aspect_ratio="1:1"):
    api_key = get_api_key()
    
    if not api_key:
        return False, "API key not found"
    
    url = "https://api.minimax.io/v1/image_generation"
    
    # Try WITHOUT "Bearer" prefix - just the key directly
    headers = {
        "Authorization": api_key,  # Just the key, no Bearer
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": "url"
    }
    
    try:
        print(f"Testing WITHOUT Bearer prefix...")
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        return True, "Done"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    import sys
    prompt = sys.argv[1] if len(sys.argv) > 1 else "A cute bunny"
    output = sys.argv[2] if len(sys.argv) > 2 else "test.png"
    ratio = sys.argv[3] if len(sys.argv) > 3 else "1:1"
    
    success, msg = generate_image(prompt, output, ratio)
    print(msg)
