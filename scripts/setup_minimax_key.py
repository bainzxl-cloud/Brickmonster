"""
MiniMax API Key Setup Script
Helps you configure your MiniMax API key for image generation
"""

import os
import sys

def setup_api_key():
    """Guide user through API key setup."""
    
    print("="*60)
    print("MINIMAX IMAGE GENERATION - API KEY SETUP")
    print("="*60)
    print()
    
    # Check current setup
    env_key = os.environ.get("MINIMAX_API_KEY")
    
    env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".clawdbot", ".env")
    
    # Check .env file
    env_file_key = None
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("MINIMAX_API_KEY="):
                    env_file_key = line.strip().split("=", 1)[1]
                    break
    
    print("Current Status:")
    print("-" * 30)
    print(f"Environment variable: {'✅ Set' if env_key else '❌ Not set'}")
    print(f".env file: {'✅ Has key' if env_file_key else '❌ No key'}")
    print()
    
    if env_key or env_file_key:
        print("✅ MiniMax API key appears to be configured!")
        print()
        print("You can now generate images with:")
        print("  python minimax_image.py \"Your prompt\" output.png")
        return True
    
    print("❌ MiniMax API key not found.")
    print()
    print("To get an API key:")
    print("1. Go to: https://platform.minimax.io/")
    print("2. Sign up / Log in")
    print("3. Navigate to API section")
    print("4. Generate an API key")
    print()
    
    # Ask user if they have a key
    choice = input("Do you have a MiniMax API key? (y/n): ").strip().lower()
    
    if choice != 'y':
        print()
        print("No problem! Get your API key from MiniMax first, then run this script again.")
        return False
    
    # Get API key from user
    print()
    api_key = input("Enter your MiniMax API key: ").strip()
    
    if not api_key:
        print("❌ No key entered.")
        return False
    
    # Save to .env file
    print()
    print("Saving API key to .env file...")
    
    env_content = ""
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            env_content = f.read()
    
    # Remove existing MINIMAX_API_KEY if present
    lines = env_content.split('\n')
    new_lines = []
    for line in lines:
        if not line.startswith("MINIMAX_API_KEY="):
            new_lines.append(line)
    
    # Add new key
    new_lines.append(f"MINIMAX_API_KEY={api_key}")
    env_content = '\n'.join(new_lines)
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("✅ API key saved to .env file!")
    print()
    
    # Also set environment variable for current session
    os.environ["MINIMAX_API_KEY"] = api_key
    print("✅ Environment variable set for this session!")
    print()
    
    print("="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print()
    print("You can now generate images with:")
    print("  python minimax_image.py \"A beautiful sunset\" sunset.png")
    print()
    print("Note: You may need to restart your terminal for the")
    print("environment variable to persist across sessions.")
    
    return True


if __name__ == "__main__":
    success = setup_api_key()
    sys.exit(0 if success else 1)
