"""
Quick API Key Setup for MiniMax Image Generation
"""

import os

print("="*60)
print("MINIMAX API KEY SETUP")
print("="*60)
print()
print("Enter your MiniMax API key to enable image generation.")
print("Your key is used for the AI model (MiniMax-M2.1).")
print()

api_key = input("Enter your MiniMax API key: ").strip()

if not api_key:
    print("❌ No key entered.")
    input("Press Enter to exit...")
    exit(1)

# Save to .env file
env_path = r"C:\Users\bainz\.clawdbot\.env"

# Read existing content
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

print()
print("✅ API key saved!")
print()
print("You can now generate images with:")
print("  python minimax_image.py \"Your prompt\" output.png")
print()

input("Press Enter to exit...")
