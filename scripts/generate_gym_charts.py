#!/usr/bin/env python3
"""
Gym Lift Chart Generator
Generates charts for gym lifts (weight x reps)
"""

import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from common_utils import (
    load_data, save_data, setup_chart_style,
    get_trend_color, COLORS, DISPLAY_NAMES, CHARTS_DIR
)

DATA_FILE = Path(__file__).parent.parent / "data" / "gym_lifts.json"


def update_history(data):
    """Update history with current values if they changed"""
    modified = False

    for exercise_key, exercise_data in data.get('exercises', {}).items():
        current_weight = exercise_data['current_weight']
        current_reps = exercise_data['current_reps']
        history = exercise_data['history']

        current_entry = {"weight": current_weight, "reps": current_reps}

        if not history or history[-1] != current_entry:
            if history and history[-1] != current_entry:
                history.append(current_entry)
                modified = True
            elif not history:
                history.append(current_entry)
                modified = True

    if modified:
        save_data(DATA_FILE, data)
        print("✓ History updated with new values")

    return data


def generate_chart(exercise_key, exercise_data, timestamp):
    """Generate crypto-style chart for gym lift"""
    history = exercise_data['history']
    current_weight = exercise_data['current_weight']
    current_reps = exercise_data['current_reps']

    current_entry = {"weight": current_weight, "reps": current_reps}

    # Only add current if it's different from last history entry
    if not history or history[-1] != current_entry:
        all_entries = history + [current_entry]
    else:
        all_entries = history

    x_values = list(range(1, len(all_entries) + 1))

    # Extract weights for plotting
    all_weights = [entry['weight'] for entry in all_entries]

    fig, ax = plt.subplots(figsize=(12, 7), facecolor='#0d1117')
    ax.set_facecolor('#161b22')

    color = COLORS.get(exercise_key, "#95a5a6")
    display_name = DISPLAY_NAMES.get(exercise_key, exercise_key.replace('_', ' ').title())
    trend_color = get_trend_color(all_weights, color)

    # Plot
    ax.fill_between(x_values, all_weights, alpha=0.15, color=trend_color)
    ax.plot(x_values, all_weights, linewidth=3, color=trend_color, alpha=0.9)
    ax.scatter(x_values, all_weights, s=80, color=trend_color,
               edgecolors='white', linewidths=2, zorder=5)

    # Labels with weight x reps and better padding
    for x, entry in zip(x_values, all_entries):
        weight = entry['weight']
        reps = entry['reps']
        weight_range = max(all_weights) - min(all_weights)
        offset = max(weight_range * 0.15, 1.5) if len(all_weights) > 1 else 1.5
        ax.text(x, weight + offset, f'{int(weight)}kg x {int(reps)}',
                ha='center', va='bottom', fontsize=11, fontweight='bold', color='white')

    # Change indicator for weight
    if len(all_weights) > 1:
        change = all_weights[-1] - all_weights[0]
        pct_change = (change / all_weights[0] * 100) if all_weights[0] != 0 else 0
        change_text = f"+{change}kg" if change >= 0 else f"{change}kg"
        pct_text = f"+{pct_change:.1f}%" if pct_change >= 0 else f"{pct_change:.1f}%"
        change_color = '#00ff88' if change >= 0 else '#ff4444'
        ax.text(0.02, 0.98, f'{change_text} ({pct_text})',
                transform=ax.transAxes, fontsize=14, fontweight='bold',
                color=change_color, va='top', ha='left',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#0d1117',
                         edgecolor=change_color, alpha=0.8))

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
    print("Gym Lift Chart Generator")
    print("=" * 50)

    CHARTS_DIR.mkdir(exist_ok=True)

    print("\nLoading gym lift data...")
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
