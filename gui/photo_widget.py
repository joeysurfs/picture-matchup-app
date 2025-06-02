from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image, ImageQt
from PIL.ImageOps import exif_transpose
import os
import traceback

class PhotoWidget(QWidget):
    clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(240, 240)  # Even smaller size for Pi screen
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.photo_path = None
        
        # Set up layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)  # Smaller margins
        
        # Photo display
        self.photo_label = QLabel()
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet("border: 2px solid #555555; background-color: #252525;")  # Thinner border
        layout.addWidget(self.photo_label, 1)  # 1 gives it stretch
        
        # Photo filename
        self.filename_label = QLabel()
        self.filename_label.setAlignment(Qt.AlignCenter)
        self.filename_label.setStyleSheet("font-size: 10px;")  # Smaller text
        layout.addWidget(self.filename_label)
        
        # Make clickable with stronger visual feedback for touch
        self.setStyleSheet("""
            QWidget:hover {
                background-color: #454545;
                cursor: pointer;
            }
            QWidget:pressed {
                background-color: #656565;
            }
        """)
    
    def load_photo(self, photo_path):
        """Load and display a photo with proper orientation"""
        self.photo_path = photo_path
        if not photo_path:
            self.photo_label.clear()
            self.filename_label.setText("")
            return
        
        try:
            # Open image with Pillow and fix rotation using exif_transpose
            pil_image = Image.open(photo_path)
            pil_image = exif_transpose(pil_image)
            
            # Resize to a smaller size for better performance on Raspberry Pi
            max_size = (600, 600)  # Reduced size for Raspberry Pi
            if pil_image.width > max_size[0] or pil_image.height > max_size[1]:
                pil_image.thumbnail(max_size, Image.LANCZOS)
            
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
            
            # Scale pixmap to fit label while preserving aspect ratio
            scaled_pixmap = pixmap.scaled(
                self.photo_label.width() - 10,  # Leave a small margin
                self.photo_label.height() - 10,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            self.photo_label.setPixmap(scaled_pixmap)
            
            # Truncate filename if too long for small screen
            filename = os.path.basename(photo_path)
            if len(filename) > 15:
                filename = filename[:12] + "..."
            self.filename_label.setText(filename)
        
        except Exception as e:
            print(f"Error loading image {photo_path}: {str(e)}")
            traceback.print_exc()
            self.photo_label.setText(f"Error loading image")
            self.filename_label.setText(os.path.basename(photo_path))
    
    def mousePressEvent(self, event):
        """Handle click/touch events"""
        self.setStyleSheet("""
            QWidget {
                background-color: #656565;
            }
        """)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle releasing the click/touch"""
        self.setStyleSheet("""
            QWidget {
                background-color: #353535;
            }
            QWidget:hover {
                background-color: #454545;
                cursor: pointer;
            }
        """)
        self.clicked.emit()
        super().mouseReleaseEvent(event)
    
    def resizeEvent(self, event):
        """Handle resize events by rescaling the photo"""
        if self.photo_path:
            self.load_photo(self.photo_path)
        super().resizeEvent(event)
