from rating_systems.base_rating import BaseRating
import random
import math

class Glicko2Rating(BaseRating):
    """Glicko-2 rating system with rating deviation and volatility"""
    
    def __init__(self, photo_files):
        super().__init__(photo_files)
        self.name = "Glicko-2"
        
        # System constants
        self.tau = 0.5  # System volatility (smaller = less volatility)
        self.default_rd = 350  # Default rating deviation
        self.default_volatility = 0.06  # Default volatility
        
        # Initialize ratings, rating deviations (RD), and volatilities
        self.ratings = {}
        self.rds = {}
        self.volatilities = {}
        
        for photo in photo_files:
            self.ratings[photo] = 1500  # Initial rating
            self.rds[photo] = self.default_rd  # Initial RD
            self.volatilities[photo] = self.default_volatility  # Initial volatility
        
        # Track number of comparisons
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
        
        # Select photos, prioritizing those with higher RD (uncertainty)
        photos = list(self.photo_files)
        
        # Weight selection by RD
        weights = [self.rds[p] for p in photos]
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        
        # Select first photo
        photo1 = random.choices(photos, weights=weights, k=1)[0]
        
        # For second photo, select one with similar rating but high RD
        remaining = [p for p in photos if p != photo1]
        photo1_rating = self.ratings[photo1]
        
        # Calculate combined weights based on rating similarity and RD
        combined_weights = []
        for p in remaining:
            rating_diff = abs(self.ratings[p] - photo1_rating)
            # Rating similarity factor (closer = higher weight)
            similarity = 1.0 / (1 + rating_diff / 400.0)
            # RD factor (higher RD = higher weight)
            rd_factor = self.rds[p] / self.default_rd
            # Combine factors
            weight = similarity * rd_factor
            combined_weights.append(weight)
        
        # Normalize weights
        total_weight = sum(combined_weights)
        if total_weight > 0:
            combined_weights = [w / total_weight for w in combined_weights]
            photo2 = random.choices(remaining, weights=combined_weights, k=1)[0]
        else:
            photo2 = random.choice(remaining)
        
        self.current_matchup = (photo1, photo2)
        return self.current_matchup
    
    def update_ratings(self, winner, loser):
        """Update Glicko-2 ratings based on comparison result"""
        # Verify this is the current pair
        if set(self.current_matchup) != set([winner, loser]):
            return
        
        # Convert ratings and RDs to Glicko-2 scale
        winner_rating = (self.ratings[winner] - 1500) / 173.7178
        winner_rd = self.rds[winner] / 173.7178
        
        loser_rating = (self.ratings[loser] - 1500) / 173.7178
        loser_rd = self.rds[loser] / 173.7178
        
        # Compute g(RD)
        g_loser = 1 / math.sqrt(1 + 3 * loser_rd**2 / math.pi**2)
        g_winner = 1 / math.sqrt(1 + 3 * winner_rd**2 / math.pi**2)
        
        # Compute E (expected outcome)
        E_winner = 1 / (1 + math.exp(-g_loser * (winner_rating - loser_rating)))
        E_loser = 1 / (1 + math.exp(-g_winner * (loser_rating - winner_rating)))
        
        # Compute v (variance)
        v_winner = 1 / (g_loser**2 * E_winner * (1 - E_winner))
        v_loser = 1 / (g_winner**2 * E_loser * (1 - E_loser))
        
        # Compute delta (expected rating change)
        delta_winner = v_winner * g_loser * (1 - E_winner)
        delta_loser = v_loser * g_winner * (0 - E_loser)
        
        # Update volatilities
        self.volatilities[winner] = self._update_volatility(
            winner_rating, winner_rd, delta_winner, v_winner, self.volatilities[winner]
        )
        self.volatilities[loser] = self._update_volatility(
            loser_rating, loser_rd, delta_loser, v_loser, self.volatilities[loser]
        )
        
        # Update RDs
        new_rd_winner = math.sqrt(winner_rd**2 + self.volatilities[winner]**2)
        new_rd_loser = math.sqrt(loser_rd**2 + self.volatilities[loser]**2)
        
        self.rds[winner] = 1 / math.sqrt(1/new_rd_winner**2 + 1/v_winner) * 173.7178
        self.rds[loser] = 1 / math.sqrt(1/new_rd_loser**2 + 1/v_loser) * 173.7178
        
        # Ensure RDs don't go below a minimum threshold
        min_rd = 30
        self.rds[winner] = max(self.rds[winner], min_rd)
        self.rds[loser] = max(self.rds[loser], min_rd)
        
        # Update ratings
        self.ratings[winner] += g_loser * (1 - E_winner) * new_rd_winner**2 * 173.7178
        self.ratings[loser] += g_winner * (0 - E_loser) * new_rd_loser**2 * 173.7178
        
        # Update comparison counts
        self.comparisons[winner] += 1
        self.comparisons[loser] += 1
        self.completed_matches += 1
        
        # Reset current matchup
        self.current_matchup = None
    
    def _update_volatility(self, rating, rd, delta, v, sigma):
        """Update volatility using iterative algorithm"""
        # Simplified volatility update
        # In a full implementation, this would use the iterative algorithm
        # from the Glicko-2 paper, but we use a simpler approach here
        delta_sq = delta**2
        rd_sq = rd**2
        
        # If the outcome was expected (delta is small), reduce volatility
        # If the outcome was unexpected (delta is large), increase volatility
        if delta_sq > rd_sq + v:
            # Unexpected result - increase volatility
            return min(sigma * 1.1, 0.1)
        else:
            # Expected result - decrease volatility slightly
            return max(sigma * 0.9, 0.05)
    
    def get_current_rankings(self):
        """Return sorted list of (photo_path, score) tuples"""
        # Convert ratings to confidence-adjusted scores
        # Lower RD means more confidence in the rating
        scores = []
        for photo in self.photo_files:
            # Confidence factor: reduces score if RD is high
            confidence = 1 - (self.rds[photo] / (self.default_rd * 2))
            confidence = max(0.5, min(1.0, confidence))
            
            # Adjusted score combines rating and confidence
            adjusted_score = self.ratings[photo] * confidence
            scores.append((photo, adjusted_score))
        
        return sorted(scores, key=lambda x: x[1], reverse=True)
    
    def is_complete(self):
        """Return True if all scheduled matches have been completed"""
        return self.completed_matches >= self.total_matches
    
    def estimated_matchups(self):
        """Return total number of matchups"""
        return self.total_matches
