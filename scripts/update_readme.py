#!/usr/bin/env python3
"""
Update README with latest chart filenames and clean up old charts
"""

from pathlib import Path
import re

def update_readme_with_latest_charts():
    """Update README with latest chart filenames and remove old chart files"""
    charts_dir = Path(__file__).parent.parent / "charts"
    readme_path = Path(__file__).parent.parent / "README.md"

    # Get all chart files grouped by exercise
    chart_files = {}
    for chart_file in charts_dir.glob("*.png"):
        # Extract exercise name from filename (e.g., "pull_ups_20251017131116.png" -> "pull_ups")
        match = re.match(r'([a-z_]+)_\d+\.png', chart_file.name)
        if match:
            exercise_name = match.group(1)
            if exercise_name not in chart_files:
                chart_files[exercise_name] = []
            chart_files[exercise_name].append(chart_file)

    # Keep only the latest file for each exercise, delete old ones
    latest_charts = {}
    for exercise, files in chart_files.items():
        # Sort by modification time, keep the newest
        files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        latest_charts[exercise] = files[0].name

        # Delete old files
        for old_file in files[1:]:
            print(f"✓ Deleting old chart: {old_file.name}")
            old_file.unlink()

    # Update README
    readme_content = readme_path.read_text()

    for exercise, filename in latest_charts.items():
        # Pattern to match old chart references
        pattern = rf'(\!\[.*?\]\(charts/{exercise}(?:_\d+)?\.png(?:\?t=\d+)?\))'
        replacement = f'![{exercise.replace("_", " ").title()}](charts/{filename})'
        readme_content = re.sub(pattern, replacement, readme_content)

    readme_path.write_text(readme_content)
    print(f"✓ README updated with {len(latest_charts)} chart references")

if __name__ == "__main__":
    update_readme_with_latest_charts()
