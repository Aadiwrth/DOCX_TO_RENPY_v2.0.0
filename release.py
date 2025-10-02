#!/usr/bin/env python3
"""
Build script for Docx to Renpy Converter
Supports Windows, macOS, and Linux
"""

import os
import sys
import shutil
import subprocess
import datetime
import platform
from pathlib import Path

# ===================== Configuration =====================
APP_NAME = "DocxToRenpy"
APP_VERSION = "2.0.0"
MAIN_SCRIPT = "main.py"
OUTPUT_DIR = Path("dist")
BUILD_DIR = Path("build")
ICON_PATH = Path("assets/icon.ico")

# Platform-specific icon paths
ICON_WINDOWS = Path("assets/icon.ico")
ICON_MACOS = Path("assets/icon.icns")  # macOS needs .icns format
ICON_LINUX = Path("assets/icon.png")   # Linux uses .png

# PyInstaller base options (icon will be added per platform)
PYINSTALLER_COMMON = [
    "--clean",
    "--noconfirm",
    "--log-level=INFO",
]

# ===================== Helper Functions =====================

def clear_directory(dir_path):
    if dir_path.exists():
        print(f"Cleaning {dir_path}...")
        shutil.rmtree(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)

def clean_pycache():
    for root, dirs, _ in os.walk(".", topdown=False):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))

def check_prerequisites():
    try:
        proc = subprocess.run(
            ["pyinstaller", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if proc.returncode != 0:
            print("PyInstaller not found. Install via: pip install pyinstaller")
            return False
        print(f"PyInstaller version: {proc.stdout.strip()}")
        return True
    except Exception as e:
        print(f"Error checking prerequisites: {str(e)}")
        return False

# ===================== Build Functions =====================

def run_pyinstaller(system):
    """Run PyInstaller based on platform"""
    cmd = ["pyinstaller", f"--name={APP_NAME}"] + PYINSTALLER_COMMON
    
    # Add platform-specific icon
    if system == "Windows":
        if ICON_WINDOWS.exists():
            cmd.append(f"--icon={ICON_WINDOWS}")
    elif system == "Darwin":
        if ICON_MACOS.exists():
            cmd.append(f"--icon={ICON_MACOS}")
        else:
            print(f"Warning: {ICON_MACOS} not found, using default icon")
    elif system == "Linux":
        if ICON_LINUX.exists():
            cmd.append(f"--icon={ICON_LINUX}")
    
    # Add data files (assets folder)
    # IMPORTANT: Make sure assets folder exists
    assets_dir = Path("assets")
    if not assets_dir.exists():
        print(f"WARNING: Assets directory not found at {assets_dir.absolute()}")
    else:
        print(f"Assets directory found: {assets_dir.absolute()}")
        # List files in assets
        print("Assets contents:")
        for item in assets_dir.iterdir():
            print(f"  - {item.name}")
    
    if system == "Windows":
        cmd.append("--add-data=assets;assets")
    else:  # macOS and Linux
        cmd.append("--add-data=assets:assets")

    # Platform-specific build options
    if system == "Darwin":
        cmd.append("--onedir")
        cmd.append("--windowed")
    elif system == "Windows":
        cmd.append("--onefile")
        cmd.append("--windowed")
    elif system == "Linux":
        # CHANGED: Use --onedir for Linux to properly handle assets
        cmd.append("--onedir")
        # Note: No --windowed on Linux as it may cause issues
    else:
        raise RuntimeError(f"Unsupported platform: {system}")

    cmd.append(MAIN_SCRIPT)
    print(f"Running PyInstaller: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def create_zip(system):
    """Create zip package for distribution"""
    if system == "Windows":
        dist_path = OUTPUT_DIR / f"{APP_NAME}.exe"
        temp_dir = BUILD_DIR / f"{APP_NAME}_zip"
        temp_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(dist_path, temp_dir / f"{APP_NAME}.exe")
        dist_path = temp_dir
    elif system == "Darwin":
        dist_path = OUTPUT_DIR / f"{APP_NAME}.app"
    elif system == "Linux":
        # Linux now uses --onedir, so we need to zip the folder
        dist_path = OUTPUT_DIR / APP_NAME
    else:
        raise RuntimeError(f"Unsupported platform: {system}")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{APP_NAME}_{APP_VERSION}_{timestamp}_{system.lower()}"
    shutil.make_archive(zip_name, 'zip', dist_path)
    print(f"Created zip: {zip_name}.zip")

# ===================== Main =====================

def main():
    system = platform.system()
    print(f"=== Building {APP_NAME} v{APP_VERSION} for {system} ===")

    if system not in ["Darwin", "Windows", "Linux"]:
        print(f"Unsupported platform: {system}")
        sys.exit(1)

    if not check_prerequisites():
        sys.exit(1)

    clean_pycache()
    clear_directory(BUILD_DIR)
    clear_directory(OUTPUT_DIR)

    try:
        run_pyinstaller(system)
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller failed: {e}")
        sys.exit(1)

    try:
        create_zip(system)
    except Exception as e:
        print(f"Zip creation failed: {e}")
        sys.exit(1)

    print(f"=== Build complete for {system} ===")
    
    # Platform-specific instructions
    if system == "Linux":
        print("\nLinux build notes:")
        print(f"  - Extract the zip file and run ./{APP_NAME}/{APP_NAME}")
        print("  - The executable may need chmod +x to run")
        print(f"  - All assets are bundled in the {APP_NAME} folder")

if __name__ == "__main__":
    main()