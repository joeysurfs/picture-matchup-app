class BaseRating:
    """Base class for all rating systems"""
    
    def __init__(self, photo_files):
        self.photo_files = list(photo_files)
        self.name = "Base Rating System"
    
    def get_next_matchup(self):
        """Return the next pair of photos to compare (photo1, photo2)"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def update_ratings(self, winner, loser):
        """Update ratings based on a matchup result"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_current_rankings(self):
        """Return sorted list of (photo_path, score) tuples"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def is_complete(self):
        """Return True if the rating process is complete"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def estimated_matchups(self):
        """Return an estimate of the total number of matchups needed"""
        raise NotImplementedError("Subclasses must implement this method")
