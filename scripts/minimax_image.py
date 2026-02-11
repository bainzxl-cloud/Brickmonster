"""
MiniMax Image Generation Integration
Generates images using MiniMax API

Usage:
    python minimax_image.py "Your prompt here" output.png
    python minimax_image.py "A cute bunny in a garden" bunny.png
    python minimax_image.py "Study desk with books" --aspect-ratio "1:1"
"""

import os
import base64
import requests
import sys
import json
from datetime import datetime

# Load API key from environment or config
def get_api_key():
    """Get MiniMax API key from environment."""
    api_key = os.environ.get("MINIMAX_API_KEY")
    
    if not api_key:
        # Try to read from clawdbot config
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", ".clawdbot", ".env")
        try:
            with open(config_path, 'r') as f:
                for line in f:
                    if line.startswith("MINIMAX_API_KEY="):
                        api_key = line.strip().split("=", 1)[1]
                        break
        except:
            pass
    
    return api_key

def generate_image(prompt, output_path, aspect_ratio="16:9", api_key=None):
    """
    Generate an image using MiniMax API.
    
    Args:
        prompt: Text description of the image
        output_path: Path to save the generated image
        aspect_ratio: Image aspect ratio (16:9, 1:1, 9:16, 3:4, 4:3, 3:5, 5:3, 9:21)
        api_key: MiniMax API key (optional, will auto-detect)
    
    Returns:
        tuple: (success: bool, message: str)
    """
    
    if not api_key:
        api_key = get_api_key()
    
    if not api_key:
        return False, "API key not found. Set MINIMAX_API_KEY environment variable."
    
    url = "https://api.minimax.io/v1/image_generation"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": "url",  # Use URL instead of base64
        "n": 1
    }
    
    try:
        print(f"Generating image...")
        print(f"Prompt: {prompt[:100]}...")
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        print(f"Response: {result}")
        
        # Check for different response formats
        images = []
        
        # Format 1: data.image_base64 (old format)
        if "data" in result and "image_base64" in result.get("data", {}):
            images = result["data"]["image_base64"]
        
        # Format 2: data.images[i].url (new format)
        elif "data" in result and "images" in result.get("data", {}):
            for img in result["data"]["images"]:
                if "url" in img:
                    # Download the image
                    img_response = requests.get(img["url"], timeout=30)
                    img_response.raise_for_status()
                    images.append(base64.b64encode(img_response.content).decode('utf-8'))
        
        # Format 3: data.urls (direct URLs)
        elif "data" in result and "urls" in result.get("data", {}):
            for url_item in result["data"]["urls"]:
                if "url" in url_item:
                    img_response = requests.get(url_item["url"], timeout=30)
                    img_response.raise_for_status()
                    images.append(base64.b64encode(img_response.content).decode('utf-8'))
        
        if images:
            image_data = base64.b64decode(images[0])
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "wb") as f:
                f.write(image_data)
            
            file_size = len(image_data)
            return True, f"Image saved: {output_path} ({file_size:,} bytes)"
            
        return False, f"No images in response. Response: {result}"
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error: {e}"
        try:
            error_detail = response.json()
            if "error" in error_detail:
                error_msg = f"API Error: {error_detail['error']}"
        except:
            pass
        return False, error_msg
        
    except Exception as e:
        return False, f"Error: {str(e)}"


def generate_with_reference(prompt, reference_image_url, output_path, aspect_ratio="16:9", api_key=None):
    """
    Generate an image using a reference image.
    
    Args:
        prompt: Text description
        reference_image_url: URL of reference image
        output_path: Path to save
        aspect_ratio: Image aspect ratio
        api_key: MiniMax API key
    """
    
    if not api_key:
        api_key = get_api_key()
    
    if not api_key:
        return False, "API key not found"
    
    url = "https://api.minimax.io/v1/image_generation"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": "base64",
        "subject_reference": [
            {
                "type": "character",
                "image_file": reference_image_url
            }
        ]
    }
    
    try:
        print(f"Generating image with reference...")
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        if "data" in result and "image_base64" in result["data"]:
            images = result["data"]["image_base64"]
            
            if images:
                image_data = base64.b64decode(images[0])
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(output_path, "wb") as f:
                    f.write(image_data)
                
                return True, f"Image saved: {output_path}"
            
        return False, "No images in response"
        
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n" + "="*60)
        print("MINIMAX IMAGE GENERATION")
        print("="*60)
        print('\nExamples:')
        print('  python minimax_image.py "A sunset over ocean" sunset.png')
        print('  python minimax_image.py "Cute cat" cat.png --aspect-ratio "1:1"')
        print('  python minimax_image.py "Study desk" desk.png --aspect-ratio "9:16"')
        print()
        print('With reference image:')
        print('  python minimax_image.py --reference "https://example.com/ref.jpg" "same person studying" out.png')
        print()
        print('Aspect ratios: 16:9, 1:1, 9:16, 3:4, 4:3, 3:5, 5:3, 9:21')
        sys.exit(1)
    
    # Check for reference mode
    if sys.argv[1] == "--reference":
        if len(sys.argv) < 4:
            print("Error: --reference requires reference URL, prompt, and output path")
            sys.exit(1)
        reference_url = sys.argv[2]
        prompt = sys.argv[3]
        output = sys.argv[4] if len(sys.argv) > 4 else "reference_output.png"
        
        success, msg = generate_with_reference(prompt, reference_url, output)
        print(msg)
        sys.exit(0 if success else 1)
    
    # Parse arguments
    prompt = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "minimax_output.png"
    
    aspect_ratio = "16:9"
    for i, arg in enumerate(sys.argv[2:-1]):
        if arg == "--aspect-ratio":
            aspect_ratio = sys.argv[i + 3] if len(sys.argv) > i + 3 else "16:9"
    
    success, msg = generate_image(prompt, output, aspect_ratio)
    print(msg)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
