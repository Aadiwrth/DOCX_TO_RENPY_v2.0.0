
"""
Constants and configuration values for the GUI
"""

# Window Configuration
WINDOW_TITLE_PREFIX = "Docx to Renpy Converter"
DEFAULT_WINDOW_SIZE = "1300x800"
MIN_WINDOW_SIZE = (1100, 700)

# Sidebar Configuration
SIDEBAR_WIDTH = 320

# Theme Configuration
THEME_OPTIONS = ["Dark", "Light", "System"]
DEFAULT_THEME = "Dark"
DEFAULT_COLOR_THEME = "blue"

# Colors
COLORS = {
    'primary': ("#1f6aa5", "#1f6aa5"),
    'primary_hover': ("#144870", "#144870"),
    'success': ("#2c7a3d", "#2c7a3d"),
    'success_hover': ("#1e5529", "#1e5529"),
    'danger': ("#c1121f", "#c1121f"),
    'danger_hover': ("#8b0000", "#8b0000"),
    'kofi': ("#29ABE0", "#29ABE0"),
    'kofi_hover': ("#1E8CB8", "#1E8CB8"),
    'github': ("#24292e", "#24292e"),
    'github_hover': ("#454d55", "#454d55"),
    'border': ("gray70", "gray30"),
    'frame_bg': ("gray90", "gray15"),
}

# Status Colors
STATUS_COLORS = {
    'ready': ("#2c7a3d", "#2c7a3d"),
    'processing': ("#f59e0b", "#f59e0b"),
    'error': ("#c1121f", "#c1121f"),
    'viewing': ("#1f6aa5", "#1f6aa5"),
}

# Button Sizes
BUTTON_HEIGHTS = {
    'primary': 48,
    'secondary': 42,
    'header': 38,
    'small': 35,
}

# File Types
SUPPORTED_FILE_TYPES = [("Word Documents", "*.docx"), ("All Files", "*.*")]
RENPY_FILE_TYPES = [("Renpy Script", "*.rpy"), ("All Files", "*.*")]

# URLs
URLS = {
    'kofi': "https://ko-fi.com/wokuu",
    'github': "https://github.com/Aadiwrth/doc-to-renpy",
}

# Fonts
FONTS = {
    'title': ('', 28, 'bold'),
    'heading': ('', 24, 'bold'),
    'subheading': ('', 15, 'bold'),
    'normal': ('', 13),
    'code': ('Consolas', 13),
    'small': ('', 12),
}