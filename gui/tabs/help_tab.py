
"""
Help documentation tab
"""

import customtkinter as ctk
from gui.utils.constants import COLORS


class HelpTab:
    """Help documentation tab"""
    
    HELP_TEXT = """
🚀 QUICK START GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Click "📁 Open DOCX Files" to select Word documents
2. Files are automatically converted upon loading
3. Click on files in the sidebar to view their output
4. Review the converted Renpy script in the Output tab
5. Use "💾 Save Current" or "💾 Save All" to export


📝 DOCUMENT FORMAT GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Character Definitions (Optional):
  Characters{ E = Ellen (#678CD1), F = Felix (#C77850) }

Dialogue Format:
  E: Hello there!
  Felix: How are you doing today?

Narration:
  Simply write text without a character prefix or colon.
  This will be treated as narration in your Renpy script.

Comments:
  # This is a comment (hash style)
  (This is also a comment - parentheses style)

Scene Labels:
  == scene_name ==
  Use double equals to create labeled scenes for navigation

Menu System:
  E: What will you choose?
  - Go left == left_path
  - Go right == right_path
  - Stay here == stay_scene


✨ FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Auto-conversion on file open
• Multiple file batch processing
• Character definitions with hex colors
• Text styling (bold, italic, underline, colors)
• Interactive menu system with choices
• Label markers for scene navigation
• Comment preservation
• Character name color styling
• Preview before saving


💡 PRO TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Select multiple DOCX files for batch processing
• Define characters at the start for cleaner code
• Apply text colors in Word for styled dialogue
• Use labels (== name ==) to organize scenes
• Preview output before saving to verify formatting
• Test your scripts in Renpy to ensure compatibility
• Use comments to organize complex scripts


⚠️ COMMON ISSUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Ensure DOCX files are properly formatted
• Character names should be consistent
• Check for special characters that may need escaping
• Verify menu options have proper formatting
• Test output in Renpy before full conversion
"""
    
    def __init__(self, parent):
        help_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color=("gray95", "gray10")
        )
        help_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(
            help_frame,
            text=self.HELP_TEXT,
            font=ctk.CTkFont(family="Consolas", size=13),
            justify="left",
            anchor="nw"
        ).pack(fill="both", expand=True, padx=15, pady=15)
