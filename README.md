# Photo Matchup App

A sophisticated PyQt5-based application for ranking photos through pairwise comparisons using advanced rating algorithms. Originally designed for Raspberry Pi touch screens but works on any desktop platform.

## 🎯 Overview

The Photo Matchup App helps you rank collections of photos by presenting them in pairs and asking you to choose your preference. Using proven rating algorithms from competitive gaming, chess, and statistical analysis, it efficiently determines the relative ranking of your entire photo collection with minimal comparisons.

## ✨ Features

### Core Functionality
- **Folder Selection**: Choose any folder containing your photos
- **Multiple Rating Systems**: Six different algorithms to suit various needs
- **Automatic Ranking**: Photos are automatically ranked and saved with numerical prefixes
- **Progress Tracking**: Real-time progress bar and comparison counter
- **Live Leaderboard**: View current rankings at any time during the process

### User Interface
- **Dark Theme**: Optimized for photo comparison and reduced eye strain
- **Touch-Friendly**: Large buttons and intuitive interface designed for touch screens
- **Windowed/Fullscreen**: Start in windowed mode with option to toggle fullscreen
- **Responsive Design**: Adapts to different screen sizes and orientations
- **Visual Feedback**: Clear hover and selection states for better user experience

### Technical Features
- **EXIF Orientation**: Automatically handles photo rotation based on EXIF data
- **Image Optimization**: Intelligent resizing for performance on lower-end hardware
- **Virtual Environment Support**: Clean dependency management
- **Cross-Platform**: Works on Linux, Windows, and macOS

## 🎲 Rating Systems

Each rating system offers different trade-offs between accuracy, speed, and statistical rigor:

### Quick Sort
- **Algorithm**: Divide-and-conquer sorting algorithm
- **Comparisons**: ~n log n (most efficient)
- **Best For**: Large collections where speed is priority
- **Real-World Use**: Database sorting, programming language implementations
- **Pros**: Fastest, requires fewest comparisons
- **Cons**: Less statistically robust than other methods

### Simple Rating
- **Algorithm**: Basic win/loss counting
- **Comparisons**: n(n-1)/2 (all possible pairs)
- **Best For**: Small collections, maximum thoroughness
- **Real-World Use**: Basic sports rankings, informal competitions
- **Pros**: Simple to understand, most thorough
- **Cons**: Requires most comparisons, time-consuming for large collections

### Elo Rating
- **Algorithm**: Chess rating system adapted for photos
- **Comparisons**: ~6n (moderate efficiency)
- **Best For**: Balanced accuracy and speed
- **Real-World Use**: Chess rankings, League of Legends, sports leagues
- **Pros**: Proven algorithm, good balance of speed and accuracy
- **Cons**: Can be sensitive to initial ratings

### Bradley-Terry Model
- **Algorithm**: Statistical probability model for paired comparisons
- **Comparisons**: ~10n (more data for statistical accuracy)
- **Best For**: When statistical rigor is important
- **Real-World Use**: Market research, academic rankings, psychology studies
- **Pros**: Statistically robust, handles inconsistencies well
- **Cons**: Requires more comparisons for accuracy

### Glicko-2
- **Algorithm**: Enhanced Elo with rating deviation tracking
- **Comparisons**: ~6n (similar to Elo)
- **Best For**: Ongoing ranking projects, uncertainty tracking
- **Real-World Use**: Chess.com, competitive gaming platforms
- **Pros**: Tracks confidence in ratings, handles inactivity
- **Cons**: More complex than basic Elo

### TrueSkill
- **Algorithm**: Microsoft's Bayesian skill rating system
- **Comparisons**: ~6n (efficient convergence)
- **Best For**: Most accurate rankings with reasonable time investment
- **Real-World Use**: Xbox Live matchmaking, Halo tournaments
- **Pros**: Fast convergence, excellent accuracy, handles uncertainty
- **Cons**: Most complex algorithm

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Virtual environment support (recommended)

### Quick Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd picture-matchup-app
   ```

2. **Run the setup script** (handles virtual environment and dependencies):
   ```bash
   chmod +x start_photo_matchup.sh
   ./start_photo_matchup.sh
   ```

### Manual Installation

1. **Create virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 📋 Dependencies

- **PyQt5** (5.15.9): GUI framework
- **Pillow** (≥10.0.0): Image processing and EXIF handling
- **NumPy** (≥1.26.0): Numerical computations for rating algorithms

## 💻 Usage

### Getting Started

1. **Launch the application**:
   ```bash
   ./start_photo_matchup.sh
   ```
   Or manually: `python main.py`

2. **Select your photo folder**:
   - Click "Select Folder" button
   - Choose a folder containing your photos (supports: PNG, JPG, JPEG, BMP, GIF, TIFF)

3. **Choose a rating system**:
   - Read the detailed explanation for each system
   - Consider your collection size and time available
   - View estimated number of comparisons

4. **Start the comparison process**:
   - Click "Start Matchups"
   - For each pair, click the photo you prefer
   - View progress in real-time

5. **Review and complete**:
   - Use "Leaderboard" button to see current rankings
   - Continue until all necessary comparisons are done
   - Photos are automatically saved with rank prefixes

### Output

Ranked photos are saved in a `ranked_list` subfolder within your input directory:
```
your-photos/
├── IMG_001.jpg
├── IMG_002.jpg
├── IMG_003.jpg
└── ranked_list/
    ├── 001_IMG_002.jpg  # Highest ranked
    ├── 002_IMG_001.jpg  # Second place
    └── 003_IMG_003.jpg  # Third place
```

### Interface Controls

- **Fullscreen Toggle**: Switch between windowed and fullscreen modes
- **Leaderboard**: View current rankings during comparison
- **Home**: Return to main screen
- **Progress Bar**: Visual indicator of completion percentage

## 🏗️ Project Structure

```
picture-matchup-app/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── start_photo_matchup.sh  # Setup and launch script
├── README.md              # This file
├── gui/                   # User interface components
│   ├── __init__.py
│   ├── dark_theme.py      # Dark theme styling
│   ├── home_screen.py     # Main selection screen
│   ├── matchup_screen.py  # Photo comparison interface
│   ├── photo_widget.py    # Photo display component
│   └── leaderboard_dialog.py  # Rankings display
├── rating_systems/        # Rating algorithm implementations
│   ├── __init__.py
│   ├── base_rating.py     # Abstract base class
│   ├── quicksort_rating.py
│   ├── simple_rating.py
│   ├── elo_rating.py
│   ├── bradley_terry_rating.py
│   ├── glicko2_rating.py
│   ├── trueskill_rating.py
│   └── rating_factory.py  # Rating system factory
└── utils/                 # Utility functions
    ├── __init__.py
    ├── config.py          # Configuration management
    └── file_renamer.py    # Output file handling
```

## 🔧 Configuration

The application stores user preferences and configuration in a local config file. Settings are automatically saved and restored between sessions.

## 🎮 Hardware Optimization

### Raspberry Pi Specific Features
- Optimized image loading and display for ARM processors
- Touch-friendly interface with large buttons
- Reduced memory footprint for limited RAM environments
- Efficient image thumbnailing to prevent memory issues

### Performance Tips
- For collections over 100 photos, consider Quick Sort or Elo systems
- Use fullscreen mode on small screens for better photo visibility
- Close other applications to free memory on resource-constrained systems

## 🐛 Troubleshooting

### Common Issues

**Virtual Environment Not Activating**:
```bash
# Ensure the script is executable
chmod +x start_photo_matchup.sh

# Run with explicit bash
bash start_photo_matchup.sh
```

**Image Loading Errors**:
- Ensure photos are in supported formats (PNG, JPG, JPEG, BMP, GIF, TIFF)
- Check file permissions on the photo directory
- Verify the folder contains actual image files

**Memory Issues on Raspberry Pi**:
- Use Quick Sort for large collections
- Close unnecessary applications
- Consider using smaller image files if possible

**GUI Display Issues**:
- Ensure PyQt5 is properly installed
- Try running in different screen resolutions
- Use fullscreen mode if interface elements are cut off

### Debug Mode

For troubleshooting, run with verbose output:
```bash
python main.py --debug
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional rating algorithms
- Performance optimizations
- New export formats
- Accessibility improvements
- Mobile platform support

## 📜 License

This project is open source. Please check the license file for specific terms.

## 🏆 Acknowledgments

- **Elo Rating System**: Arpad Elo's chess rating system
- **TrueSkill**: Microsoft Research's skill rating algorithm
- **Bradley-Terry Model**: Statistical paired comparison framework
- **Glicko-2**: Mark Glickman's enhanced rating system
- **PyQt5**: Cross-platform GUI framework
- **Pillow**: Python Imaging Library for image processing

## 📞 Support

For issues, questions, or contributions, please refer to the project repository or contact the maintainers.
