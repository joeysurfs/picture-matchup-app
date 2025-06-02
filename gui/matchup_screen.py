import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QSizePolicy, QProgressBar,
                            QScrollArea, QFrame, QDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QFont

from gui.leaderboard_dialog import LeaderboardDialog
from gui.photo_widget import PhotoWidget
from utils.file_renamer import rename_photos

class MatchupScreen(QMainWindow):
    finished = pyqtSignal()
    
    def __init__(self, photo_files, rating_system, output_dir=None):
        super().__init__()
        self.setWindowTitle("Photo Matchup")
        
        # Store output directory
        self.output_dir = output_dir
        
        self.photo_files = photo_files
        self.rating_system = rating_system
        self.isFullScreen = False
        
        # Initialize counters
        self.total_matchups = self.rating_system.estimated_matchups()
        self.completed_matchups = 0
        
        # Set up the UI
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)  # Very small margins for Pi screen
        
        # Header with info - simplified for smaller screen
        header_layout = QHBoxLayout()
        
        # Progress info
        self.progress_label = QLabel("1/{0}".format(self.total_matchups))
        self.progress_label.setStyleSheet("font-size: 12px;")  # Smaller font
        header_layout.addWidget(self.progress_label)
        
        header_layout.addStretch(1)
        
        # Add fullscreen toggle button
        self.fullscreen_button = QPushButton("Fullscreen")
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        self.fullscreen_button.setFixedWidth(80)
        self.fullscreen_button.setFixedHeight(30)
        self.fullscreen_button.setStyleSheet("font-size: 10px;")
        header_layout.addWidget(self.fullscreen_button)
        
        # Rating system info
        system_label = QLabel(f"{self.rating_system.name}")
        system_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        system_label.setStyleSheet("font-size: 12px;")  # Smaller font
        header_layout.addWidget(system_label)
        
        main_layout.addLayout(header_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, self.total_matchups)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximumHeight(15)  # Smaller height
        main_layout.addWidget(self.progress_bar)
        
        # Instructions
        instructions = QLabel("Tap the photo you prefer")
        instructions.setAlignment(Qt.AlignCenter)
        instructions_font = QFont("Arial", 14)
        instructions.setFont(instructions_font)
        main_layout.addWidget(instructions)
        
        # Photos layout - key area that needs to fit the screen
        photos_layout = QHBoxLayout()
        photos_layout.setSpacing(5)  # Smaller spacing between photos
        
        # Create photo widgets
        self.left_photo = PhotoWidget()
        self.right_photo = PhotoWidget()
        
        # Set sizes appropriate for the Pi screen (7-inch, typically 800x480)
        self.left_photo.setMinimumSize(300, 300)  # Smaller for Pi screen
        self.right_photo.setMinimumSize(300, 300)  # Smaller for Pi screen
        
        self.left_photo.clicked.connect(lambda: self.photo_selected(0))
        self.right_photo.clicked.connect(lambda: self.photo_selected(1))
        
        photos_layout.addWidget(self.left_photo)
        photos_layout.addWidget(self.right_photo)
        
        main_layout.addLayout(photos_layout, 1)  # 1 stretch factor
        
        # Bottom buttons - simplified layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(5)  # Smaller spacing
        
        # View leaderboard button
        self.leaderboard_btn = QPushButton("Leaderboard")  # Shorter text
        self.leaderboard_btn.setMinimumHeight(50)  # Larger for touch
        self.leaderboard_btn.setStyleSheet("QPushButton { font-size: 14px; }")  # Smaller font
        self.leaderboard_btn.clicked.connect(self.show_leaderboard)
        buttons_layout.addWidget(self.leaderboard_btn)
        
        # Return to home button
        self.home_btn = QPushButton("Home")  # Shorter text
        self.home_btn.setMinimumHeight(50)  # Larger for touch
        self.home_btn.setStyleSheet("QPushButton { font-size: 14px; }")  # Smaller font
        self.home_btn.clicked.connect(self.return_home)
        buttons_layout.addWidget(self.home_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # Load first matchup
        self.next_matchup()
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        if self.isFullScreen:
            self.showNormal()
            self.fullscreen_button.setText("Fullscreen")
        else:
            self.showFullScreen()
            self.fullscreen_button.setText("Windowed")
        self.isFullScreen = not self.isFullScreen
    
    def next_matchup(self):
        """Load the next photo matchup"""
        # Check if we're done
        if self.rating_system.is_complete():
            self.finish_matchups()
            return
        
        # Get next matchup
        photo1, photo2 = self.rating_system.get_next_matchup()
        
        # Check if we got a valid matchup
        if photo1 is None or photo2 is None:
            self.finish_matchups()
            return
        
        # Update photos
        self.left_photo.load_photo(photo1)
        self.right_photo.load_photo(photo2)
        
        # Update progress
        self.completed_matchups += 1
        self.progress_bar.setValue(self.completed_matchups)
        self.progress_label.setText(f"Matchup {self.completed_matchups} of ~{self.total_matchups}")
    
    def photo_selected(self, selected_index):
        """Handle photo selection"""
        winner = self.left_photo.photo_path if selected_index == 0 else self.right_photo.photo_path
        loser = self.right_photo.photo_path if selected_index == 0 else self.left_photo.photo_path
        
        # Update ratings
        self.rating_system.update_ratings(winner, loser)
        
        # Load next matchup
        self.next_matchup()
    
    def show_leaderboard(self):
        """Show the leaderboard dialog"""
        rankings = self.rating_system.get_current_rankings()
        dialog = LeaderboardDialog(rankings[:10], self)
        
        # Use the same display mode (fullscreen or windowed) for the dialog
        if self.isFullScreen:
            dialog.showFullScreen()
        else:
            dialog.show()
        
        dialog.exec_()
    
    def return_home(self):
        """Return to home screen"""
        self.finished.emit()
        self.close()
    
    def finish_matchups(self):
        """Handle completion of all matchups"""
        # Get final rankings
        rankings = self.rating_system.get_current_rankings()
        
        # Rename files to the output directory if specified
        if self.output_dir and os.path.isdir(self.output_dir):
            rename_photos(rankings, self.output_dir)
        else:
            rename_photos(rankings)
        
        # Show summary dialog with option to return home
        from PyQt5.QtWidgets import QMessageBox
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Matchups Complete")
        msg.setText("All matchups are complete!")
        msg.setInformativeText("The photos have been ranked and saved to the output folder.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        
        # Return to home
        self.return_home()
