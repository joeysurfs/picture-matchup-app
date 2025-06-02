from rating_systems.base_rating import BaseRating
import random
import math
from collections import defaultdict

class TrueSkillRating(BaseRating):
    """Microsoft's TrueSkill rating system"""
    
    def __init__(self, photo_files):
        super().__init__(photo_files)
        self.name = "TrueSkill"
        
        # TrueSkill parameters
        self.beta = 25.0 / 6  # Skill width (standard deviation of performance)
        self.tau = 25.0 / 300  # Dynamic factor (additive dynamics variance per comparison)
        self.draw_probability = 0.0  # No draws in our application
        
        # Initialize skills and uncertainties
        self.mu = {photo: 25.0 for photo in photo_files}  # Mean skill
        self.sigma = {photo: 25.0 / 3 for photo in photo_files}  # Skill uncertainty
        
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
        
        # Select photos based on uncertainty and expected information gain
        photos = list(self.photo_files)
        
        # Weight selection by uncertainty (sigma)
        weights = [self.sigma[p] for p in photos]
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        
        # Select first photo based on uncertainty
        photo1 = random.choices(photos, weights=weights, k=1)[0]
        
        # For second photo, select one that would give most information
        remaining = [p for p in photos if p != photo1]
        
        # Calculate expected information gain for each potential opponent
        info_gains = []
        mu1 = self.mu[photo1]
        sigma1 = self.sigma[photo1]
        
        for p in remaining:
            mu2 = self.mu[p]
            sigma2 = self.sigma[p]
            
            # Calculate draw margin
            draw_margin = self.beta * math.sqrt(2)
            
            # Calculate expected information gain
            # Higher when skills are close and uncertainties are high
            skill_diff = abs(mu1 - mu2)
            total_uncertainty = math.sqrt(sigma1**2 + sigma2**2 + 2 * self.beta**2)
            
            # More information when skills are similar and uncertainties are high
            if total_uncertainty > 0:
                info_gain = (1 - skill_diff / (3 * total_uncertainty)) * total_uncertainty
                info_gain = max(0.1, info_gain)  # Ensure all have some chance
            else:
                info_gain = 0.1
                
            info_gains.append(info_gain)
        
        # Normalize weights
        total_gain = sum(info_gains)
        if total_gain > 0:
            info_gains = [g / total_gain for g in info_gains]
            photo2 = random.choices(remaining, weights=info_gains, k=1)[0]
        else:
            photo2 = random.choice(remaining)
        
        self.current_matchup = (photo1, photo2)
        return self.current_matchup
    
    def update_ratings(self, winner, loser):
        """Update TrueSkill ratings based on comparison result"""
        # Verify this is the current pair
        if set(self.current_matchup) != set([winner, loser]):
            return
            
        # Get current skills
        mu_winner = self.mu[winner]
        sigma_winner = self.sigma[winner]
        
        mu_loser = self.mu[loser]
        sigma_loser = self.sigma[loser]
        
        # Calculate variance of the sum of the two skills
        c = math.sqrt(2 * self.beta**2 + sigma_winner**2 + sigma_loser**2)
        
        # Calculate the mean of performance difference
        mean_diff = mu_winner - mu_loser
        
        # Calculate v and w for the update equations
        v = self._v(mean_diff / c)
        w = v * (v + mean_diff / c)
        
        # Update winner's skill and uncertainty
        mu_winner_new = mu_winner + (sigma_winner**2 / c) * v
        sigma_winner_new = sigma_winner * math.sqrt(1 - (sigma_winner**2 / c**2) * w)
        
        # Update loser's skill and uncertainty
        mu_loser_new = mu_loser - (sigma_loser**2 / c) * v
        sigma_loser_new = sigma_loser * math.sqrt(1 - (sigma_loser**2 / c**2) * w)
        
        # Add dynamic factor (tau) to increase uncertainty over time
        sigma_winner_new = math.sqrt(sigma_winner_new**2 + self.tau**2)
        sigma_loser_new = math.sqrt(sigma_loser_new**2 + self.tau**2)
        
        # Store updated values
        self.mu[winner] = mu_winner_new
        self.sigma[winner] = sigma_winner_new
        
        self.mu[loser] = mu_loser_new
        self.sigma[loser] = sigma_loser_new
        
        # Update comparison counts
        self.comparisons[winner] += 1
        self.comparisons[loser] += 1
        self.completed_matches += 1
        
        # Reset current matchup
        self.current_matchup = None
    
    def _v(self, x):
        """Helper function for TrueSkill updates"""
        sqrt2pi = math.sqrt(2 * math.pi)
        return self._pdf(x) / self._cdf(x)
    
    def _pdf(self, x):
        """Probability density function for normal distribution"""
        return math.exp(-(x*x)/2) / math.sqrt(2 * math.pi)
    
    def _cdf(self, x):
        """Cumulative distribution function for normal distribution"""
        return (1.0 + math.erf(x / math.sqrt(2))) / 2.0
    
    def get_current_rankings(self):
        """Return sorted list of (photo_path, score) tuples"""
        # Calculate conservative skill estimate: mu - 3*sigma
        scores = []
        for photo in self.photo_files:
            # Use conservative skill estimate (mu - sigma) as score
            # This balances exploration and exploitation
            conservative_skill = self.mu[photo] - self.sigma[photo]
            scores.append((photo, conservative_skill))
        
        return sorted(scores, key=lambda x: x[1], reverse=True)
    
    def is_complete(self):
        """Return True if all scheduled matches have been completed"""
        return self.completed_matches >= self.total_matches
    
    def estimated_matchups(self):
        """Return total number of matchups"""
        return self.total_matches
