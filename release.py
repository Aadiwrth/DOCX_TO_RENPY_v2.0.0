#!/usr/bin/env python3
"""
Build script for Docx to Renpy Converter
Creates distributable executables for Windows, macOS, and Linux
"""

import os
import sys
import shutil
import subprocess
import datetime
import platform

# ===================== Configuration =====================
APP_NAME = "DocxToRenpy"
APP_VERSION = "2.0.0"
MAIN_SCRIPT = "main.py"
OUTPUT_DIR = "dist"
BUILD_DIR = "build"
ICON_PATH = os.path.join("assets", "icon.png")

# PyInstaller base options
PYINSTALLER_COMMON = [
    "--windowed",
    "--clean",
    "--noconfirm",
    f"--icon={ICON_PATH}",
    "--log-level=INFO",
]

# ===================== Helper Functions =====================

def clear_directory(dir_path):
    if os.path.exists(dir_path):
        print(f"Cleaning {dir_path}...")
        shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)

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

def run_pyinstaller(platform_system):
    """Run PyInstaller based on platform"""
    cmd = ["pyinstaller", f"--name={APP_NAME}"] + PYINSTALLER_COMMON

    # macOS: onedir mode
    if platform_system == "Darwin":
        cmd.append("--onedir")
    else:  # Windows & Linux
        cmd.append("--onefile")

    cmd.append(MAIN_SCRIPT)
    print(f"Running PyInstaller: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def create_zip(platform_system):
    """Create zip package for distribution"""
    dist_dir = os.path.join(OUTPUT_DIR, APP_NAME)
    if not os.path.exists(dist_dir):
        # Fallback to the normal dist folder
        dist_dir = os.path.join(OUTPUT_DIR, APP_NAME) if platform_system != "Linux" else OUTPUT_DIR

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{APP_NAME}_{APP_VERSION}_{timestamp}_{platform_system.lower()}"
    shutil.make_archive(zip_name, 'zip', dist_dir)
    print(f"Created zip: {zip_name}.zip")

# ===================== Linux AppImage =====================

def create_appimage():
    """Create AppImage for Linux"""
    appdir = f"{APP_NAME}.AppDir"
    os.makedirs(f"{appdir}/usr/bin", exist_ok=True)

    # Copy PyInstaller onedir output to AppDir
    src_dir = os.path.join(OUTPUT_DIR, APP_NAME)
    exe_name = APP_NAME
    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Linux dist folder not found: {src_dir}")

    shutil.copy(os.path.join(src_dir, exe_name), f"{appdir}/usr/bin/{exe_name}")

    # Create AppRun launcher
    apprun_path = os.path.join(appdir, "AppRun")
    with open(apprun_path, "w") as f:
        f.write(f"""#!/bin/bash
HERE="$(dirname "$(readlink -f "${{0}}")")"
exec "$HERE/usr/bin/{exe_name}" "$@"
""")
    os.chmod(apprun_path, 0o755)

    # Create minimal .desktop file
    desktop_file = os.path.join(appdir, f"{APP_NAME}.desktop")
    with open(desktop_file, "w") as f:
        f.write(f"""[Desktop Entry]
Name={APP_NAME}
Exec={exe_name}
Icon={APP_NAME}
Type=Application
Categories=Utility;
""")

    # Download appimagetool
    appimagetool = "appimagetool"
    if not os.path.exists(appimagetool):
        subprocess.run([
            "wget",
            "-O", appimagetool,
            "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
        ], check=True)
        os.chmod(appimagetool, 0o755)

    # Build AppImage
    output_appimage = f"{APP_NAME}_{APP_VERSION}_linux_x86_64.AppImage"
    subprocess.run([f"./{appimagetool}", appdir, output_appimage], check=True)
    print(f"Created AppImage: {output_appimage}")
    return output_appimage

# ===================== Main =====================

def main():
    system = platform.system()
    print(f"=== Building {APP_NAME} v{APP_VERSION} for {system} ===")

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

    # Linux AppImage
    if system == "Linux":
        try:
            create_appimage()
        except Exception as e:
            print(f"AppImage creation failed: {e}")
            sys.exit(1)

    # Create zip for all platforms
    create_zip(system)

    print(f"=== Build complete for {system} ===")

if __name__ == "__main__":
    main()
