from rating_systems.base_rating import BaseRating
import random
from collections import defaultdict

class SimpleRating(BaseRating):
    """Simple rating system based on win/loss counts"""
    
    def __init__(self, photo_files):
        super().__init__(photo_files)
        self.name = "Simple"
        
        # Initialize scores for each photo
        self.scores = {photo: 0 for photo in photo_files}
        
        # Track comparisons to avoid duplicates
        self.comparisons = set()
        
        # Pairs waiting to be compared
        self.remaining_pairs = []
        self.generate_all_pairs()
        
        # Estimated total comparisons
        self.total_comparisons = len(self.remaining_pairs)
    
    def generate_all_pairs(self):
        """Generate all possible photo pairs for comparison"""
        photo_list = list(self.photo_files)
        for i in range(len(photo_list)):
            for j in range(i + 1, len(photo_list)):
                self.remaining_pairs.append((photo_list[i], photo_list[j]))
        
        # Shuffle to randomize comparison order
        random.shuffle(self.remaining_pairs)
    
    def get_next_matchup(self):
        """Return the next pair of photos to compare"""
        if not self.remaining_pairs:
            return None, None
        
        return self.remaining_pairs[0]
    
    def update_ratings(self, winner, loser):
        """Update ratings based on comparison result"""
        # Verify this is the current pair
        current_pair = self.remaining_pairs[0]
        if set(current_pair) == set([winner, loser]):
            # Update scores
            self.scores[winner] += 1
            
            # Mark comparison as done
            self.comparisons.add(tuple(sorted((winner, loser))))
            self.remaining_pairs.pop(0)
    
    def get_current_rankings(self):
        """Return sorted list of (photo_path, score) tuples"""
        return sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
    
    def is_complete(self):
        """Return True if all comparisons have been made"""
        return len(self.remaining_pairs) == 0
    
    def estimated_matchups(self):
        """Return total number of matchups"""
        return self.total_comparisons
