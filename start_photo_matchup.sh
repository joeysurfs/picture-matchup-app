#!/bin/bash
# Auto-start script for Photo Matchup App on Raspberry Pi
# Save this as /home/pi/start_photo_matchup.sh and make executable with:
# chmod +x /home/pi/start_photo_matchup.sh

# Get the directory where the script is located
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# Change to the app directory
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Install required packages
    echo "Installing required packages..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    # Activate virtual environment
    source .venv/bin/activate
fi

# Run the application
python main.py

# Deactivate the virtual environment when done
deactivate