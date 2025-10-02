#!/usr/bin/env python3
"""
Build script for DOCX to Renpy Converter
Creates distributable executables for Windows, macOS, and Linux (AppImage)
"""

import os
import sys
import shutil
import subprocess
import datetime
import platform

# ==== Configuration ====
APP_NAME = "DocxToRenpy"
APP_VERSION = "2.0.0"
MAIN_SCRIPT = "main.py"
OUTPUT_DIR = "dist"
BUILD_DIR = "build"
ICON_PATH = os.path.join("assets", "icon.png")
REQ_FILE = "requirements.txt"

# PyInstaller options
BASE_OPTS = [
    "--onefile",
    "--windowed",
    f"--icon={ICON_PATH}",
    "--clean",
    "--noconfirm",
    "--log-level=INFO"
]

def clear_directory(dir_path):
    if os.path.exists(dir_path):
        print(f"Cleaning {dir_path}...")
        shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)

def clean_pycache():
    for root, dirs, files in os.walk(".", topdown=False):
        for d in dirs:
            if d == "__pycache__":
                cache_dir = os.path.join(root, d)
                print(f"Removing {cache_dir}")
                shutil.rmtree(cache_dir)

def generate_requirements():
    """Freeze dependencies into requirements.txt"""
    print("Generating requirements.txt...")
    try:
        with open(REQ_FILE, "w") as f:
            subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=f, check=True)
        print("requirements.txt generated.")
        return True
    except Exception as e:
        print(f"Failed to generate requirements.txt: {e}")
        return False

def run_pyinstaller():
    """Run PyInstaller for current OS"""
    opts = BASE_OPTS.copy()
    opts.append(f"--name={APP_NAME}")
    cmd = ["pyinstaller"] + opts + [MAIN_SCRIPT]

    print("Running PyInstaller...")
    print(f"Command: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller failed: {e}")
        return False

def create_appimage():
    """Package Linux build into AppImage"""
    if platform.system().lower() != "linux":
        return None

    print("Creating AppImage...")

    appdir = f"{APP_NAME}.AppDir"
    if os.path.exists(appdir):
        shutil.rmtree(appdir)
    os.makedirs(os.path.join(appdir, "usr", "bin"), exist_ok=True)
    os.makedirs(os.path.join(appdir, "usr", "share", "applications"), exist_ok=True)
    os.makedirs(os.path.join(appdir, "usr", "share", "icons", "hicolor", "256x256", "apps"), exist_ok=True)

    # Move binary
    binary_path = os.path.join("dist", APP_NAME)
    shutil.copy(binary_path, os.path.join(appdir, "usr", "bin", APP_NAME))

    # Desktop entry
    desktop_file = f"""
    [Desktop Entry]
    Name={APP_NAME}
    Exec={APP_NAME}
    Icon={APP_NAME}
    Type=Application
    Categories=Utility;
    """
    desktop_path = os.path.join(appdir, "usr", "share", "applications", f"{APP_NAME}.desktop")
    with open(desktop_path, "w") as f:
        f.write(desktop_file.strip())

    # Icon
    shutil.copy(ICON_PATH, os.path.join(appdir, "usr", "share", "icons", "hicolor", "256x256", "apps", f"{APP_NAME}.png"))

    # AppRun script
    apprun_path = os.path.join(appdir, "AppRun")
    with open(apprun_path, "w") as f:
        f.write(f"#!/bin/sh\nexec $APPDIR/usr/bin/{APP_NAME} \"$@\"")
    os.chmod(apprun_path, 0o755)

    # Download appimagetool if not installed
    if not shutil.which("appimagetool"):
        print("Downloading appimagetool...")
        subprocess.run([
            "wget", "-q",
            "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage",
            "-O", "appimagetool"
        ], check=True)
        os.chmod("appimagetool", 0o755)
        tool = "./appimagetool"
    else:
        tool = "appimagetool"

    # Build AppImage
    output_appimage = f"{APP_NAME}_{APP_VERSION}_linux_x86_64.AppImage"
    subprocess.run([tool, appdir, output_appimage], check=True)
    print(f"AppImage created: {output_appimage}")
    return output_appimage

def create_distribution_package(appimage_path=None):
    """Zip release package with binary + requirements.txt"""
    system = platform.system().lower()
    dist_dir = os.path.join(OUTPUT_DIR, APP_NAME)
    if not os.path.exists(dist_dir):
        dist_dir = OUTPUT_DIR

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{APP_NAME}_{APP_VERSION}_{timestamp}"

    if system == "windows":
        zip_name += "_win"
    elif system == "linux":
        zip_name += "_linux"
    elif system == "darwin":
        zip_name += "_mac"

    # Copy requirements.txt into dist
    if os.path.exists(REQ_FILE):
        shutil.copy(REQ_FILE, dist_dir)

    # Include AppImage if present
    if appimage_path:
        shutil.copy(appimage_path, dist_dir)

    shutil.make_archive(zip_name, 'zip', dist_dir)
    print(f"Created package: {zip_name}.zip")
    return True

def check_prerequisites():
    try:
        proc = subprocess.run(["pyinstaller", "--version"], stdout=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            print("Install PyInstaller: pip install pyinstaller")
            return False
        print(f"PyInstaller version: {proc.stdout.strip()}")
        return True
    except Exception as e:
        print(f"Error checking prerequisites: {e}")
        return False

def main():
    print(f"=== Building {APP_NAME} v{APP_VERSION} ===")
    if not check_prerequisites():
        sys.exit(1)

    clean_pycache()
    clear_directory(BUILD_DIR)
    clear_directory(OUTPUT_DIR)

    generate_requirements()

    if not run_pyinstaller():
        sys.exit(1)

    appimage_path = None
    if platform.system().lower() == "linux":
        appimage_path = create_appimage()

    create_distribution_package(appimage_path)
    print("=== Build completed successfully ===")

if __name__ == "__main__":
    main()
