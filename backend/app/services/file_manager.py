"""
File Manager - Generate and manage output files
"""

import os
import json
import zipfile
import io
from typing import Dict, Any
from datetime import datetime

class FileManager:
    """
    Manages generated website files and ZIP creation
    """
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.output_dir = f"outputs/{project_id}"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def save_files(self, code: Dict[str, str]) -> Dict[str, str]:
        """
        Save HTML, CSS, JS files
        
        Args:
            code: Dict with 'html', 'css', 'js' keys
        
        Returns:
            Dict with file paths
        """
        files = {}
        
        # Save HTML
        html_path = os.path.join(self.output_dir, 'index.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(code.get('html', ''))
        files['html'] = html_path
        
        # Save CSS (if separate)
        if code.get('css'):
            css_path = os.path.join(self.output_dir, 'style.css')
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(code.get('css'))
            files['css'] = css_path
        
        # Save JS (if separate)
        if code.get('js'):
            js_path = os.path.join(self.output_dir, 'script.js')
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(code.get('js'))
            files['js'] = js_path
        
        return files
    
    def create_zip(self, files: Dict[str, str]) -> bytes:
        """
        Create ZIP file of all generated files
        
        Args:
            files: Dict of file paths
        
        Returns:
            ZIP file bytes
        """
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_type, file_path in files.items():
                if os.path.exists(file_path):
                    arcname = os.path.basename(file_path)
                    zf.write(file_path, arcname)
        
        return zip_buffer.getvalue()
    
    def save_metadata(self, metadata: Dict[str, Any]):
        """Save project metadata"""
        metadata_path = os.path.join(self.output_dir, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
