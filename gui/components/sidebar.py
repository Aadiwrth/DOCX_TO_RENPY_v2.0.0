"""
Sidebar component with file list and controls
"""

import sys
import customtkinter as ctk
import webbrowser
from pathlib import Path
from PIL import Image

try:
    from gui.utils.constants import *
    print("constants imported successfully")
except Exception as e:
    print("FAILED importing constants:", e)

try:
    from renpy_doc_convert.api import DOC_TO_RENPY_VERSION
    print("api imported successfully")
except Exception as e:
    print("FAILED importing api:", e)


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    
    When running as a PyInstaller bundle, files are extracted to a temp folder
    and the path is stored in sys._MEIPASS.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        # If not running as a bundle, use the script's directory
        base_path = Path(__file__).parent.parent.parent
    
    return base_path / relative_path


class Sidebar(ctk.CTkScrollableFrame):
    """Left sidebar with controls and file list - Now scrollable!"""
    
    def __init__(self, parent, callbacks):
        super().__init__(
            parent, 
            width=SIDEBAR_WIDTH, 
            corner_radius=0,
            fg_color=("gray90", "gray13")
        )
        
        self.callbacks = callbacks
        
        self._create_logo_section()
        self._create_separator()
        self._create_files_section()
        self._create_separator()
        self._create_actions_section()
        self._create_separator()
        self._create_support_section()
        self._create_separator()
        self._create_theme_section()

    def _create_logo_section(self):
        """Create logo and version display"""
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(padx=20, pady=(20, 5), fill="x")
        
        # Try to load logo
        try:
            # Use resource_path helper to get correct path in both dev and production
            logo_path = resource_path("assets/icon.png")
            
            if logo_path.exists():
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((150, 150), Image.Resampling.LANCZOS)
                logo_image = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(150, 150))
                
                logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="")
                logo_label.pack(pady=(0, 10))
            else:
                raise FileNotFoundError(f"Logo not found at {logo_path}")
        except Exception as e:
            # Fallback to emoji if logo can't be loaded
            print(f"Could not load logo: {e}")  # Helpful for debugging
            logo_label = ctk.CTkLabel(logo_frame, text="📄", font=ctk.CTkFont(size=60))
            logo_label.pack(pady=(0, 10))
        
        version_label = ctk.CTkLabel(
            logo_frame,
            text=f"v{DOC_TO_RENPY_VERSION}",
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray40")
        )
        version_label.pack(pady=(2, 0))
        
    def _create_separator(self):
        """Create a separator line"""
        separator = ctk.CTkFrame(self, height=2, fg_color=COLORS['border'])
        separator.pack(padx=20, pady=15, fill="x")
    
    def _create_files_section(self):
        """Create files list section"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(padx=20, pady=(5, 5), fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text="📁 Loaded Files",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        ).pack(side="left")
        
        self.files_count_label = ctk.CTkLabel(
            header_frame,
            text="(0)",
            font=ctk.CTkFont(size=13),
            text_color=("gray60", "gray40"),
            anchor="e"
        )
        self.files_count_label.pack(side="right")
        
        # Scrollable file list
        self.files_frame = ctk.CTkScrollableFrame(
            self,
            height=180,
            fg_color=COLORS['frame_bg'],
            border_width=1,
            border_color=COLORS['border']
        )
        self.files_frame.pack(padx=20, pady=(0, 15), fill="x")
    
    def _create_actions_section(self):
        """Create action buttons"""
        ctk.CTkLabel(
            self,
            text="⚡ Actions",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        ).pack(padx=20, pady=(5, 10), anchor="w")
        
        # Open files button
        self.open_button = ctk.CTkButton(
            self,
            text="📁  Open DOCX Files",
            command=self.callbacks['open_files'],
            height=BUTTON_HEIGHTS['primary'],
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover'],
            corner_radius=8
        )
        self.open_button.pack(padx=20, pady=(0, 8), fill="x")
        
        # Save current button
        self.save_button = ctk.CTkButton(
            self,
            text="💾  Save Current",
            command=self.callbacks['save_output'],
            height=BUTTON_HEIGHTS['secondary'],
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            fg_color=COLORS['success'],
            hover_color=COLORS['success_hover'],
            state="disabled"
        )
        self.save_button.pack(padx=20, pady=4, fill="x")
        
        # Save all button
        self.save_all_button = ctk.CTkButton(
            self,
            text="💾  Save All Outputs",
            command=self.callbacks['save_all'],
            height=BUTTON_HEIGHTS['secondary'],
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            fg_color=COLORS['success'],
            hover_color=COLORS['success_hover'],
            state="disabled"
        )
        self.save_all_button.pack(padx=20, pady=4, fill="x")
        
        # Clear button
        ctk.CTkButton(
            self,
            text="🗑️  Clear All",
            command=self.callbacks['clear_all'],
            height=BUTTON_HEIGHTS['secondary'],
            font=ctk.CTkFont(size=14),
            fg_color=COLORS['danger'],
            hover_color=COLORS['danger_hover'],
            corner_radius=8
        ).pack(padx=20, pady=4, fill="x")
    
    def _create_support_section(self):
        """Create support section"""
        ctk.CTkLabel(
            self,
            text="💝 Support",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        ).pack(padx=20, pady=(0, 10), anchor="w")
        
        support_frame = ctk.CTkFrame(self, fg_color="transparent")
        support_frame.pack(padx=20, pady=(0, 10), fill="x")
        
        # Ko-fi button
        try:
            # Use resource_path helper for Ko-fi image
            kofi_path = resource_path("assets/kofi.png")
            
            if kofi_path.exists():
                kofi_img = Image.open(kofi_path)
                kofi_img = kofi_img.resize((220, 55), Image.Resampling.LANCZOS)
                kofi_photo = ctk.CTkImage(light_image=kofi_img, dark_image=kofi_img, size=(220, 55))
                
                kofi_button = ctk.CTkButton(
                    support_frame,
                    image=kofi_photo,
                    text="",
                    command=lambda: webbrowser.open(URLS['kofi']),
                    height=55,
                    width=220,
                    fg_color="transparent",
                    hover_color=COLORS['kofi_hover'],
                    corner_radius=8
                )
                kofi_button.pack(pady=4)
            else:
                # raise FileNotFoundError(f"Ko-fi image not found at {kofi_path}")
                raise FileNotFoundError
        except Exception as e:
            print(f"Could not load Ko-fi image: {e}")  # Helpful for debugging
            kofi_button = ctk.CTkButton(
                support_frame,
                text="☕  Buy me a Coffee",
                command=lambda: webbrowser.open(URLS['kofi']),
                height=45,
                font=ctk.CTkFont(size=13),
                fg_color=COLORS['kofi'],
                hover_color=COLORS['kofi_hover'],
                corner_radius=8
            )
            kofi_button.pack(pady=4, fill="x")
        
        # GitHub button
        ctk.CTkButton(
            support_frame,
            text="⭐  Star on GitHub",
            command=lambda: webbrowser.open(URLS['github']),
            height=45,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS['github'],
            hover_color=COLORS['github_hover'],
            corner_radius=8
        ).pack(pady=4, fill="x")
    
    def _create_theme_section(self):
        """Create theme selector"""
        ctk.CTkLabel(
            self,
            text="🎨 Theme",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(padx=20, pady=(5, 5), anchor="w")
        
        self.theme_menu = ctk.CTkOptionMenu(
            self,
            values=THEME_OPTIONS,
            command=self.callbacks['change_theme'],
            height=BUTTON_HEIGHTS['small'],
            corner_radius=8,
            font=ctk.CTkFont(size=13)
        )
        self.theme_menu.pack(padx=20, pady=(0, 20), fill="x")
        self.theme_menu.set(DEFAULT_THEME)
    
    def update_file_count(self, count):
        """Update the file count display"""
        self.files_count_label.configure(text=f"({count})")
    
    def enable_save_buttons(self):
        """Enable save buttons"""
        self.save_button.configure(state="normal")
        self.save_all_button.configure(state="normal")
    
    def disable_save_buttons(self):
        """Disable save buttons"""
        self.save_button.configure(state="disabled")
        self.save_all_button.configure(state="disabled")