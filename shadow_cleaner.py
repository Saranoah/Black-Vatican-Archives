#!/usr/bin/env python3
"""
🗑️ SHADOW CLEANER - Purge the digital realm of unnecessary files
Cleans temporary files, logs, and cache directories
"""

import os
import shutil
import tempfile
from pathlib import Path

class ShadowCleaner:
    def __init__(self):
        self.temp_paths = [
            tempfile.gettempdir(),
            "/tmp",
            "~/.cache",
            "~/.local/share/Trash",
            "/var/log" # Be careful with this one
        ]
        self.cleaned_size = 0
        
    def purge_shadows(self, path):
        """Remove temporary files and free up space"""
        try:
            path = Path(path).expanduser()
            if path.exists():
                initial_size = self.get_dir_size(path)
                for item in path.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                final_size = self.get_dir_size(path)
                return initial_size - final_size
        except PermissionError:
            print(f"🚫 Access denied to {path}")
        return 0
    
    def get_dir_size(self, path):
        """Calculate directory size"""
        total = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self.get_dir_size(entry.path)
        except:
            pass
        return total
    
    def ritual_cleanse(self):
        """Perform the cleansing ritual"""
        print("🔥 Beginning shadow purge ritual...")
        total_freed = 0
        
        for path in self.temp_paths:
            print(f"🗑️ Purging {path}...")
            freed = self.purge_shadows(path)
            total_freed += freed
            print(f"   💀 Freed: {freed / 1024 / 1024:.2f} MB")
        
        print(f"\n🎉 Ritual complete! Total freed: {total_freed / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    cleaner = ShadowCleaner()
    cleaner.ritual_cleanse()
