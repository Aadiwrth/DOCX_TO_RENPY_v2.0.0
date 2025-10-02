"""
Session and document state management
"""

from pathlib import Path


class SessionManager:
    """Manages the current session state"""
    
    def __init__(self):
        self.current_files = []
        self.output_contents = {}
        self.selected_file_index = None
    
    def add_file(self, filepath, content):
        """Add a file to the session"""
        if filepath not in self.current_files:
            self.current_files.append(filepath)
            self.output_contents[filepath] = content
            return True
        return False
    
    def remove_file(self, filepath):
        """Remove a file from the session"""
        if filepath in self.current_files:
            self.current_files.remove(filepath)
            if filepath in self.output_contents:
                del self.output_contents[filepath]
            
            # Adjust selected index if needed
            if self.selected_file_index is not None:
                if self.selected_file_index >= len(self.current_files):
                    self.selected_file_index = len(self.current_files) - 1 if self.current_files else None
    
    def get_file(self, index):
        """Get file at index"""
        if 0 <= index < len(self.current_files):
            return self.current_files[index]
        return None
    
    def get_content(self, filepath):
        """Get content for a file"""
        return self.output_contents.get(filepath, "")
    
    def get_selected_file(self):
        """Get currently selected file"""
        if self.selected_file_index is not None:
            return self.get_file(self.selected_file_index)
        return None
    
    def get_selected_content(self):
        """Get content of selected file"""
        filepath = self.get_selected_file()
        if filepath:
            return self.get_content(filepath)
        return ""
    
    def clear_all(self):
        """Clear all session data"""
        self.current_files = []
        self.output_contents = {}
        self.selected_file_index = None
    
    def has_files(self):
        """Check if any files are loaded"""
        return len(self.current_files) > 0
    
    def file_count(self):
        """Get number of loaded files"""
        return len(self.current_files)
    
    def get_file_name(self, index):
        """Get filename at index"""
        filepath = self.get_file(index)
        if filepath:
            return Path(filepath).name
        return None
    def has_file(self, filepath):
        """Check if file is already loaded"""
        return filepath in self.current_files