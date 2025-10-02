
"""
Output display tab
"""

import customtkinter as ctk
from gui.utils.constants import COLORS


class OutputTab:
    """Output text display tab"""
    
    def __init__(self, parent):
        self.text_widget = ctk.CTkTextbox(
            parent,
            font=ctk.CTkFont(family="Consolas", size=13),
            wrap="none",
            border_width=1,
            border_color=COLORS['border']
        )
        self.text_widget.pack(fill="both", expand=True, padx=15, pady=15)
    
    def set_content(self, content):
        """Set the text content"""
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", content)
    
    def get_content(self):
        """Get the text content"""
        return self.text_widget.get("1.0", "end-1c")
    
    def clear(self):
        """Clear the text content"""
        self.text_widget.delete("1.0", "end")

