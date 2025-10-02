
"""
File handling operations for the application
"""

import os
from pathlib import Path
from tkinter import messagebox
from renpy_doc_convert.api import convert


class FileHandler:
    """Handles file operations for document conversion"""
    
    @staticmethod
    def convert_docx_to_renpy(docx_file_path):
        """
        Convert a single DOCX file to Renpy format
        
        Args:
            docx_file_path: Path to the DOCX file
            
        Returns:
            tuple: (success: bool, content: str or None, error: str or None)
        """
        try:
            # Create temporary output file
            temp_output = os.path.join(
                os.path.dirname(docx_file_path),
                f"temp_renpy_{Path(docx_file_path).stem}"
            )
            
            # Convert
            convert(docx_file_path, temp_output)
            
            # Read output
            with open(temp_output, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Clean up temp file
            if os.path.exists(temp_output):
                os.remove(temp_output)
            
            return True, content, None
            
        except Exception as e:
            error_msg = f"Error converting {Path(docx_file_path).name}:\n{str(e)}"
            return False, None, error_msg
    
    @staticmethod
    def save_file(content, filepath):
        """
        Save content to a file
        
        Args:
            content: String content to save
            filepath: Destination file path
            
        Returns:
            tuple: (success: bool, error: str or None)
        """
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return True, None
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def save_multiple_files(output_contents, directory):
        """
        Save multiple files to a directory
        
        Args:
            output_contents: Dict mapping filepaths to content
            directory: Target directory
            
        Returns:
            tuple: (saved_count: int, error: str or None)
        """
        try:
            saved_count = 0
            for filepath, content in output_contents.items():
                if content:
                    output_filename = os.path.join(
                        directory,
                        Path(filepath).stem + ".rpy"
                    )
                    with open(output_filename, "w", encoding="utf-8") as f:
                        f.write(content)
                    saved_count += 1
            return saved_count, None
        except Exception as e:
            return 0, str(e)

