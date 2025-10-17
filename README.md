# Lifts

> Track lifts, push commits, merge gains - The vibecoder's workout tracker

**[How to Use](#how-to-use)**

---

## Bodyweight Exercises

<table>
<tr>
<td width="50%">

### Pull Ups
![Pull Ups](charts/pull_ups.png?t=20251017131116)

</td>
<td width="50%">

### Dips
![Dips](charts/dips.png?t=20251017131116)

</td>
</tr>
<tr>
<td width="50%">

### Pushups
![Pushups](charts/pushups.png?t=20251017131116)

</td>
<td width="50%">

### Bodyweight Squats
![Bodyweight Squats](charts/bodyweight_squats.png?t=20251017131116)

</td>
</tr>
</table>

## Gym Lifts

<table>
<tr>
<td width="50%">

### Bench Press
![Bench Press](charts/bench_press.png?t=20251017131116)

</td>
<td width="50%">

### Squat
![Squat](charts/squat.png?t=20251017131116)

</td>
</tr>
<tr>
<td width="50%">

### Deadlift
![Deadlift](charts/deadlift.png?t=20251017131116)

</td>
<td width="50%">

### Overhead Press
![Overhead Press](charts/overhead_press.png?t=20251017131116)

</td>
</tr>
</table>

---

## How to Use

This project uses **GitHub Actions** to automatically update your workout charts. You can update your workouts directly from GitHub (even from mobile!) without touching any code.

### Method 1: GitHub Actions (Recommended)

Perfect for quick updates on the go from your phone!

#### Update Bodyweight Exercises

1. Go to **Actions** tab in GitHub
2. Select **"Update Bodyweight Workout"**
3. Click **"Run workflow"**
4. Fill in the exercises you completed (leave others empty):
   - Pull Ups: `8`
   - Dips: `12`
   - Pushups: (leave empty if not done)
   - Bodyweight Squats: `25`
5. Click **"Run workflow"**
6. Wait ~1-2 minutes → Charts automatically updated!

#### Update Gym Lifts

1. Go to **Actions** tab in GitHub
2. Select **"Update Gym Workout"**
3. Click **"Run workflow"**
4. Select exercise from dropdown:
   - `bench_press` / `squat` / `deadlift` / `overhead_press`
5. Enter weight and reps:
   - Weight: `75`
   - Reps: `5`
6. Click **"Run workflow"**
7. Wait ~1-2 minutes → Charts automatically updated!

### Method 2: Manual Edit

For advanced users (hahahaaha :D) who prefer editing JSON directly:

#### Bodyweight Exercises

Edit `data/bw_exercises.json`:
```json
{
  "exercises": {
    "pull_ups": {
      "current": 8,
      "history": [2, 3, 4, 5, 6, 7]
    }
  }
}
```

#### Gym Lifts

Edit `data/gym_lifts.json`:
```json
{
  "exercises": {
    "bench_press": {
      "current_weight": 75,
      "current_reps": 5,
      "history": [
        {"weight": 60, "reps": 5},
        {"weight": 70, "reps": 5}
      ]
    }
  }
}
```

Commit and push → GitHub Actions will automatically:
- ✅ Update history
- ✅ Generate new charts
- ✅ Commit changes

### Features

- 🌙 **Crypto-style dark theme charts**
- 📈 **Progress tracking with percentage changes**
- 🎨 **Color-coded trends** (green = gains, red = losses)
- 🔄 **Automatic history management**
- 📱 **Mobile-friendly** (update from GitHub mobile app)
- ⚡ **Optimized CI/CD** (only runs for changed workouts)

### Fork This Repo

Want to track your own workouts?

1. **Fork this repository**
2. **Enable GitHub Actions** in your fork
3. **Update exercises** in JSON files or via Actions
4. **Charts auto-generate** and display in your README!

That's it! Your personal workout tracker is ready 💪

---

### Project Structure

```
lifts/
├── data/
│   ├── bw_exercises.json      # Bodyweight exercise data
│   └── gym_lifts.json         # Gym lift data
├── scripts/
│   ├── common_utils.py        # Shared utilities
│   ├── generate_bw_charts.py  # BW chart generator
│   └── generate_gym_charts.py # Gym chart generator
├── charts/                    # Auto-generated charts
└── .github/workflows/         # GitHub Actions workflows
    ├── update-bw-workout.yml  # Manual BW update
    ├── update-gym-workout.yml # Manual gym update
    └── update-charts.yml      # Auto-update on push
```

### Requirements

- Python 3.11+
- matplotlib
- numpy

All dependencies are automatically installed by GitHub Actions.

---

*Made by vibecoder, for vibecoders 🚀*
