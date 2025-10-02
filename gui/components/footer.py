"""
Status bar footer component
"""

import customtkinter as ctk
from gui.utils.constants import COLORS, STATUS_COLORS


class Footer(ctk.CTkFrame):
    """Status bar footer"""
    
    def __init__(self, parent):
        super().__init__(
            parent,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=COLORS['border']
        )
        
        self.status_label = ctk.CTkLabel(
            self,
            text="✓ Ready - Select DOCX files to begin",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.status_label.pack(side="left", padx=20, pady=8)
        
        self.status_indicator = ctk.CTkLabel(
            self,
            text="●",
            font=ctk.CTkFont(size=16),
            text_color=STATUS_COLORS['ready'],
            anchor="e"
        )
        self.status_indicator.pack(side="right", padx=20, pady=8)
    
    def set_status(self, message, status_type='ready'):
        """Update status message and indicator"""
        self.status_label.configure(text=message)
        color = STATUS_COLORS.get(status_type, STATUS_COLORS['ready'])
        self.status_indicator.configure(text_color=color)
