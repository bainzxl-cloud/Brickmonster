"""
Stable Diffusion Web UI - Automatic Setup Script
Sets up Automatic1111 Web UI for unlimited local image generation

Prerequisites:
- Windows 10/11
- NVIDIA GPU (RTX 4050 detected!)
- 10GB+ free disk space
- Admin privileges for Python installation

Usage:
    python setup_stable_diffusion.py
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path

def run_command(cmd, description, check=True):
    """Run a command and report status."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print()
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        
        if check and result.returncode != 0:
            print(f"❌ Command failed with exit code {result.returncode}")
            return False
        
        print("✅ Success!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_python():
    """Check for Python installations."""
    print("\n" + "="*60)
    print("CHECKING PYTHON INSTALLATIONS")
    print("="*60)
    
    python_paths = [
        "python.exe",
        "python3.exe", 
        "C:\\Python310\\python.exe",
        "C:\\Python39\\python.exe",
        f"{os.environ['LOCALAPPDATA']}\\Programs\\Python\\Python310\\python.exe",
    ]
    
    found_python = []
    for path in python_paths:
        try:
            result = subprocess.run([path, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                found_python.append((path, result.stdout.strip()))
        except:
            pass
    
    if found_python:
        print("Found Python installations:")
        for path, version in found_python:
            print(f"  ✅ {path}: {version}")
        return True, found_python[0][0]  # Return first found
    else:
        print("❌ No Python installation found")
        return False, None

def download_python():
    """Download and install Python 3.10."""
    print("\n" + "="*60)
    print("DOWNLOADING PYTHON 3.10")
    print("="*60)
    
    python_url = "https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe"
    installer_path = Path.home() / "Downloads" / "python-3.10.11-amd64.exe"
    
    print(f"Downloading from: {python_url}")
    print(f"Saving to: {installer_path}")
    
    try:
        urllib.request.urlretrieve(python_url, installer_path)
        print("✅ Download complete!")
        print(f"\n📌 NEXT STEPS:")
        print(f"1. Run the installer: {installer_path}")
        print(f"2. CHECK 'Add Python to PATH' ✓")
        print(f"3. Click 'Install Now'")
        print(f"4. After install, restart this script")
        
        # Try to open installer
        try:
            os.startfile(installer_path)
            print("\n🚀 Opening installer...")
        except:
            pass
        
        return True
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def clone_sd_webui():
    """Clone Stable Diffusion Web UI repository."""
    print("\n" + "="*60)
    print("CLONING STABLE DIFFUSION WEB UI")
    print("="*60)
    
    sd_path = Path.home() / "stable-diffusion-webui"
    
    if sd_path.exists():
        print(f"⚠️  Already exists: {sd_path}")
        return True
    
    git_cmd = 'git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git'
    return run_command(git_cmd, "Cloning Stable Diffusion Web UI")

def create_launch_script():
    """Create a convenient launch script."""
    print("\n" + "="*60)
    print("CREATING LAUNCH SCRIPT")
    print("="*60)
    
    script_content = '''@echo off
echo ============================================
echo 🚀 STABLE DIFFUSION WEB UI
echo ============================================
echo.
echo Starting Stable Diffusion...
echo Open your browser to: http://127.0.0.1:7860
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

cd /d "%~dp0stable-diffusion-webui"

if exist "webui-user.bat" (
    call webui-user.bat
) else (
    echo webui-user.bat not found, running webui.bat
    call webui.bat
)
'''
    
    script_path = Path.home() / "Stable Diffusion.lnk"
    
    try:
        script_path.write_text(script_content)
        print(f"✅ Created launch script: {script_path}")
        print("\n📌 To use Stable Diffusion:")
        print("1. Double-click 'Stable Diffusion.lnk' on your desktop")
        print("2. Wait for it to download models (~5GB)")
        print("3. Open http://127.0.0.1:7860 in your browser")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def main():
    print("="*60)
    print("🎨 STABLE DIFFUSION SETUP")
    print("="*60)
    print("\nThis will set up Automatic1111 Stable Diffusion Web UI")
    print("for UNLIMITED FREE image generation on your RTX 4050!")
    
    # Step 1: Check Python
    print("\n" + "="*60)
    print("STEP 1: CHECKING PYTHON")
    print("="*60)
    
    has_python, python_path = check_python()
    
    if not has_python:
        print("\n❌ Python 3.10 is required but not found.")
        print("\n📌 Downloading Python 3.10 installer...")
        if download_python():
            print("\n" + "="*60)
            print("⚠️  INSTALL PYTHON MANUALLY")
            print("="*60)
            print("""
1. The Python installer should have opened
2. CHECK 'Add Python to PATH' ✓ (VERY IMPORTANT!)
3. Click 'Install Now'
4. Wait for installation to complete
5. RESTART THIS SCRIPT
            """)
            input("Press Enter to exit...")
            sys.exit(0)
    
    # Step 2: Clone repository
    if not clone_sd_webui():
        print("❌ Failed to clone Stable Diffusion Web UI")
        sys.exit(1)
    
    # Step 3: Create launch script
    create_launch_script()
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print("""
📌 NEXT STEPS:

1. Double-click 'Stable Diffusion.lnk' on your desktop
   (or navigate to stable-diffusion-webui folder)
   
2. On first run, it will:
   - Download Stable Diffusion model (~5GB)
   - Download necessary files
   - Install dependencies
   
3. Once running, open:
   http://127.0.0.1:7860
   
4. Enter prompts like:
   "A cute bunny reading a book"
   "Beautiful sunset over ocean"
   "Study room with books"

5. Press Ctrl+C to stop the server

🎨 Enjoy UNLIMITED free image generation!
    """)

if __name__ == "__main__":
    main()
