#!/usr/bin/env python3
"""
Bodyweight Exercise Chart Generator
Generates charts for bodyweight exercises (reps only)
"""

import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from common_utils import (
    load_data, save_data, setup_chart_style, add_change_indicator,
    get_trend_color, COLORS, DISPLAY_NAMES, CHARTS_DIR
)

DATA_FILE = Path(__file__).parent.parent / "data" / "bw_exercises.json"


def update_history(data):
    """Update history with current values if they changed"""
    modified = False

    for exercise_key, exercise_data in data.get('exercises', {}).items():
        current = exercise_data['current']
        history = exercise_data['history']

        if not history or history[-1] != current:
            if history and history[-1] != current:
                history.append(current)
                modified = True
            elif not history:
                history.append(current)
                modified = True

    if modified:
        save_data(DATA_FILE, data)
        print("✓ History updated with new values")

    return data


def generate_chart(exercise_key, exercise_data, timestamp):
    """Generate crypto-style chart for bodyweight exercise"""
    history = exercise_data['history']
    current = exercise_data['current']

    # Only add current if it's different from last history value
    if not history or history[-1] != current:
        all_values = history + [current]
    else:
        all_values = history

    x_values = list(range(1, len(all_values) + 1))

    fig, ax = plt.subplots(figsize=(12, 7), facecolor='#0d1117')
    ax.set_facecolor('#161b22')

    color = COLORS.get(exercise_key, "#95a5a6")
    display_name = DISPLAY_NAMES.get(exercise_key, exercise_key.replace('_', ' ').title())
    trend_color = get_trend_color(all_values, color)

    # Plot
    ax.fill_between(x_values, all_values, alpha=0.15, color=trend_color)
    ax.plot(x_values, all_values, linewidth=3, color=trend_color, alpha=0.9)
    ax.scatter(x_values, all_values, s=80, color=trend_color,
               edgecolors='white', linewidths=2, zorder=5)

    # Labels with better padding
    for x, value in zip(x_values, all_values):
        value_range = max(all_values) - min(all_values)
        offset = max(value_range * 0.15, 0.8) if len(all_values) > 1 else 0.8
        ax.text(x, value + offset, f'{int(value)}', ha='center', va='bottom',
                fontsize=12, fontweight='bold', color='white')

    # Change indicator
    add_change_indicator(ax, all_values)

    # Styling
    ax.set_xlabel('Session', fontsize=12, fontweight='bold', color='#8b949e')
    ax.set_ylabel('', fontsize=12, fontweight='bold', color='#8b949e')
    ax.set_title(f'{display_name}', fontsize=16, fontweight='bold',
                 pad=20, color='white')
    setup_chart_style(ax, x_values)

    plt.tight_layout()
    output_path = CHARTS_DIR / f"{exercise_key}_{timestamp}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0d1117')
    print(f"✓ {display_name} chart saved: {output_path}")
    plt.close()
    return f"{exercise_key}_{timestamp}.png"


def main():
    """Main execution function"""
    print("=" * 50)
    print("Bodyweight Exercise Chart Generator")
    print("=" * 50)

    CHARTS_DIR.mkdir(exist_ok=True)

    print("\nLoading bodyweight exercise data...")
    data = load_data(DATA_FILE)

    print("\nChecking for updates...")
    data = update_history(data)

    print("\nGenerating charts...")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    chart_filenames = {}
    for exercise_key, exercise_data in data.get('exercises', {}).items():
        filename = generate_chart(exercise_key, exercise_data, timestamp)
        chart_filenames[exercise_key] = filename

    print("\n" + "=" * 50)
    print("Chart generation complete!")
    print("=" * 50)

    return chart_filenames


if __name__ == "__main__":
    main()
