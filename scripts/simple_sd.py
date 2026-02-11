"""
Simple Stable Diffusion - Python Library Version
Uses Hugging Face diffusers for easy image generation

Requirements:
- Python 3.10+
- PyTorch with CUDA support
- Hugging Face diffusers

Usage:
    python simple_sd.py "Your prompt here" output.png
"""

import os
import sys

def check_requirements():
    """Check if required packages are installed."""
    print("="*60)
    print("CHECKING REQUIREMENTS")
    print("="*60)
    
    # Check Python version
    py_version = sys.version_info
    print(f"Python version: {sys.version}")
    
    if py_version.major == 3 and py_version.minor >= 10:
        print("✅ Python 3.10+ found")
    else:
        print("❌ Python 3.10+ required")
        print("   Current version:", sys.version)
        return False
    
    # Check PyTorch
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        else:
            print("⚠️  CUDA not available - will use CPU (slow!)")
    except ImportError:
        print("❌ PyTorch not installed")
        return False
    
    # Check diffusers
    try:
        from diffusers import StableDiffusionPipeline
        print("✅ Diffusers library installed")
    except ImportError:
        print("❌ Diffusers not installed")
        return False
    
    # Check transformers
    try:
        from transformers import CLIPTextModel
        print("✅ Transformers library installed")
    except ImportError:
        print("❌ Transformers not installed")
        return False
    
    return True

def install_requirements():
    """Install required packages."""
    print("\n" + "="*60)
    print("INSTALLING REQUIREMENTS")
    print("="*60)
    
    print("Installing PyTorch with CUDA support...")
    print("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
    
    print("\nInstalling Diffusers...")
    print("pip install diffusers transformers accelerate")
    
    print("\n" + "="*60)
    print("📌 MANUAL INSTALLATION NEEDED")
    print("="*60)
    print("""
Run these commands in PowerShell/Command Prompt:

1. Install PyTorch with CUDA:
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

2. Install diffusers:
   pip install diffusers transformers accelerate

3. Run this script again:
   python simple_sd.py "A cute bunny" bunny.png
    """)

def generate_image(prompt, output_path="test.png", negative_prompt=None):
    """Generate an image using Stable Diffusion."""
    print("\n" + "="*60)
    print("GENERATING IMAGE")
    print("="*60)
    print(f"Prompt: {prompt}")
    print(f"Output: {output_path}")
    
    try:
        import torch
        from diffusers import StableDiffusionPipeline
        
        print("\nLoading Stable Diffusion model...")
        print("This may take a few minutes on first run (downloading ~4GB)...")
        
        # Use a smaller model for RTX 4050 (6GB VRAM)
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            safety_checker=None  # Disable for speed
        )
        
        # Move to GPU
        pipe = pipe.to("cuda")
        
        print("Model loaded! Generating image...")
        
        # Generate
        image = pipe(
            prompt,
            negative_prompt=negative_prompt or "low quality, blurry, distorted",
            num_inference_steps=50,
            guidance_scale=7.5,
            height=512,
            width=512
        ).images[0]
        
        # Save
        image.save(output_path)
        print(f"\n✅ Image saved: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("="*60)
    print("🎨 SIMPLE STABLE DIFFUSION")
    print("="*60)
    print("\nThis script generates images using Hugging Face Diffusers")
    print("Works with your RTX 4050 GPU!")
    
    # Check requirements
    if not check_requirements():
        install_requirements()
        return
    
    # Get prompt from command line
    if len(sys.argv) < 2:
        print("\n" + "="*60)
        print("USAGE")
        print("="*60)
        print("""
Generate an image:
    python simple_sd.py "Your prompt here" output.png

With negative prompt:
    python simple_sd.py "A cute bunny" bunny.png "no watermark, no text"

Examples:
    python simple_sd.py "A sunset over ocean" sunset.png
    python simple_sd.py "Cute bunny studying" bunny_study.png
    python simple_sd.py "Cozy study room" study_room.png
        """)
        return
    
    prompt = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "sd_output.png"
    negative = sys.argv[3] if len(sys.argv) > 3 else None
    
    success = generate_image(prompt, output, negative)
    
    if success:
        print("\n🎉 Image generated successfully!")
        print(f"📁 Saved to: {output}")

if __name__ == "__main__":
    main()
