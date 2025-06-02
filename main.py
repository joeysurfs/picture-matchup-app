import sys
import os
from PyQt5.QtWidgets import QApplication
from gui.home_screen import HomeScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # For consistent cross-platform look
    
    # Apply dark theme
    import gui.dark_theme
    gui.dark_theme.apply_dark_theme(app)
    
    # Let the user select input folder in the home screen
    window = HomeScreen()
    window.resize(800, 600)  # Start with a reasonable window size
    window.show()  # Show in windowed mode instead of fullscreen
    
    sys.exit(app.exec_())
