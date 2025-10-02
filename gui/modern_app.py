"""
Main application class for Docx to Renpy Converter
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import sys

from gui.components import Sidebar, MainArea, Footer
from gui.user import Settings, ThemeManager, SessionManager
from gui.utils import FileHandler
from gui.utils.constants import *
from renpy_doc_convert.api import DOC_TO_RENPY_VERSION


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(__file__).parent.parent
    return base_path / relative_path


class DocxToRenpyApp(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize managers
        self.settings = Settings()
        self.theme_manager = ThemeManager(self.settings)
        self.session = SessionManager()
        self.file_handler = FileHandler()
        
        # Window configuration
        self.title(f"{WINDOW_TITLE_PREFIX} v{DOC_TO_RENPY_VERSION}")
        self.geometry(DEFAULT_WINDOW_SIZE)
        self.minsize(*MIN_WINDOW_SIZE)
        
        # Set window icon
        try:
            icon_path = resource_path("assets/icon.ico")
            if icon_path.exists():
                self.iconbitmap(str(icon_path))
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create UI components
        self._create_ui()
    
    def _create_ui(self):
        """Create all UI components"""
        # Define callbacks
        callbacks = {
            'open_files': self.open_files,
            'save_output': self.save_output,
            'save_all': self.save_all_outputs,
            'clear_all': self.clear_all,
            'change_theme': self.change_theme,
            'copy_to_clipboard': self.copy_to_clipboard,
            'select_file': self.select_file,
        }
        
        # Create components
        self.sidebar = Sidebar(self, callbacks)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        self.main_area = MainArea(self, callbacks)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=(5, 15), pady=15)
        
        self.footer = Footer(self)
        self.footer.grid(row=1, column=1, sticky="ew", padx=(5, 15), pady=(0, 15))
        
        # Apply saved theme
        saved_theme = self.settings.get('theme', DEFAULT_THEME)
        self.sidebar.theme_menu.set(saved_theme)
    
    def open_files(self):
        """Open file dialog and load multiple DOCX files"""
        filenames = filedialog.askopenfilenames(
            title="Select DOCX Files",
            filetypes=SUPPORTED_FILE_TYPES,
            initialdir=self.settings.get('last_directory', str(Path.home()))
        )
        
        if not filenames:
            return
        
        # Save last directory
        self.settings.set('last_directory', str(Path(filenames[0]).parent))
        
        self.footer.set_status("⏳ Converting files...", 'processing')
        self.update()
        
        new_files = [f for f in filenames if not self.session.has_file(f)]
        
        # Auto-convert all new files
        success_count = 0
        for filename in new_files:
            success, content, error = self.file_handler.convert_docx_to_renpy(filename)
            if success:
                self.session.add_file(filename, content)
                self.settings.add_recent_file(filename)
                success_count += 1
            else:
                messagebox.showerror("Conversion Error", error)
        
        # Update UI
        self._update_file_list()
        
        if success_count > 0:
            self.sidebar.enable_save_buttons()
            self.footer.set_status(f"✓ Converted {success_count} file(s) successfully", 'ready')
            
            # Select the first new file
            if new_files:
                first_new_index = self.session.current_files.index(new_files[0])
                self.select_file(first_new_index)
        else:
            self.footer.set_status("✗ No files were converted", 'error')
    
    def _update_file_list(self):
        """Update the file list display"""
        # Clear existing buttons
        for widget in self.sidebar.files_frame.winfo_children():
            widget.destroy()
        
        # Update count
        self.sidebar.update_file_count(self.session.file_count())
        
        # Create buttons for each file
        for i in range(self.session.file_count()):
            filename = self.session.get_file_name(i)
            self._create_file_button(filename, i)
    
    def _create_file_button(self, filename, index):
        """Create a clickable button for each file"""
        is_selected = (index == self.session.selected_file_index)
        
        btn = ctk.CTkButton(
            self.sidebar.files_frame,
            text=f"📄  {filename}",
            command=lambda: self.select_file(index),
            anchor="w",
            height=40,
            font=ctk.CTkFont(size=12),
            corner_radius=6,
            fg_color=COLORS['primary'] if is_selected else ("gray80", "gray20"),
            hover_color=COLORS['primary_hover']
        )
        btn.pack(fill="x", pady=3, padx=5)
    
    def select_file(self, index):
        """Select a file and display its output"""
        if 0 <= index < self.session.file_count():
            self.session.selected_file_index = index
            filepath = self.session.get_file(index)
            
            # Update file list to show selection
            self._update_file_list()
            
            # Display content
            content = self.session.get_content(filepath)
            output_widget = self.main_area.get_output_text_widget()
            output_widget.delete("1.0", "end")
            output_widget.insert("1.0", content)
            
            self.footer.set_status(f"📄 Viewing: {Path(filepath).name}", 'viewing')
            self.main_area.switch_to_output_tab()
    
    def save_output(self):
        """Save current output to .rpy file"""
        if self.session.selected_file_index is None:
            messagebox.showwarning("Warning", "No file selected")
            return
        
        filepath = self.session.get_selected_file()
        content = self.session.get_selected_content()
        
        if not content:
            messagebox.showwarning("Warning", "No content to save")
            return
        
        save_filename = filedialog.asksaveasfilename(
            title="Save Renpy Script",
            defaultextension=".rpy",
            initialfile=Path(filepath).stem + ".rpy",
            filetypes=RENPY_FILE_TYPES,
            initialdir=self.settings.get('last_directory', str(Path.home()))
        )
        
        if save_filename:
            success, error = self.file_handler.save_file(content, save_filename)
            if success:
                self.settings.set('last_directory', str(Path(save_filename).parent))
                self.footer.set_status(f"✓ Saved: {Path(save_filename).name}", 'ready')
                messagebox.showinfo("Success", "File saved successfully!")
            else:
                messagebox.showerror("Save Error", f"Error: {error}")
    
    def save_all_outputs(self):
        """Save all outputs to a directory"""
        if not self.session.has_files():
            messagebox.showwarning("Warning", "No files to save")
            return
        
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.settings.get('last_directory', str(Path.home()))
        )
        
        if directory:
            saved_count, error = self.file_handler.save_multiple_files(
                self.session.output_contents,
                directory
            )
            
            if error:
                messagebox.showerror("Save Error", f"Error: {error}")
            else:
                self.settings.set('last_directory', directory)
                self.footer.set_status(
                    f"✓ Saved {saved_count} file(s) to {Path(directory).name}",
                    'ready'
                )
                messagebox.showinfo("Success", f"Saved {saved_count} file(s) successfully!")
    
    def clear_all(self):
        """Clear all loaded files"""
        if not self.session.has_files():
            return
        
        if messagebox.askyesno("Clear All", "Clear all loaded files and outputs?"):
            self.session.clear_all()
            self._update_file_list()
            self.main_area.get_output_text_widget().delete("1.0", "end")
            self.sidebar.disable_save_buttons()
            self.footer.set_status("✓ Ready - Select DOCX files to begin", 'ready')
    
    def copy_to_clipboard(self):
        """Copy current output to clipboard"""
        content = self.session.get_selected_content()
        
        if content:
            self.clipboard_clear()
            self.clipboard_append(content)
            self.footer.set_status("✓ Copied to clipboard", 'ready')
            
            # Show temporary feedback
            self.main_area.update_copy_button("✓ Copied!")
            self.after(2000, lambda: self.main_area.update_copy_button("📋  Copy"))
        else:
            messagebox.showwarning("Warning", "No content to copy")
    
    def change_theme(self, new_theme):
        """Change UI appearance mode"""
        self.theme_manager.change_theme(new_theme)
    
    def run(self):
        """Start the application"""
        self.mainloop()