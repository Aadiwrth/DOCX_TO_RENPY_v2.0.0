"""
Main entry point for the Docx to Renpy Converter application
"""

from gui.modern_app import DocxToRenpyApp

def main():
    """Launch the application"""
    app = DocxToRenpyApp()
    app.run()

if __name__ == "__main__":
    main()
