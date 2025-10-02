# Docx to Renpy Converter 
 ![Python](https://img.shields.io/badge/platform-Cross--Platform-green) ![License](https://img.shields.io/badge/license-MIT-orange)

**Added** advance version and continuation of docx to renpy which is inspired by @pass-by-reference

## 📁 Complete Project Structure

```
DOCX_TO_RENPY_v2.0.0/
├── gui/
│   ├── __init__.py
│   ├── modern_app.py              # Main application class
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py             # Sidebar with file list and controls
│   │   ├── main_area.py           # Main content area with tabs
│   │   └── footer.py              # Status bar footer
│   ├── tabs/
│   │   ├── __init__.py
│   │   ├── output_tab.py          # Output display tab
│   │   ├── help_tab.py            # Help documentation tab
│   │   └── about_tab.py           # About information tab
│   ├── user/
│   │   ├── __init__.py
│   │   ├── settings.py            # User settings manager (saves preferences)
│   │   ├── theme.py               # Theme configuration manager
│   │   └── session.py             # Session/document state manager
│   └── utils/
│       ├── __init__.py
│       ├── file_handler.py        # File operations (convert, save)
│       └── constants.py           # UI constants and configs
├── renpy_doc_convert/
│   ├── __init__.py
│   ├── api.py
│   ├── consolidate.py
│   └── to_renpy.py
├── assets/
│   ├── icon.png
│   └── kofi.png
├── requirements.txt
├── main.py                         # Entry point
└── README.md
```

----
## 🔍 Quick File Reference

### When you need to...

| Task | Edit This File |
|------|---------------|
| Change colors, sizes, URLs | `gui/utils/constants.py` |
| Modify file operations | `gui/utils/file_handler.py` |
| Add new settings | `gui/user/settings.py` |
| Change theme behavior | `gui/user/theme.py` |
| Modify session state | `gui/user/session.py` |
| Update sidebar UI | `gui/components/sidebar.py` |
| Change main content area | `gui/components/main_area.py` |
| Modify status bar | `gui/components/footer.py` |
| Update output display | `gui/tabs/output_tab.py` |
| Change help content | `gui/tabs/help_tab.py` |
| Update about info | `gui/tabs/about_tab.py` |
| Coordinate components | `gui/modern_app.py` |
| Change app entry point | `main.py` |

---
### **For Developers**

#### Adding a New Tab:
1. Create new file in `gui/tabs/` (e.g., `settings_tab.py`)
2. Create tab class with parent parameter
3. Add to `gui/tabs/__init__.py`
4. Register in `MainArea` class

#### Adding a New Feature:
1. Add constants to `gui/utils/constants.py`
2. Add business logic to appropriate manager
3. Add UI component to relevant component file
4. Connect callback in `modern_app.py`

#### Modifying Settings:
- Edit `gui/user/settings.py` for new settings
- Settings are automatically saved to JSON

### **For Users**

#### Running the Application:
```bash
python main.py
```

## 🔧 Installation

### Requirements
```txt
python-docx==1.1.2
sv-ttk==2.6
pyinstaller==6.10.0
customtkinter>=5.2.0
python-docx>=0.8.11
Pillow>=9.0.0
```

### Setup Steps
```bash
# Clone repository
git clone https://github.com/Aadiwrth/DOCX_TO_RENPY_v2.0.0.git
cd DOCX_TO_RENPY_v2.0.0

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 📦 File Descriptions

### Core Application Files

| File | Purpose | Key Responsibilities |
|------|---------|---------------------|
| `main.py` | Entry point | Initialize and launch app |
| `gui/modern_app.py` | Main app class | Coordinate all components, handle events |

### Component Files

| File | Purpose | What It Contains |
|------|---------|-----------------|
| `gui/components/sidebar.py` | Sidebar UI | File list, buttons, support links, theme selector |
| `gui/components/main_area.py` | Main content | Tab management, header with actions |
| `gui/components/footer.py` | Status bar | Status messages and indicators |

### Tab Files

| File | Purpose | Content |
|------|---------|---------|
| `gui/tabs/output_tab.py` | Output display | Text widget for converted Renpy code |
| `gui/tabs/help_tab.py` | Help docs | Usage instructions, formatting guide |
| `gui/tabs/about_tab.py` | About info | Version, credits, links |

### User Management Files

| File | Purpose | Features |
|------|---------|----------|
| `gui/user/settings.py` | Settings manager | Save/load preferences, recent files |
| `gui/user/theme.py` | Theme manager | Apply and change themes |
| `gui/user/session.py` | Session state | Track loaded files, selection, content |

### Utility Files

| File | Purpose | Contains |
|------|---------|----------|
| `gui/utils/constants.py` | Constants | Colors, sizes, URLs, file types |
| `gui/utils/file_handler.py` | File operations | Convert DOCX, save files, batch operations |

## 🎨 Customization Guide

### Changing Colors
Edit `gui/utils/constants.py`:
```python
COLORS = {
    'primary': ("#YOUR_COLOR", "#YOUR_COLOR"),
    'success': ("#YOUR_COLOR", "#YOUR_COLOR"),
    # ... more colors
}
```

### Adding New Settings
1. Edit `gui/user/settings.py`:
```python
default_settings = {
    'theme': 'Dark',
    'your_new_setting': 'default_value',  # Add here
}
```

2. Use in your code:
```python
value = self.settings.get('your_new_setting')
self.settings.set('your_new_setting', new_value)
```

### Adding a New Component
1. Create file in `gui/components/your_component.py`:
```python
import customtkinter as ctk
from gui.utils.constants import COLORS

class YourComponent(ctk.CTkFrame):
    def __init__(self, parent, callbacks):
        super().__init__(parent)
        # Your component code
```

2. Import in `gui/components/__init__.py`:
```python
from .your_component import YourComponent
__all__ = [..., 'YourComponent']
```

3. Use in `modern_app.py`:
```python
from gui.components import YourComponent

self.your_component = YourComponent(self, callbacks)
```

## 🧪 Testing Strategy

### Component Testing
Each component can be tested independently:

```python
# test_sidebar.py
from gui.components import Sidebar

def test_sidebar_creation():
    callbacks = {
        'open_files': lambda: None,
        # ... mock callbacks
    }
    sidebar = Sidebar(None, callbacks)
    assert sidebar is not None
```

### Manager Testing
```python
# test_session.py
from gui.user import SessionManager

def test_add_file():
    session = SessionManager()
    session.add_file('/path/to/file.docx', 'content')
    assert session.has_file('/path/to/file.docx')
```


## 🤝 Contributing

### Structure Makes it Easy:

1. **Fork** the repository
2. **Choose** a component to improve
3. **Make changes** in that component only
4. **Test** your changes
5. **Submit** pull request with clear description

### Component Ownership:
- `components/sidebar.py` - UI/UX improvements
- `components/main_area.py` - Tab management
- `user/settings.py` - Settings features
- `user/session.py` - State management
- `utils/file_handler.py` - File operations
- `tabs/*.py` - Content improvements

## 📞 Support

### Issues:
- **Bug Reports**: Open issue with component name
- **Feature Requests**: Specify which component
- **Questions**: Check documentation first

### Resources:
- 📖 [Documentation](https://github.com/Aadiwrth/DOCX_TO_RENPY_v2.0.0/wiki)
- 🐛 [Issue Tracker](https://github.com/Aadiwrth/DOCX_TO_RENPY_v2.0.0/issues)
- ☕ [Buy me a Cofee](https://ko-fi.com/wokuu)
## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Aadiwrth

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---


## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=Aadiwrth/devlog-Multi-Platform-Publisher&type=Date)](https://star-history.com/#Aadiwrth/DOCX_TO_RENPY_v2.0.0&Date)

---

**Created with ❤️ for the visual novel community**
