"""
Cross-platform path utilities for test data loading.
"""
import platform
from pathlib import Path


class PathFactory:
    """Factory for resolving cross-platform file paths based on OS."""

    @staticmethod
    def get_platform() -> str:
        """
        Get the current operating system.
        
        Returns:
            str: 'windows', 'linux', or 'darwin' (macOS)
        """
        system = platform.system().lower()
        if system == "windows":
            return "windows"
        elif system == "linux":
            return "linux"
        elif system == "darwin":
            return "darwin"
        return system

    @staticmethod
    def get_test_data_path(relative_path: str) -> Path:
        """
        Resolve a relative path from the project root to a test data file.
        Automatically uses the correct path format for the current OS.
        
        Args:
            relative_path: Relative path using forward slashes
                          (e.g., "WEB_UI/data/users.json")
        
        Returns:
            Path: Absolute path to the test data file, formatted for the current OS
        """
        current_os = PathFactory.get_platform()
        
        # Get the project root (where this conftest.py is located)
        project_root = Path(__file__).parent
        
        if current_os == "windows":
            # Use Windows path format with backslashes
            path_parts = relative_path.replace("/", "\\").split("\\")
            data_path = project_root
            for part in path_parts:
                data_path = data_path / part
            return data_path
        else:
            # Use POSIX path format with forward slashes (Linux, macOS)
            path_parts = relative_path.replace("\\", "/").split("/")
            data_path = project_root
            for part in path_parts:
                data_path = data_path / part
            return data_path

    @staticmethod
    def validate_path_exists(path: Path) -> bool:
        """
        Validate that a path exists.
        
        Args:
            path: Path to validate
            
        Returns:
            bool: True if path exists, False otherwise
        """
        return path.exists()
