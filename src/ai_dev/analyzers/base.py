"""Base analyzer class for all file analyzers"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path


class AnalyzerBase(ABC):
    """Base class for all file analyzers"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
    @abstractmethod
    def analyze(self, file_path: str) -> Dict[str, Any]:
        """Analyze a file and extract structured information"""
        pass
    
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        """Extract plain text content from file"""
        pass
    
    def validate_file(self, file_path: str) -> bool:
        """Check if file exists and is valid"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if not path.is_file():
            raise ValueError(f"Not a file: {file_path}")
        return True
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get basic file information"""
        path = Path(file_path)
        return {
            "name": path.name,
            "size": path.stat().st_size,
            "extension": path.suffix,
            "path": str(path.absolute())
        }