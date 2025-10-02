
"""
Theme management for the application
"""

import customtkinter as ctk
from gui.utils.constants import DEFAULT_THEME, DEFAULT_COLOR_THEME


class ThemeManager:
    """Manages application theme and appearance"""
    
    def __init__(self, settings):
        self.settings = settings
        self.apply_saved_theme()
    
    def apply_saved_theme(self):
        """Apply theme from saved settings"""
        theme = self.settings.get('theme', DEFAULT_THEME)
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme(DEFAULT_COLOR_THEME)
    
    def change_theme(self, theme):
        """Change the application theme"""
        ctk.set_appearance_mode(theme)
        self.settings.set('theme', theme)
