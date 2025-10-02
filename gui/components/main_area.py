
"""
Main content area with tabbed interface
"""

import customtkinter as ctk
from gui.utils.constants import COLORS, BUTTON_HEIGHTS
from gui.tabs import OutputTab, HelpTab, AboutTab


class MainArea(ctk.CTkFrame):
    """Main content area with tabs"""
    
    def __init__(self, parent, callbacks):
        super().__init__(
            parent,
            corner_radius=10,
            border_width=1,
            border_color=COLORS['border']
        )
        
        self.callbacks = callbacks
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._create_header()
        self._create_tabview()
    
    def _create_header(self):
        """Create header section"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(25, 15))
        
        ctk.CTkLabel(
            header_frame,
            text="📝 Output Preview",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left")
        
        # Button frame
        button_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        button_frame.pack(side="right")
        
        self.copy_button = ctk.CTkButton(
            button_frame,
            text="📋  Copy",
            command=self.callbacks['copy_to_clipboard'],
            width=110,
            height=BUTTON_HEIGHTS['header'],
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.copy_button.pack(side="right", padx=5)
    
    def _create_tabview(self):
        """Create tabbed interface"""
        self.tabview = ctk.CTkTabview(
            self,
            corner_radius=10,
            border_width=1,
            border_color=COLORS['border']
        )
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 25))
        
        # Add tabs
        self.tabview.add("📄 Output")
        self.tabview.add("📖 Help")
        self.tabview.add("⁉️ About")
        
        # Create tab content
        self.output_tab = OutputTab(self.tabview.tab("📄 Output"))
        self.help_tab = HelpTab(self.tabview.tab("📖 Help"))
        self.about_tab = AboutTab(self.tabview.tab("⁉️ About"))
    
    def get_output_text_widget(self):
        """Get the output text widget"""
        return self.output_tab.text_widget
    
    def switch_to_output_tab(self):
        """Switch to the output tab"""
        self.tabview.set("📄 Output")
    
    def update_copy_button(self, text):
        """Update copy button text"""
        self.copy_button.configure(text=text)
