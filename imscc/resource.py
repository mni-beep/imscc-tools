"""Resource classes for files and web resources in IMSCC packages."""

import os
import shutil
from pathlib import Path
from typing import Optional
from .utils import generate_identifier


class FileResource:
    """Represents a file/web resource to be included in the IMSCC package."""
    
    def __init__(
        self,
        filepath: str,
        destination_path: Optional[str] = None,
        identifier: Optional[str] = None
    ):
        """
        Create a file resource.
        
        Args:
            filepath: Path to the file on disk
            destination_path: Path within the IMSCC (e.g., 'web_resources/image.png')
                            If None, uses just the filename
            identifier: Unique identifier (auto-generated if not provided)
        """
        self.filepath = filepath
        self.identifier = identifier or generate_identifier()
        
        if destination_path:
            self.destination_path = destination_path
        else:
            # Use just the filename
            self.destination_path = f"web_resources/{os.path.basename(filepath)}"
    
    @property
    def filename(self) -> str:
        """Get the filename from the filepath."""
        return os.path.basename(self.filepath)
    
    def copy_to(self, target_dir: str) -> None:
        """
        Copy this file to the target directory.
        
        Args:
            target_dir: Base directory to copy to
        """
        target_path = os.path.join(target_dir, self.destination_path)
        
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # Copy the file
        shutil.copy2(self.filepath, target_path)


class FileManager:
    """Manages file resources for a course."""
    
    def __init__(self):
        self.files: list[FileResource] = []
    
    def add_file(
        self,
        filepath: str,
        destination_path: Optional[str] = None
    ) -> FileResource:
        """
        Add a file to be included in the package.
        
        Args:
            filepath: Path to the file
            destination_path: Optional path within the IMSCC
        
        Returns:
            The created FileResource
        """
        resource = FileResource(filepath, destination_path)
        self.files.append(resource)
        return resource
    
    def add_directory(
        self,
        directory: str,
        destination_prefix: str = "web_resources"
    ) -> list[FileResource]:
        """
        Add all files from a directory.
        
        Args:
            directory: Path to the directory
            destination_prefix: Prefix for destination paths
        
        Returns:
            List of created FileResources
        """
        added_files = []
        dir_path = Path(directory)
        
        for file_path in dir_path.rglob('*'):
            if file_path.is_file():
                # Calculate relative path
                rel_path = file_path.relative_to(dir_path)
                dest_path = f"{destination_prefix}/{rel_path}"
                
                resource = FileResource(str(file_path), dest_path)
                self.files.append(resource)
                added_files.append(resource)
        
        return added_files
    
    def copy_all(self, target_dir: str) -> None:
        """
        Copy all managed files to the target directory.
        
        Args:
            target_dir: Base directory to copy files to
        """
        for file_resource in self.files:
            file_resource.copy_to(target_dir)
