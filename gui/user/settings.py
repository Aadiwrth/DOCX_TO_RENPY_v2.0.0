
"""
User settings management
"""

import json
import os
from pathlib import Path


class Settings:
    """Manages user settings and preferences"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".docx_to_renpy"
        self.config_file = self.config_dir / "settings.json"
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from config file"""
        default_settings = {
            'theme': 'Dark',
            'last_directory': str(Path.home()),
            'window_size': '1300x800',
            'recent_files': [],
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    default_settings.update(loaded)
            except Exception:
                pass
        
        return default_settings
    
    def save_settings(self):
        """Save settings to config file"""
        try:
            self.config_dir.mkdir(exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception:
            pass
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()
    
    def add_recent_file(self, filepath):
        """Add a file to recent files list"""
        recent = self.settings.get('recent_files', [])
        if filepath in recent:
            recent.remove(filepath)
        recent.insert(0, filepath)
        recent = recent[:10]  # Keep only last 10
        self.set('recent_files', recent)

