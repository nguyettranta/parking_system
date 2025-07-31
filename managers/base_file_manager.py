import os

class BaseFileManager:
    """Base class for file operations"""
    
    base_directory = os.path.join(os.getcwd(), "data")
    
    def __init__(self):
        # Create the directory if it doesn't exist
        os.makedirs(self.base_directory, exist_ok=True)
    
    def get_file_path(self, filename):
        """Get the full path for a file"""
        return os.path.join(self.base_directory, filename)