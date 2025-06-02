# Photo Matchup App

A modern application for ranking photos through pairwise comparisons.

## Features

- Multiple rating algorithms (Quick Sort, Elo, TrueSkill, etc.)
- Dark theme for optimal photo comparison
- Automatic file renaming based on rankings
- Real-time leaderboard to track progress

## Installation

1. Ensure you have Python 3.6+ installed
2. Clone or download this repository
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python main.py
```

2. Select a folder containing photos
3. Choose a rating system:
   - Quick Sort: Fast algorithm requiring fewest comparisons
   - Simple: Basic win/loss counting (compares all pairs)
   - Elo: Chess rating system adapted for photos
   - Bradley-Terry: Statistical model for paired comparisons
   - Glicko-2: Enhanced Elo with rating deviation
   - TrueSkill: Microsoft's skill rating system for Xbox Live
   
4. Click "Start Matchups" and select your preferred photo in each pair
5. Once complete, your photos will be renamed in your source folder with rank prefixes

## Rating Systems

Each rating system has different characteristics:

- **Quick Sort**: Fastest option, but less accurate. Good for initial sorting.
- **Simple**: Most thorough but requires the most comparisons. Best for small collections.
- **Elo**: Good balance of speed and accuracy. Classic option.
- **Bradley-Terry**: Statistical approach that requires more data but provides robust rankings.
- **Glicko-2**: Evolution of Elo that tracks uncertainty. Good for ongoing sorting.
- **TrueSkill**: Most sophisticated system. Excellent at finding true rankings with fewer comparisons.

## Credits

Created with PyQt5 and Pillow.
