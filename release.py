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
from pathlib import Path

# ===================== Configuration =====================
APP_NAME = "DocxToRenpy"
APP_VERSION = "2.0.0"
MAIN_SCRIPT = "main.py"
OUTPUT_DIR = Path("dist")
BUILD_DIR = Path("build")
ICON_PATH = Path("assets/icon.png")

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

    # macOS: onedir mode
    if system == "Darwin":
        cmd.append("--onedir")
    else:  # Windows & Linux
        cmd.append("--onefile")

    cmd.append(MAIN_SCRIPT)
    print(f"Running PyInstaller: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def create_zip(system):
    """Create zip package for distribution"""
    if system == "Linux":
        # Single executable
        dist_path = OUTPUT_DIR / APP_NAME
        exe_path = OUTPUT_DIR / APP_NAME
        if exe_path.exists():
            temp_dir = BUILD_DIR / f"{APP_NAME}_zip"
            temp_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(exe_path, temp_dir / APP_NAME)
            dist_path = temp_dir
    elif system == "Darwin":
        dist_path = OUTPUT_DIR / APP_NAME
    else:
        dist_path = OUTPUT_DIR

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{APP_NAME}_{APP_VERSION}_{timestamp}_{system.lower()}"
    shutil.make_archive(zip_name, 'zip', dist_path)
    print(f"Created zip: {zip_name}.zip")

# ===================== Linux AppImage =====================

def create_appimage():
    """Create AppImage for Linux"""
    appdir = Path(f"{APP_NAME}.AppDir")
    bin_dir = appdir / "usr/bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    exe_path = OUTPUT_DIR / APP_NAME
    if not exe_path.exists():
        raise FileNotFoundError(f"Linux executable not found: {exe_path}")

    shutil.copy(exe_path, bin_dir / APP_NAME)

    # Create AppRun launcher
    apprun_path = appdir / "AppRun"
    apprun_path.write_text(f"""#!/bin/bash
HERE="$(dirname "$(readlink -f "${{0}}")")"
exec "$HERE/usr/bin/{APP_NAME}" "$@"
""")
    os.chmod(apprun_path, 0o755)

    # Minimal .desktop file
    desktop_file = appdir / f"{APP_NAME}.desktop"
    desktop_file.write_text(f"""[Desktop Entry]
Name={APP_NAME}
Exec={APP_NAME}
Icon={APP_NAME}
Type=Application
Categories=Utility;
""")

    # Download appimagetool if missing
    appimagetool = Path("./appimagetool")
    if not appimagetool.exists():
        subprocess.run([
            "wget",
            "-O", str(appimagetool),
            "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
        ], check=True)
        os.chmod(appimagetool, 0o755)

    output_appimage = Path(f"{APP_NAME}_{APP_VERSION}_linux_x86_64.AppImage")
    subprocess.run([str(appimagetool), str(appdir), str(output_appimage)], check=True)
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
