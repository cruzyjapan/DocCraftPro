"""PDF file analyzer"""

from typing import Dict, Any, List
from .base import AnalyzerBase
import PyPDF2
from pathlib import Path


class PDFAnalyzer(AnalyzerBase):
    """Analyzer for PDF files"""
    
    def analyze(self, file_path: str) -> Dict[str, Any]:
        """Analyze PDF file and extract information"""
        self.validate_file(file_path)
        
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Extract metadata
            metadata = self._extract_metadata(reader)
            
            # Extract text from all pages
            pages_data = []
            all_text = []
            
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                pages_data.append({
                    "page_number": page_num,
                    "text_length": len(text),
                    "text": text[:500] + "..." if len(text) > 500 else text  # Sample
                })
                all_text.append(f"=== Page {page_num} ===\n{text}")
            
            full_text = '\n\n'.join(all_text)
            
            return {
                "file_info": self.get_file_info(file_path),
                "pdf_info": {
                    "page_count": len(reader.pages),
                    "is_encrypted": reader.is_encrypted,
                    "metadata": metadata
                },
                "pages": pages_data,
                "statistics": {
                    "total_pages": len(reader.pages),
                    "total_characters": len(full_text),
                    "total_words": len(full_text.split()),
                    "average_chars_per_page": len(full_text) // len(reader.pages) if reader.pages else 0
                },
                "full_text": full_text,
                "summary": self._generate_summary(full_text),
                "toc": self._extract_toc(reader)
            }
    
    def extract_text(self, file_path: str) -> str:
        """Extract all text from PDF"""
        self.validate_file(file_path)
        
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            all_text = []
            
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text.strip():
                    all_text.append(f"=== Page {page_num} ===\n{text}")
            
            return '\n\n'.join(all_text)
    
    def _extract_metadata(self, reader: PyPDF2.PdfReader) -> Dict[str, Any]:
        """Extract PDF metadata"""
        metadata = {}
        
        if reader.metadata:
            # Common metadata fields
            fields = ['/Title', '/Author', '/Subject', '/Creator', 
                     '/Producer', '/CreationDate', '/ModDate', '/Keywords']
            
            for field in fields:
                if field in reader.metadata:
                    value = reader.metadata[field]
                    # Convert to string if needed
                    if hasattr(value, '__str__'):
                        metadata[field[1:]] = str(value)
                    else:
                        metadata[field[1:]] = value
        
        return metadata
    
    def _extract_toc(self, reader: PyPDF2.PdfReader) -> List[Dict[str, Any]]:
        """Try to extract table of contents (bookmarks)"""
        toc = []
        
        try:
            if hasattr(reader, 'outline'):
                outline = reader.outline
                if outline:
                    toc = self._process_outline(outline)
        except:
            pass  # TOC extraction might fail for some PDFs
        
        return toc
    
    def _process_outline(self, outline, level: int = 0) -> List[Dict[str, Any]]:
        """Process PDF outline/bookmarks recursively"""
        toc = []
        
        for item in outline:
            if isinstance(item, list):
                # Nested items
                toc.extend(self._process_outline(item, level + 1))
            elif hasattr(item, 'title'):
                # Bookmark item
                entry = {
                    "title": item.title,
                    "level": level
                }
                
                # Try to get page number
                if hasattr(item, 'page') and hasattr(item.page, 'idnum'):
                    entry["page"] = item.page.idnum
                
                toc.append(entry)
        
        return toc
    
    def _generate_summary(self, text: str, max_length: int = 500) -> str:
        """Generate summary of PDF content"""
        # Clean text
        text = ' '.join(text.split())
        
        # Take first part as summary
        if len(text) > max_length:
            # Try to find a sentence boundary
            summary = text[:max_length]
            last_period = summary.rfind('。')
            if last_period == -1:
                last_period = summary.rfind('.')
            
            if last_period > max_length // 2:
                summary = summary[:last_period + 1]
            else:
                summary = summary + "..."
            
            return summary
        else:
            return text