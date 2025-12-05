import os
from enum import Enum
from copy import deepcopy
from typing import List, Set, Tuple

RESOURCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')

class FreshIngredientDatabase:
    """Class to manage fresh food database.
    The data is given as a list of ID ranges. Each range is represented as a tuple (start_id, end_id).
    Every id falls into that range is considered fresh food ID.
    """

    def __init__(self):
        self.fresh_ingredient_id_ranges: List[Tuple[int, int]] = []
        self.available_ingredient_ids: Set[int] = set()

    def load_data_from_file(self, file_path: str):
        """Load fresh ingredient ID ranges from a file."""
        with open(file_path, 'r') as f:
            while True:
                line = f.readline()
                if line == '\n' or not line:
                    break
                start_id, end_id = map(int, line.strip().split('-'))
                self.fresh_ingredient_id_ranges.append((start_id, end_id))

            self._preprocess_fresh_ingredient_id_ranges()
            
            lines = f.readlines()
            for line in lines:
                self.available_ingredient_ids.add(int(line.strip()))

    def count_all_theoretically_fresh_ingredients(self) -> int:
        """Count all theoretically fresh ingredient IDs based on the ID ranges."""
        total_count = 0
        for start_id, end_id in self.fresh_ingredient_id_ranges:
            total_count += (end_id - start_id + 1)
        return total_count


    def _preprocess_fresh_ingredient_id_ranges(self):
        """Preprocess the fresh ingredient ID ranges to merge overlapping ranges."""
        if not self.fresh_ingredient_id_ranges:
            return
        
        # Sort ranges by start_id
        self.fresh_ingredient_id_ranges.sort(key=lambda x: x[0])
        
        merged_ranges = []
        current_start, current_end = self.fresh_ingredient_id_ranges[0]
        
        for start, end in self.fresh_ingredient_id_ranges[1:]:
            if start <= current_end + 1:  # Overlapping or contiguous ranges
                current_end = max(current_end, end)
            else:
                merged_ranges.append((current_start, current_end))
                current_start, current_end = start, end
        
        merged_ranges.append((current_start, current_end))
        self.fresh_ingredient_id_ranges = merged_ranges


class FreshIngredientIdChecker:
    """Class to check fresh ingredient IDs based on """

    def __init__(self, fresh_ingredient_db: FreshIngredientDatabase):
        self.fresh_ingredient_db = fresh_ingredient_db

    def is_fresh_ingredient(self, ingredient_id: int) -> bool:
        """Check if the given ingredient ID is fresh."""
        for start_id, end_id in self.fresh_ingredient_db.fresh_ingredient_id_ranges:
            if start_id <= ingredient_id <= end_id:
                return True
        return False
    
    def available_fresh_ingredient_ids(self) -> Set[int]:
        """Get the set of available fresh ingredient IDs."""
        fresh_ids = set()
        for ingredient_id in self.fresh_ingredient_db.available_ingredient_ids:
            if self.is_fresh_ingredient(ingredient_id):
                fresh_ids.add(ingredient_id)
        return fresh_ids
    


if __name__ == "__main__":
    print("======Day 5, Part 1=======")
    print("Sample Input:")
    fresh_ingredients_filename = "puzzle_input_sample.txt"
    fresh_ingredient_db = FreshIngredientDatabase()
    fresh_ingredient_db.load_data_from_file(os.path.join(RESOURCE_DIR, fresh_ingredients_filename))    
    print("Fresh Ingredient ID Ranges:", fresh_ingredient_db.fresh_ingredient_id_ranges)
    print("Available Ingredient IDs:", fresh_ingredient_db.available_ingredient_ids)
    print("Sample Answer:")
    fresh_ingredient_id_checker = FreshIngredientIdChecker(fresh_ingredient_db)
    available_fresh_ingredient_ids = fresh_ingredient_id_checker.available_fresh_ingredient_ids()
    print("Number of Fresh Ingredients:", len(available_fresh_ingredient_ids))
    print()
    print("Puzzle Answer:")
    puzzle_input_filename = "puzzle_input.txt"
    fresh_ingredient_db = FreshIngredientDatabase()
    fresh_ingredient_db.load_data_from_file(os.path.join(RESOURCE_DIR, puzzle_input_filename))
    fresh_ingredient_id_checker = FreshIngredientIdChecker(fresh_ingredient_db)
    available_fresh_ingredient_ids = fresh_ingredient_id_checker.available_fresh_ingredient_ids()
    print("Number of Fresh Ingredients:", len(available_fresh_ingredient_ids))
    
    print("======Day 5, Part 2=======")
    print("Sample Input:")
    fresh_ingredients_filename = "puzzle_input_sample.txt"
    fresh_ingredient_db = FreshIngredientDatabase()
    fresh_ingredient_db.load_data_from_file(os.path.join(RESOURCE_DIR, fresh_ingredients_filename))    
    print("Fresh Ingredient ID Ranges:", fresh_ingredient_db.fresh_ingredient_id_ranges)
    print("Sample Answer:")
    print("Number of Theoretically Fresh Ingredients:", fresh_ingredient_db.count_all_theoretically_fresh_ingredients())
    print("Puzzle Answer:")
    puzzle_input_filename = "puzzle_input.txt"
    fresh_ingredient_db = FreshIngredientDatabase()
    fresh_ingredient_db.load_data_from_file(os.path.join(RESOURCE_DIR, puzzle_input_filename))
    print("Number of Theoretically Fresh Ingredients:", fresh_ingredient_db.count_all_theoretically_fresh_ingredients())
