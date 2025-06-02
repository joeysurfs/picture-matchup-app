from rating_systems.base_rating import BaseRating
import random

class QuickSortRating(BaseRating):
    """Rating system using quicksort algorithm for efficiency"""
    
    def __init__(self, photo_files):
        super().__init__(photo_files)
        self.name = "Quick Sort"
        
        # Initialize data structures
        self.photos_to_sort = list(photo_files)
        random.shuffle(self.photos_to_sort)  # Randomize order initially
        
        # Stacks for quicksort-like algorithm
        self.stack = []
        if len(self.photos_to_sort) > 1:
            self.stack.append((0, len(self.photos_to_sort) - 1))
        
        # Current comparison state
        self.current_partition = None
        self.current_pivot = None
        self.current_i = None
        self.current_j = None
        
        # For estimating total matchups
        self.n = len(photo_files)
        self.est_matchups = int(self.n * (self.n.bit_length() - 1)) if self.n > 1 else 0
        self.completed_sorts = 0
    
    def get_next_matchup(self):
        """Return the next pair of photos to compare"""
        # If we're in the middle of partitioning
        if self.current_partition is not None:
            left, right = self.current_partition
            pivot_photo = self.photos_to_sort[self.current_pivot]
            compare_photo = self.photos_to_sort[self.current_j]
            return pivot_photo, compare_photo
        
        # Otherwise, start a new partition
        if self.stack:
            left, right = self.stack.pop()
            self.current_partition = (left, right)
            self.current_pivot = left
            self.current_i = left
            self.current_j = left + 1
            
            pivot_photo = self.photos_to_sort[self.current_pivot]
            
            if self.current_j <= right:
                compare_photo = self.photos_to_sort[self.current_j]
                return pivot_photo, compare_photo
        
        # This shouldn't happen unless is_complete() is not checked properly
        return None, None
    
    def update_ratings(self, winner, loser):
        """Update based on comparison result"""
        if self.current_partition is None:
            return
        
        left, right = self.current_partition
        pivot_photo = self.photos_to_sort[self.current_pivot]
        
        # If pivot wins, keep the order
        if winner == pivot_photo:
            pass  # No swap needed
        # If comparing photo wins, swap with the next position after i
        else:
            self.current_i += 1
            self.photos_to_sort[self.current_i], self.photos_to_sort[self.current_j] = \
                self.photos_to_sort[self.current_j], self.photos_to_sort[self.current_i]
        
        # Move to next comparison
        self.current_j += 1
        
        # If we've reached the end of this partition
        if self.current_j > right:
            # Swap pivot into its final position
            self.photos_to_sort[left], self.photos_to_sort[self.current_i] = \
                self.photos_to_sort[self.current_i], self.photos_to_sort[left]
            
            # Add sub-partitions to stack if they have more than one element
            if left < self.current_i - 1:
                self.stack.append((left, self.current_i - 1))
            if self.current_i + 1 < right:
                self.stack.append((self.current_i + 1, right))
            
            # Reset current partition
            self.current_partition = None
    
    def get_current_rankings(self):
        """Return sorted list of (photo_path, score) tuples"""
        # In QuickSort, the score is just the position (higher position = higher rank)
        n = len(self.photos_to_sort)
        return [(photo, n - i) for i, photo in enumerate(self.photos_to_sort)]
    
    def is_complete(self):
        """Return True if the rating process is complete"""
        return not self.stack and self.current_partition is None
    
    def estimated_matchups(self):
        """Return an estimate of the total number of matchups needed"""
        return self.est_matchups
