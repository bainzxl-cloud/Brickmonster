# MiniMax Image Generation Setup

## API Key Required

To use MiniMax image generation, you need a MiniMax API key.

### Getting an API Key:

1. Go to: https://platform.minimax.io/
2. Sign up or log in
3. Navigate to API section
4. Generate an API key

### Setting Up the API Key:

#### Option 1: Environment Variable
```bash
# Windows PowerShell
$env:MINIMAX_API_KEY = "your-api-key-here"

# Windows Command Prompt
set MINIMAX_API_KEY=your-api-key-here
```

#### Option 2: Add to .env File
Edit `C:\Users\bainz\.clawdbot\.env`:
```
OPENAI_API_KEY=your-openai-key
MINIMAX_API_KEY=your-minimax-key-here
```

#### Option 3: Run Setup Script
```bash
python setup_minimax_key.py
```

---

## Usage

### Basic Image Generation
```bash
# Generate an image
python minimax_image.py "A sunset over ocean" sunset.png

# With custom aspect ratio
python minimax_image.py "Cute cat" cat.png --aspect-ratio "1:1"
```

### With Reference Image
```bash
python minimax_image.py --reference "https://example.com/ref.jpg" "same person studying" out.png
```

### Available Aspect Ratios
- 16:9 (landscape) - default
- 1:1 (square)
- 9:16 (portrait)
- 3:4 (portrait)
- 4:3 (landscape)
- 3:5 (portrait)
- 5:3 (landscape)
- 9:21 (tall)

---

## Integration with Discord

Once configured, you can:
- 🎨 Generate images from text prompts
- 📸 Use reference images for character consistency
- 🖼️ Send generated images directly to Discord
- 🎯 Create study aids, illustrations, and more!

---

## Quick Start After Getting API Key

```bash
# Set your API key (PowerShell)
$env:MINIMAX_API_KEY = "your-key-here"

# Test generation
python minimax_image.py "A cozy study room with books" test.png
```
