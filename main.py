"""
Main entry point for the Docx to Renpy Converter application
"""

import sys
from pathlib import Path
from gui.modern_app import DocxToRenpyApp

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(__file__).parent

    return base_path / relative_path

def main():
    """Launch the application"""
    app = DocxToRenpyApp()
    app.run()

if __name__ == "__main__":
    main()