#!/usr/bin/env python3
"""
Common utilities for workout chart generation
"""

import json
import matplotlib.pyplot as plt
from pathlib import Path

# Configuration
CHARTS_DIR = Path(__file__).parent.parent / "charts"

# Color scheme
COLORS = {
    # Bodyweight exercises
    "pull_ups": "#96CEB4",
    "dips": "#FF6B6B",
    "pushups": "#FFA726",
    "bodyweight_squats": "#45B7D1",
    # Gym lifts
    "bench_press": "#E91E63",
    "squat": "#9C27B0",
    "deadlift": "#FF5722",
    "overhead_press": "#00BCD4"
}

# Display names
DISPLAY_NAMES = {
    # Bodyweight exercises
    "pull_ups": "Pull Ups",
    "dips": "Dips",
    "pushups": "Pushups",
    "bodyweight_squats": "Bodyweight Squats",
    # Gym lifts
    "bench_press": "Bench Press",
    "squat": "Squat",
    "deadlift": "Deadlift",
    "overhead_press": "Overhead Press"
}


def load_data(file_path):
    """Load workout data from JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)


def save_data(file_path, data):
    """Save workout data to JSON file"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def setup_chart_style(ax, x_values):
    """Apply common crypto-style chart styling"""
    ax.grid(True, alpha=0.1, linestyle='-', color='#8b949e')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#30363d')
    ax.spines['bottom'].set_color('#30363d')
    ax.tick_params(colors='#8b949e', which='both')
    ax.set_xticks(x_values)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))


def add_change_indicator(ax, values):
    """Add percentage change indicator to chart"""
    if len(values) > 1:
        change = values[-1] - values[0]
        pct_change = (change / values[0] * 100) if values[0] != 0 else 0
        change_text = f"+{change}" if change >= 0 else f"{change}"
        pct_text = f"+{pct_change:.1f}%" if pct_change >= 0 else f"{pct_change:.1f}%"
        change_color = '#00ff88' if change >= 0 else '#ff4444'
        ax.text(0.02, 0.98, f'{change_text} ({pct_text})',
                transform=ax.transAxes, fontsize=14, fontweight='bold',
                color=change_color, va='top', ha='left',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#0d1117',
                         edgecolor=change_color, alpha=0.8))


def get_trend_color(values, default_color):
    """Determine trend color based on values"""
    if len(values) > 1:
        return '#00ff88' if values[-1] >= values[0] else '#ff4444'
    return default_color
