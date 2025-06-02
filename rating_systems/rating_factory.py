from rating_systems.quicksort_rating import QuickSortRating
from rating_systems.simple_rating import SimpleRating
from rating_systems.elo_rating import EloRating
from rating_systems.bradley_terry_rating import BradleyTerryRating
from rating_systems.glicko2_rating import Glicko2Rating
from rating_systems.trueskill_rating import TrueSkillRating

class RatingFactory:
    @staticmethod
    def create_rating_system(system_name, photo_files):
        """Create the appropriate rating system based on name"""
        if system_name == "Quick Sort":
            return QuickSortRating(photo_files)
        elif system_name == "Simple":
            return SimpleRating(photo_files)
        elif system_name == "Elo":
            return EloRating(photo_files)
        elif system_name == "Bradley-Terry":
            return BradleyTerryRating(photo_files)
        elif system_name == "Glicko-2":
            return Glicko2Rating(photo_files)
        elif system_name == "TrueSkill":
            return TrueSkillRating(photo_files)
        else:
            # Default to Quick Sort if unknown
            return QuickSortRating(photo_files)
