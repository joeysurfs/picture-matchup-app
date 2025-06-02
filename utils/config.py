import os
import json

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".photo_matchup_config.json")

def load_config():
    """Load configuration from file"""
    config = {
        "last_folder": None
    }
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                loaded_config = json.load(f)
                config.update(loaded_config)
        except Exception as e:
            print(f"Error loading config: {e}")
    
    return config

def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Error saving config: {e}")
