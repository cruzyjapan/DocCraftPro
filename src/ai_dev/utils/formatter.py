"""Output formatting utilities"""

import json
import csv
from io import StringIO
from typing import List, Dict, Any
from tabulate import tabulate


class OutputFormatter:
    """Format output data into various formats"""
    
    @staticmethod
    def to_markdown(data: List[Dict[str, Any]], title: str = "") -> str:
        """Convert data to Markdown table format"""
        if not data:
            return "No data available"
        
        # Build markdown content
        lines = []
        if title:
            lines.append(f"# {title}")
            lines.append("")
        
        # Prepare data for tabulate - convert complex values to strings
        formatted_data = []
        for item in data:
            formatted_item = {}
            for key, value in item.items():
                if isinstance(value, (list, tuple)):
                    # Convert list to numbered string
                    formatted_value = "\n".join([f"{i+1}. {v}" for i, v in enumerate(value)])
                elif isinstance(value, dict):
                    # Convert dict to string representation
                    formatted_value = str(value)
                else:
                    formatted_value = str(value)
                formatted_item[key] = formatted_value
            formatted_data.append(formatted_item)
        
        # Get headers from first item
        headers = list(formatted_data[0].keys()) if formatted_data else []
        
        # Create table using tabulate
        table = tabulate(formatted_data, headers="keys", tablefmt="github")
        lines.append(table)
        
        return "\n".join(lines)
    
    @staticmethod
    def to_csv(data: List[Dict[str, Any]]) -> str:
        """Convert data to CSV format"""
        if not data:
            return ""
        
        output = StringIO()
        headers = list(data[0].keys())
        writer = csv.DictWriter(output, fieldnames=headers)
        
        writer.writeheader()
        writer.writerows(data)
        
        return output.getvalue()
    
    @staticmethod
    def to_json(data: List[Dict[str, Any]], indent: int = 2) -> str:
        """Convert data to JSON format"""
        return json.dumps(data, ensure_ascii=False, indent=indent)
    
    @staticmethod
    def to_html(data: List[Dict[str, Any]], title: str = "") -> str:
        """Convert data to HTML table format"""
        if not data:
            return "<p>No data available</p>"
        
        html_parts = []
        
        # Start HTML document
        html_parts.append("<!DOCTYPE html>")
        html_parts.append("<html>")
        html_parts.append("<head>")
        html_parts.append('<meta charset="UTF-8">')
        if title:
            html_parts.append(f"<title>{title}</title>")
        html_parts.append("<style>")
        html_parts.append("table { border-collapse: collapse; width: 100%; }")
        html_parts.append("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }")
        html_parts.append("th { background-color: #f2f2f2; }")
        html_parts.append("tr:nth-child(even) { background-color: #f9f9f9; }")
        html_parts.append("</style>")
        html_parts.append("</head>")
        html_parts.append("<body>")
        
        if title:
            html_parts.append(f"<h1>{title}</h1>")
        
        # Create table
        html_parts.append("<table>")
        
        # Headers
        headers = list(data[0].keys())
        html_parts.append("<thead>")
        html_parts.append("<tr>")
        for header in headers:
            html_parts.append(f"<th>{header}</th>")
        html_parts.append("</tr>")
        html_parts.append("</thead>")
        
        # Body
        html_parts.append("<tbody>")
        for row in data:
            html_parts.append("<tr>")
            for header in headers:
                value = row.get(header, "")
                html_parts.append(f"<td>{value}</td>")
            html_parts.append("</tr>")
        html_parts.append("</tbody>")
        
        html_parts.append("</table>")
        html_parts.append("</body>")
        html_parts.append("</html>")
        
        return "\n".join(html_parts)
    
    @staticmethod
    def format_output(
        data: List[Dict[str, Any]], 
        format: str = "markdown", 
        title: str = ""
    ) -> str:
        """Format data based on specified format"""
        formatters = {
            'markdown': lambda d: OutputFormatter.to_markdown(d, title),
            'md': lambda d: OutputFormatter.to_markdown(d, title),
            'csv': OutputFormatter.to_csv,
            'json': OutputFormatter.to_json,
            'html': lambda d: OutputFormatter.to_html(d, title)
        }
        
        formatter = formatters.get(format.lower())
        if formatter:
            return formatter(data)
        else:
            raise ValueError(f"Unsupported format: {format}")