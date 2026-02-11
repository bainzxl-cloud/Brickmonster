"""
Stable Diffusion Complete Setup - One Click Install
Installs all dependencies and sets up image generation

Run this script to install everything needed for Stable Diffusion!
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    print(f"\n{'='*60}")
    print(description)
    print(f"{'='*60}")
    print(f"Command: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr}")
    
    return result.returncode

def check_python():
    print("\n" + "="*60)
    print("CHECKING PYTHON")
    print("="*60)
    
    result = run_command("python --version", "Python version")
    
    if result == 0:
        print("Python is installed!")
        return True
    else:
        print("Python not found. Installing Python 3.10...")
        return False

def install_pytorch():
    print("\n" + "="*60)
    print("INSTALLING PYTORCH WITH CUDA")
    print("="*60)
    
    cmd = 'pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121'
    return run_command(cmd, "Installing PyTorch")

def install_diffusers():
    print("\n" + "="*60)
    print("INSTALLING DIFFUSERS")
    print("="*60)
    
    cmd = 'pip install diffusers transformers accelerate'
    return run_command(cmd, "Installing diffusers")

def install_requirements():
    print("\n" + "="*60)
    print("INSTALLING ALL REQUIREMENTS")
    print("="*60)
    
    install_pytorch()
    install_diffusers()
    
    print("\n" + "="*60)
    print("INSTALLATION COMPLETE!")
    print("="*60)

def test_installation():
    print("\n" + "="*60)
    print("TESTING INSTALLATION")
    print("="*60)
    
    # Test PyTorch
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"CUDA available: {torch.cuda.get_device_name(0)}")
            return True
        else:
            print("CUDA not available - will use CPU")
            return True
    except ImportError as e:
        print(f"PyTorch import error: {e}")
        return False

def generate_test_image():
    print("\n" + "="*60)
    print("GENERATING TEST IMAGE")
    print("="*60)
    print("This will download the model on first run (~4GB)")
    print("Generating: 'A cute bunny reading a book'\n")
    
    script = '''
import os
import sys

try:
    import torch
    from diffusers import StableDiffusionPipeline
    
    print("Loading model...")
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16,
        safety_checker=None
    )
    pipe = pipe.to("cuda")
    
    print("Generating image...")
    image = pipe(
        "A cute bunny reading a book",
        num_inference_steps=50,
        guidance_scale=7.5
    ).images[0]
    
    output_path = os.path.join(os.path.dirname(__file__), "..", "test_bunny_sd.png")
    image.save(output_path)
    print(f"Image saved: {output_path}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
'''
    
    # Write and run test script
    test_script_path = "test_sd_gen.py"
    with open(test_script_path, 'w') as f:
        f.write(script)
    
    return run_command(f"python {test_script_path}", "Generating test image")

def main():
    print("="*60)
    print("STABLE DIFFUSION SETUP")
    print("="*60)
    print("This will set up AI image generation on your RTX 4050!")
    print("Estimated time: 5-10 minutes")
    
    # Check if already installed
    try:
        import torch
        from diffusers import StableDiffusionPipeline
        print("\n Stable Diffusion is already installed!")
        
        choice = input("\nGenerate a test image? (y/n): ").strip().lower()
        if choice == 'y':
            generate_test_image()
        return
    except ImportError:
        print("\nSetting up Stable Diffusion...")
    
    # Install requirements
    install_requirements()
    
    # Test
    if test_installation():
        print("\n All installed successfully!")
        
        choice = input("\nGenerate a test image? (y/n): ").strip().lower()
        if choice == 'y':
            generate_test_image()
    else:
        print("\nInstallation may have failed. Check errors above.")
        print("Try running the installation commands manually.")

if __name__ == "__main__":
    main()
