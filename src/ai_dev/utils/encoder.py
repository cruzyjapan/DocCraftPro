"""Encoding utilities for handling Shift-JIS and other encodings"""

import codecs
import chardet
from typing import Optional, Tuple
from pathlib import Path


class EncodingHandler:
    """Handle encoding detection and conversion"""
    
    @staticmethod
    def detect_encoding(file_path: str) -> str:
        """Automatically detect file encoding"""
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'
    
    @staticmethod
    def convert_encoding(
        text: str, 
        from_enc: str = 'utf-8', 
        to_enc: str = 'shift-jis'
    ) -> bytes:
        """Convert text encoding"""
        try:
            return text.encode(to_enc, errors='ignore')
        except (UnicodeDecodeError, UnicodeEncodeError) as e:
            # Fallback to replace errors
            return text.encode(to_enc, errors='replace')
    
    @staticmethod
    def read_file_auto(file_path: str) -> Tuple[str, str]:
        """Read file with automatic encoding detection"""
        encoding = EncodingHandler.detect_encoding(file_path)
        
        try:
            with codecs.open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try alternative encodings
            for enc in ['utf-8', 'shift-jis', 'cp932', 'euc-jp', 'iso-2022-jp']:
                try:
                    with codecs.open(file_path, 'r', encoding=enc) as f:
                        content = f.read()
                        encoding = enc
                        break
                except:
                    continue
            else:
                # If all fail, read as binary and decode with errors='ignore'
                with open(file_path, 'rb') as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    encoding = 'utf-8'
        
        return content, encoding
    
    @staticmethod
    def write_file(
        file_path: str, 
        content: str, 
        encoding: str = 'shift-jis',
        add_bom: bool = False,
        line_ending: str = 'crlf'
    ):
        """Write file with specified encoding"""
        # Convert line endings if specified
        if line_ending == 'crlf':
            content = content.replace('\n', '\r\n').replace('\r\r\n', '\r\n')
        elif line_ending == 'lf':
            content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        # Handle BOM for UTF-8
        if add_bom and encoding.lower() in ['utf-8', 'utf8']:
            with open(file_path, 'wb') as f:
                f.write(codecs.BOM_UTF8)
                f.write(content.encode(encoding))
        else:
            with codecs.open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
    
    @staticmethod
    def normalize_encoding_name(encoding: str) -> str:
        """Normalize encoding name to standard format"""
        encoding_map = {
            'shift-jis': 'shift_jis',
            'shiftjis': 'shift_jis',
            'sjis': 'shift_jis',
            'utf8': 'utf-8',
            'utf-8': 'utf-8',
            'cp932': 'cp932',  # Windows Japanese
            'euc-jp': 'euc_jp',
            'eucjp': 'euc_jp',
            'iso-2022-jp': 'iso2022_jp',
            'iso2022jp': 'iso2022_jp'
        }
        return encoding_map.get(encoding.lower(), encoding)