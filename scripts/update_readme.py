#!/usr/bin/env python3
"""
Update README with cache-busting timestamps for chart images
"""

from pathlib import Path
from datetime import datetime
import re

def update_readme_timestamps():
    """Add/update timestamps in README image URLs to bust cache"""
    readme_path = Path(__file__).parent.parent / "README.md"
    readme_content = readme_path.read_text()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Pattern to match: ![Alt Text](charts/filename.png) or ![Alt Text](charts/filename.png?t=timestamp)
    pattern = r'(\!\[.*?\]\(charts/.*?\.png)(\?t=\d+)?(\))'
    replacement = rf'\1?t={timestamp}\3'

    updated_content = re.sub(pattern, replacement, readme_content)

    if updated_content != readme_content:
        readme_path.write_text(updated_content)
        print(f"✓ README updated with timestamp: {timestamp}")
    else:
        print("✓ README already up to date")

if __name__ == "__main__":
    update_readme_timestamps()
