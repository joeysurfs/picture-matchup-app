from rating_systems.base_rating import BaseRating
import random
import math

class EloRating(BaseRating):
    """Elo rating system adapted from chess rankings"""
    
    def __init__(self, photo_files):
        super().__init__(photo_files)
        self.name = "Elo"
        
        # Initialize all photos with base Elo of 1400
        self.ratings = {photo: 1400 for photo in photo_files}
        
        # Parameter K determines how much ratings change after each comparison
        self.K = 32
        
        # Track number of comparisons for each photo
        self.comparisons = {photo: 0 for photo in photo_files}
        
        # Total matches to perform (approximately 6 per photo)
        self.total_matches = len(photo_files) * 6
        self.completed_matches = 0
        
        # Current matchup
        self.current_matchup = None
    
    def get_next_matchup(self):
        """Return the next pair of photos to compare"""
        if self.completed_matches >= self.total_matches:
            return None, None
        
        # Select photos, prioritizing those with fewer comparisons
        photos = list(self.photo_files)
        
        # Weight selection by inverse of comparison count
        weights = [1.0 / (1 + self.comparisons[p]) for p in photos]
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        
        # Select first photo
        photo1 = random.choices(photos, weights=weights, k=1)[0]
        
        # For second photo, select one with similar rating
        # This makes comparisons more informative
        remaining = [p for p in photos if p != photo1]
        photo1_rating = self.ratings[photo1]
        
        # Calculate "similarity" scores (closer ratings = higher score)
        similarities = []
        for p in remaining:
            rating_diff = abs(self.ratings[p] - photo1_rating)
            # Sigmoid-like function: photos with similar ratings get higher weights
            similarity = 1.0 / (1 + rating_diff / 400.0)
            similarities.append(similarity)
        
        # Normalize similarities
        total_sim = sum(similarities)
        if total_sim > 0:
            similarities = [s / total_sim for s in similarities]
            photo2 = random.choices(remaining, weights=similarities, k=1)[0]
        else:
            photo2 = random.choice(remaining)
        
        self.current_matchup = (photo1, photo2)
        return self.current_matchup
    
    def update_ratings(self, winner, loser):
        """Update Elo ratings based on comparison result"""
        # Verify this is the current pair
        if set(self.current_matchup) != set([winner, loser]):
            return
        
        # Get current ratings
        rating_winner = self.ratings[winner]
        rating_loser = self.ratings[loser]
        
        # Calculate expected scores
        expected_winner = 1.0 / (1 + 10 ** ((rating_loser - rating_winner) / 400.0))
        expected_loser = 1.0 / (1 + 10 ** ((rating_winner - rating_loser) / 400.0))
        
        # Update ratings
        self.ratings[winner] += self.K * (1 - expected_winner)
        self.ratings[loser] += self.K * (0 - expected_loser)
        
        # Update comparison counts
        self.comparisons[winner] += 1
        self.comparisons[loser] += 1
        
        # Mark match as completed
        self.completed_matches += 1
        self.current_matchup = None
    
    def get_current_rankings(self):
        """Return sorted list of (photo_path, score) tuples"""
        return sorted(self.ratings.items(), key=lambda x: x[1], reverse=True)
    
    def is_complete(self):
        """Return True if all matches have been completed"""
        return self.completed_matches >= self.total_matches
    
    def estimated_matchups(self):
        """Return total number of matchups"""
        return self.total_matches
