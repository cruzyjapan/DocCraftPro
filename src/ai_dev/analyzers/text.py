"""Text file analyzer"""

from typing import Dict, Any
from .base import AnalyzerBase
from ..utils.encoder import EncodingHandler
import re


class TextAnalyzer(AnalyzerBase):
    """Analyzer for text files (.txt, .md, etc.)"""
    
    def analyze(self, file_path: str) -> Dict[str, Any]:
        """Analyze text file and extract information"""
        self.validate_file(file_path)
        
        # Read file with auto encoding detection
        encoder = EncodingHandler()
        text, encoding = encoder.read_file_auto(file_path)
        
        # Basic analysis
        lines = text.split('\n')
        words = text.split()
        
        # Extract sections if markdown
        sections = []
        if file_path.endswith('.md'):
            sections = self._extract_markdown_sections(text)
        
        # Extract lists
        lists = self._extract_lists(text)
        
        return {
            "file_info": self.get_file_info(file_path),
            "encoding": encoding,
            "content": text,
            "statistics": {
                "characters": len(text),
                "lines": len(lines),
                "words": len(words),
                "paragraphs": len([p for p in text.split('\n\n') if p.strip()])
            },
            "sections": sections,
            "lists": lists,
            "summary": self._generate_summary(text)
        }
    
    def extract_text(self, file_path: str) -> str:
        """Extract plain text from file"""
        encoder = EncodingHandler()
        text, _ = encoder.read_file_auto(file_path)
        return text
    
    def _extract_markdown_sections(self, text: str) -> list:
        """Extract markdown headers and structure"""
        sections = []
        lines = text.split('\n')
        
        for line in lines:
            # Match markdown headers
            if match := re.match(r'^(#{1,6})\s+(.+)', line):
                level = len(match.group(1))
                title = match.group(2)
                sections.append({
                    "level": level,
                    "title": title
                })
        
        return sections
    
    def _extract_lists(self, text: str) -> list:
        """Extract bullet points and numbered lists"""
        lists = []
        lines = text.split('\n')
        
        for line in lines:
            # Bullet points
            if re.match(r'^\s*[-*+]\s+(.+)', line):
                lists.append(line.strip())
            # Numbered lists
            elif re.match(r'^\s*\d+\.\s+(.+)', line):
                lists.append(line.strip())
        
        return lists
    
    def _generate_summary(self, text: str, max_length: int = 200) -> str:
        """Generate a brief summary of the text"""
        # Take first paragraph or first N characters
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        if paragraphs:
            summary = paragraphs[0]
            if len(summary) > max_length:
                summary = summary[:max_length] + "..."
            return summary
        else:
            return text[:max_length] + "..." if len(text) > max_length else text