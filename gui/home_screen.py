import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QComboBox, 
                            QSpacerItem, QSizePolicy, QFileDialog, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from gui.matchup_screen import MatchupScreen
from rating_systems.rating_factory import RatingFactory
from utils.config import load_config, save_config

class HomeScreen(QMainWindow):
    def __init__(self, input_dir=None, output_dir=None):
        super().__init__()
        self.setWindowTitle("Photo Matchup App")
        
        # Initialize to None, user will select a folder
        self.input_dir = None
        self.output_dir = None
        self.isFullScreen = False
        
        # Load configuration
        self.config = load_config()
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # App title
        title_layout = QHBoxLayout()
        
        # Add fullscreen toggle button in the top right
        self.fullscreen_button = QPushButton("Fullscreen")
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        self.fullscreen_button.setFixedWidth(100)
        
        title_label = QLabel("Photo Matchup")
        title_font = QFont("Arial", 20, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        
        title_layout.addWidget(title_label, 1)
        title_layout.addWidget(self.fullscreen_button)
        
        main_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addLayout(title_layout)
        
        # Subtitle
        subtitle_label = QLabel("Tap to choose your preferred photo")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_font = QFont("Arial", 12)
        subtitle_label.setFont(subtitle_font)
        main_layout.addWidget(subtitle_label)
        main_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Folder selection
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Images from:")
        self.folder_path_label = QLabel("No folder selected")
        self.folder_path_label.setStyleSheet("color: #aaaaaa;")
        self.select_folder_button = QPushButton("Select Folder")
        self.select_folder_button.clicked.connect(self.select_input_folder)
        self.select_folder_button.setMinimumHeight(40)  # Larger for touch
        
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_path_label, 1)  # 1 gives it stretch
        folder_layout.addWidget(self.select_folder_button)
        
        main_layout.addLayout(folder_layout)
        main_layout.addSpacing(10)
        
        # Photo count
        self.photo_count_label = QLabel("Photos: 0")
        main_layout.addWidget(self.photo_count_label)
        main_layout.addSpacing(10)
        
        # Rating system selection
        rating_layout = QHBoxLayout()
        rating_label = QLabel("Rating System:")
        self.rating_combo = QComboBox()
        self.rating_combo.setStyleSheet("QComboBox { min-height: 40px; }")  # Larger for touch
        
        # Add rating systems with detailed explanations
        self.rating_systems = {
            "Quick Sort": {
                "short": "Quick and efficient sorting algorithm",
                "long": "Quick Sort is a divide-and-conquer algorithm that works by partitioning an array into two sub-arrays, then sorting the sub-arrays recursively. For images, this means fewer comparisons (n log n) than other methods. Real-world uses include sorting large datasets in database systems, programming language implementations, and in various computer science applications."
            },
            "Simple": {
                "short": "Basic win/loss counting system",
                "long": "The Simple rating system counts wins and losses for each item. It's straightforward to implement and understand but requires comparing all possible pairs (n²/2 comparisons). In the real world, it's used in basic sports rankings, informal competitions, and situations where simplicity is valued over statistical precision."
            }, 
            "Elo": {
                "short": "Chess rating system adapted for photos",
                "long": "The Elo rating system, originally developed for chess rankings, calculates the relative skill levels between competitors. When comparing photos, higher-rated photos are expected to win against lower-rated ones. The system adjusts ratings based on actual outcomes vs. expected outcomes. Used in chess, sports leagues, video games (like League of Legends), and matchmaking systems worldwide."
            },
            "Bradley-Terry": {
                "short": "Statistical model for paired comparisons",
                "long": "The Bradley-Terry model is a probability model that predicts the outcome of paired comparisons. It assumes the probability of item A being chosen over item B is related to their underlying 'strength' parameters. Real-world applications include preference testing in market research, sports analytics, ranking systems in academia, and various choice modeling scenarios in psychology."
            },
            "Glicko-2": {
                "short": "Enhanced Elo with rating deviation",
                "long": "Glicko-2 extends the Elo system by tracking both a rating and a 'rating deviation' (uncertainty) for each item. This allows the system to be more cautious with items that have few comparisons. Used in online gaming platforms (such as Chess.com), competitive gaming leagues, and sports rating systems where the reliability of a rating is important."
            },
            "TrueSkill": {
                "short": "Microsoft's skill rating system",
                "long": "TrueSkill was developed by Microsoft Research for Xbox Live to match players in competitive games. It uses Bayesian inference to track both skill level and uncertainty. TrueSkill allows for team-based and multiplayer rankings, and converges quickly with fewer comparisons. Used in Xbox Live matchmaking, Halo tournaments, and other gaming platforms to create balanced matches between players."
            }
        }
        
        for system in self.rating_systems:
            self.rating_combo.addItem(system)
        
        self.rating_combo.setMinimumWidth(180)
        self.rating_combo.currentTextChanged.connect(self.update_matchup_info)
        
        rating_layout.addWidget(rating_label)
        rating_layout.addWidget(self.rating_combo, 1)  # 1 gives it stretch
        
        main_layout.addLayout(rating_layout)
        main_layout.addSpacing(10)
        
        # Rating system description (short version)
        self.rating_description = QLabel(self.rating_systems["Quick Sort"]["short"])
        self.rating_description.setStyleSheet("color: #aaaaaa;")
        main_layout.addWidget(self.rating_description)
        main_layout.addSpacing(5)
        
        # Detailed system explanation (long version)
        self.rating_explanation = QTextEdit()
        self.rating_explanation.setReadOnly(True)
        self.rating_explanation.setMinimumHeight(100)
        self.rating_explanation.setMaximumHeight(150)
        self.rating_explanation.setText(self.rating_systems["Quick Sort"]["long"])
        self.rating_explanation.setStyleSheet("background-color: #2a2a2a; border: 1px solid #3a3a3a; color: #dddddd; padding: 5px;")
        main_layout.addWidget(self.rating_explanation)
        main_layout.addSpacing(10)
        
        # Matchup info
        self.matchup_info = QLabel("Estimated matchups: 0")
        main_layout.addWidget(self.matchup_info)
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Start button
        self.start_button = QPushButton("Start Matchups")
        self.start_button.setEnabled(False)
        self.start_button.setMinimumHeight(60)  # Larger for touch
        self.start_button.setStyleSheet("QPushButton { font-size: 16px; }")  # Larger text
        self.start_button.clicked.connect(self.start_matchups)
        
        # Exit button
        self.exit_button = QPushButton("Exit")
        self.exit_button.setMinimumHeight(60)  # Larger for touch
        self.exit_button.setStyleSheet("QPushButton { font-size: 16px; background-color: #AA3333; }")
        self.exit_button.clicked.connect(self.close)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.exit_button)
        main_layout.addLayout(button_layout)
        
        # Initialize variables
        self.folder_path = None
        self.photo_files = []
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        if self.isFullScreen:
            self.showNormal()
            self.fullscreen_button.setText("Fullscreen")
        else:
            self.showFullScreen()
            self.fullscreen_button.setText("Windowed")
        self.isFullScreen = not self.isFullScreen
    
    def select_input_folder(self):
        """Allow user to select input folder"""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder_path:
            self.load_folder(folder_path)
    
    def load_folder(self, folder_path):
        """Load photos from the specified folder"""
        self.folder_path = folder_path
        self.input_dir = folder_path
        # Set output directory as a subfolder named "ranked_list" within the input directory
        self.output_dir = os.path.join(folder_path, "ranked_list")
        
        self.folder_path_label.setText(folder_path)
        
        # Get all image files in the folder
        self.photo_files = [
            os.path.join(folder_path, f) for f in os.listdir(folder_path)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'))
        ]
        
        # Update photo count
        self.photo_count_label.setText(f"Photos: {len(self.photo_files)}")
        
        # Enable start button if photos found
        self.start_button.setEnabled(len(self.photo_files) > 1)
        
        # Update matchup info
        self.update_matchup_info()
    
    def update_matchup_info(self):
        if not self.photo_files:
            selected_system = self.rating_combo.currentText()
            self.rating_description.setText(self.rating_systems[selected_system]["short"])
            self.rating_explanation.setText(self.rating_systems[selected_system]["long"])
            self.matchup_info.setText("Estimated matchups: 0")
            return
        
        # Get estimated matchups based on selected algorithm
        selected_system = self.rating_combo.currentText()
        num_photos = len(self.photo_files)
        self.rating_description.setText(self.rating_systems[selected_system]["short"])
        self.rating_explanation.setText(self.rating_systems[selected_system]["long"])
        
        if selected_system == "Quick Sort":
            # Quick Sort is approximately n log n comparisons
            est_matchups = int(num_photos * (num_photos.bit_length() - 1))
        elif selected_system == "Simple":
            # Simple system needs n(n-1)/2 comparisons (all pairs)
            est_matchups = num_photos * (num_photos - 1) // 2
        elif selected_system in ["Elo", "Glicko-2", "TrueSkill"]:
            # These need fewer comparisons, roughly 5-7 per photo
            est_matchups = num_photos * 6
        elif selected_system == "Bradley-Terry":
            # Bradley-Terry typically needs more data, ~10 comparisons per photo
            est_matchups = num_photos * 10
        else:
            est_matchups = num_photos * num_photos.bit_length()
        
        self.matchup_info.setText(f"Estimated matchups: {est_matchups}")
    
    def start_matchups(self):
        if not self.photo_files or len(self.photo_files) < 2:
            return
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create rating system
        selected_system = self.rating_combo.currentText()
        rating_system = RatingFactory.create_rating_system(
            selected_system, self.photo_files
        )
        
        # Launch matchup screen in the same mode (fullscreen or windowed)
        self.matchup_screen = MatchupScreen(self.photo_files, rating_system, self.output_dir)
        if self.isFullScreen:
            self.matchup_screen.showFullScreen()
        else:
            self.matchup_screen.resize(800, 600)
            self.matchup_screen.show()
        self.hide()
        
        # Connect signals
        self.matchup_screen.finished.connect(self.show)
