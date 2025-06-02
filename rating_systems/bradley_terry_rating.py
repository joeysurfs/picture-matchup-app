from rating_systems.base_rating import BaseRating
import random
import math
import numpy as np
from collections import defaultdict

class BradleyTerryRating(BaseRating):
    """Bradley-Terry model for pairwise comparisons"""
    
    def __init__(self, photo_files):
        super().__init__(photo_files)
        self.name = "Bradley-Terry"
        
        # Maps photo paths to indices
        self.photo_to_index = {photo: i for i, photo in enumerate(photo_files)}
        self.index_to_photo = {i: photo for i, photo in enumerate(photo_files)}
        
        # Number of photos
        self.n = len(photo_files)
        
        # Wins matrix: wins[i][j] = number of times i beat j
        self.wins = np.zeros((self.n, self.n))
        
        # Initialize strengths (log-skills)
        self.strengths = np.zeros(self.n)
        
        # Initialize comparison counts
        self.total_comparisons = 0
        self.target_comparisons = self.n * 10  # ~10 comparisons per photo
        
        # Track which photos have been compared
        self.comparisons = defaultdict(int)
        
        # Current matchup
        self.current_matchup = None
    
    def get_next_matchup(self):
        """Return the next pair of photos to compare"""
        if self.total_comparisons >= self.target_comparisons:
            return None, None
            
        # Get photos with fewest comparisons first
        photos = sorted(self.photo_files, 
                      key=lambda p: self.comparisons[p])
        
        # Select first photo from least compared third
        first_third = max(1, len(photos) // 3)
        photo1 = random.choice(photos[:first_third])
        
        # Select second photo that hasn't been compared with photo1 many times
        remaining = [p for p in photos if p != photo1]
        
        idx1 = self.photo_to_index[photo1]
        remaining_weights = []
        
        for p in remaining:
            idx2 = self.photo_to_index[p]
            # Lower weight if they've been compared more times
            comparison_count = self.wins[idx1, idx2] + self.wins[idx2, idx1]
            # Sigmoid-like scale: more comparisons = lower weight
            weight = 1.0 / (1.0 + comparison_count)
            remaining_weights.append(weight)
        
        # Normalize weights
        total = sum(remaining_weights)
        if total > 0:
            remaining_weights = [w/total for w in remaining_weights]
            photo2 = random.choices(remaining, weights=remaining_weights, k=1)[0]
        else:
            photo2 = random.choice(remaining)
        
        self.current_matchup = (photo1, photo2)
        return self.current_matchup
    
    def update_ratings(self, winner, loser):
        """Update ratings based on comparison result"""
        # Verify this is the current pair
        if set(self.current_matchup) != set([winner, loser]):
            return
        
        # Get indices
        winner_idx = self.photo_to_index[winner]
        loser_idx = self.photo_to_index[loser]
        
        # Update wins matrix
        self.wins[winner_idx, loser_idx] += 1
        
        # Update comparison counts
        self.comparisons[winner] += 1
        self.comparisons[loser] += 1
        self.total_comparisons += 1
        
        # Re-estimate strengths using MM algorithm
        self._update_strengths()
        
        self.current_matchup = None
    
    def _update_strengths(self):
        """Update strength parameters using Minorization-Maximization algorithm"""
        # Skip if not enough data yet
        if self.total_comparisons < self.n:
            return
            
        # Perform 5 iterations of MM algorithm
        for _ in range(5):
            # Calculate total wins for each photo
            w_i = np.sum(self.wins, axis=1)
            
            # Calculate expected number of wins given current strengths
            p = np.exp(self.strengths)
            p_sum = np.sum(p)
            
            # Calculate new strengths
            new_strengths = np.zeros(self.n)
            for i in range(self.n):
                if w_i[i] > 0:  # Only update if the photo has won at least once
                    new_strengths[i] = math.log(w_i[i]) - math.log(p_sum - p[i])
            
            # Update strengths (with regularization to prevent divergence)
            self.strengths = 0.9 * self.strengths + 0.1 * new_strengths
    
    def get_current_rankings(self):
        """Return sorted list of (photo_path, score) tuples"""
        # Convert strengths to photo paths and scores
        scores = []
        for i, strength in enumerate(self.strengths):
            photo = self.index_to_photo[i]
            # Convert to probability scale (0-100) for more intuitive scores
            score = 100 * np.exp(strength) / (1 + np.exp(strength))
            scores.append((photo, score))
        
        return sorted(scores, key=lambda x: x[1], reverse=True)
    
    def is_complete(self):
        """Return True if all scheduled comparisons have been made"""
        return self.total_comparisons >= self.target_comparisons
    
    def estimated_matchups(self):
        """Return total number of matchups"""
        return self.target_comparisons
