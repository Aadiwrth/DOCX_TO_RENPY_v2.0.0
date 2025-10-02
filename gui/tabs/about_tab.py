"""
About information tab
"""

import customtkinter as ctk
from renpy_doc_convert.api import DOC_TO_RENPY_VERSION


class AboutTab:
    """About information tab"""
    
    @staticmethod
    def get_about_text():
        return f"""
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║          DOCX TO RENPY CONVERTER                     ║
║                                                       ║
║          Version {DOC_TO_RENPY_VERSION}                               ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝


📌 ABOUT THIS TOOL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This converter helps visual novel developers streamline their
workflow by converting Word documents into Renpy script format.

Write your dialogue and narration in the familiar Word interface,
then convert it to Renpy with a single click!


🎯 KEY FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Batch file processing
✓ Character color definitions
✓ Text styling preservation
✓ Menu and choice system
✓ Scene label support
✓ Comment preservation
✓ Real-time preview
✓ Modern, user-friendly interface


👨‍💻 DEVELOPER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Created with ❤️ for the visual novel community

GitHub: https://github.com/Aadiwrth
Ko-fi: https://ko-fi.com/wokuu


📜 LICENSE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This tool is open source and free to use.
Consider supporting development if you find it useful!


🙏 ACKNOWLEDGMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thanks to:
• The Renpy community for feedback and support
• All contributors and testers
• Coffee enthusiasts everywhere ☕


💬 FEEDBACK & SUPPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Found a bug? Have a feature request?
Open an issue on GitHub or reach out through Ko-fi!

Star the project on GitHub to show your support! ⭐
"""
    
    def __init__(self, parent):
        about_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color=("gray95", "gray10")
        )
        about_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(
            about_frame,
            text=self.get_about_text(),
            font=ctk.CTkFont(family="Consolas", size=13),
            justify="left",
            anchor="nw"
        ).pack(fill="both", expand=True, padx=15, pady=15)
