from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                          QScrollArea, QWidget, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QImage
from PIL import Image, ImageQt
from PIL.ImageOps import exif_transpose
import os
import traceback

class LeaderboardDialog(QDialog):
    def __init__(self, rankings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Current Leaderboard")
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)  # Smaller margins for touch screen
        
        # Title
        title = QLabel("Current Top Photos")
        title_font = QFont("Arial", 16, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Scroll area for rankings
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Always show scrollbar for touch dragging
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)  # More space between items for touch
        
        # Add rankings
        for i, (photo_path, score) in enumerate(rankings):
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_widget.setStyleSheet("background-color: #303030; border-radius: 5px;")  # Visual separation
            
            # Rank number
            rank_label = QLabel(f"{i+1}.")
            rank_label.setFont(QFont("Arial", 14, QFont.Bold))
            rank_label.setMinimumWidth(40)
            item_layout.addWidget(rank_label)
            
            # Thumbnail
            try:
                # Try with PIL to handle all formats and rotations
                pil_image = Image.open(photo_path)
                pil_image = exif_transpose(pil_image)
                
                # Create thumbnail
                pil_image.thumbnail((120, 120))  # Larger thumbnail for touch screen
                
                # Convert PIL image to QImage then to QPixmap
                if pil_image.mode == "RGB":
                    data = pil_image.tobytes("raw", "RGB")
                    qimage = QImage(data, pil_image.width, pil_image.height, pil_image.width * 3, QImage.Format_RGB888)
                elif pil_image.mode == "RGBA":
                    data = pil_image.tobytes("raw", "RGBA")
                    qimage = QImage(data, pil_image.width, pil_image.height, pil_image.width * 4, QImage.Format_RGBA8888)
                else:
                    # Convert to RGB for other modes
                    pil_image = pil_image.convert("RGB")
                    data = pil_image.tobytes("raw", "RGB")
                    qimage = QImage(data, pil_image.width, pil_image.height, pil_image.width * 3, QImage.Format_RGB888)
                
                pixmap = QPixmap.fromImage(qimage)
                
                thumbnail = QLabel()
                thumbnail.setPixmap(pixmap)
                thumbnail.setFixedSize(120, 120)  # Larger for touch screen
                thumbnail.setAlignment(Qt.AlignCenter)
                thumbnail.setStyleSheet("background-color: #252525; border: 1px solid #555555;")
                item_layout.addWidget(thumbnail)
                
            except Exception as e:
                print(f"Error loading thumbnail for {photo_path}: {str(e)}")
                traceback.print_exc()
                placeholder = QLabel("Error loading")
                placeholder.setFixedSize(120, 120)  # Larger for touch screen
                placeholder.setAlignment(Qt.AlignCenter)
                placeholder.setStyleSheet("background-color: #252525; border: 1px solid #555555;")
                item_layout.addWidget(placeholder)
            
            # Filename - truncate if too long
            filename = os.path.basename(photo_path)
            if len(filename) > 25:  # Truncate long filenames
                filename = filename[:22] + "..."
                
            filename_label = QLabel(filename)
            filename_label.setStyleSheet("font-size: 14px;")  # Larger text for touch screen
            item_layout.addWidget(filename_label, 1)  # 1 gives it stretch
            
            # Score
            score_label = QLabel(f"Score: {score:.1f}")  # Simplified score display
            score_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            score_label.setStyleSheet("font-size: 14px;")  # Larger text for touch screen
            item_layout.addWidget(score_label)
            
            scroll_layout.addWidget(item_widget)
        
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.setMinimumHeight(60)  # Larger for touch
        close_button.setStyleSheet("QPushButton { font-size: 16px; }")
        close_button.clicked.connect(self.accept)
        main_layout.addWidget(close_button)
