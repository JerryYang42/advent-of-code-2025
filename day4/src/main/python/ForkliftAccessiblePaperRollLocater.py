from asyncio import sleep
import os
from enum import Enum
from copy import deepcopy
from typing import List

RESOURCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')

class Symbol(str, Enum):
    FORKLIFT_ACCESSIBLE_PAPER_ROLL = 'x'
    PAPER_ROLL = '@'
    SPACE = '.'


class ForkliftAccessiblePaperRollLocater:
    """Class to locate forklift-accessible paper rolls based on their IDs."""
    
    def __init__(self):
        self.map = None

    def iteratively_remove_forklift_accessible_paper_rolls(self):
        """Iteratively remove forklift-accessible paper rolls until none remain."""
        while True:
            result_map = self.locate_forklift_accessible_paper_rolls()
            n_forklift_accessible_paper_rolls = self.count_forklift_accessible_paper_rolls(result_map)
            if n_forklift_accessible_paper_rolls == 0:
                break
            self.map = result_map
            self.remove_forklift_accessible_paper_rolls(inplace=True)

    def count_paper_rolls(self):
        return sum(row.count(Symbol.PAPER_ROLL) for row in self.map) + sum(row.count(Symbol.FORKLIFT_ACCESSIBLE_PAPER_ROLL) for row in self.map)
    
    def count_forklift_accessible_paper_rolls(self, result_map):
        return sum(row.count(Symbol.FORKLIFT_ACCESSIBLE_PAPER_ROLL) for row in result_map)

    def remove_forklift_accessible_paper_rolls(self, inplace: bool = True):
        """Remove forklift-accessible paper rolls from the map."""
        rows = len(self.map)
        cols = len(self.map[0]) if rows > 0 else 0
        if inplace:
            for r in range(rows):
                for c in range(cols):
                    if self.map[r][c] == Symbol.FORKLIFT_ACCESSIBLE_PAPER_ROLL:
                        self.map[r][c] = Symbol.SPACE
                        return self.map
        else:
            new_map = deepcopy(self.map)
            for r in range(rows):
                for c in range(cols):
                    if new_map[r][c] == Symbol.FORKLIFT_ACCESSIBLE_PAPER_ROLL:
                        new_map[r][c] = Symbol.SPACE
            return new_map


    def locate_forklift_accessible_paper_rolls(self):
        """Locate forklift-accessible paper rolls in the map."""
        score_map = self._score_map(self.map)
        rows = len(self.map)
        cols = len(self.map[0]) if rows > 0 else 0
        
        answer_map = deepcopy(self.map)
        for r in range(rows):
            for c in range(cols):
                if self.map[r][c] == Symbol.PAPER_ROLL:
                    score = score_map[r][c]
                    if self._is_forklift_accessible(score):
                        answer_map[r][c] = Symbol.FORKLIFT_ACCESSIBLE_PAPER_ROLL
        return answer_map

    def _is_forklift_accessible(self, score: int) -> bool:
        """Determine if a paper roll is forklift-accessible based on its score."""
        return score < 4

    def _score_map(self, map: List[List[Symbol]]):
        """Every '@' will add one point to its 8 neighbors."""
        rows = len(map)
        cols = len(map[0]) if rows > 0 else 0
        score_map = [[0 for _ in range(cols)] for _ in range(rows)]
        
        for r in range(rows):
            for c in range(cols):
                if map[r][c] == Symbol.PAPER_ROLL:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            score_map[nr][nc] += 1
        return score_map

    
    def load_map(self, filename):
        """Load ranges from a text file."""
        filepath = os.path.join(RESOURCE_DIR, filename)
        with open(filepath, 'r') as file:
            self.map = [[Symbol(char) for char in line.strip()] for line in file.readlines()]

class Printer:
    """Class to print the map of forklift-accessible paper rolls."""
    @staticmethod
    def print_map(map: List[List[Symbol]]) -> None:
        """Print the map."""
        for row in map:
            print(''.join(symbol.value for symbol in row))

    @staticmethod
    def print_score_map(score_map: List[List[int]]) -> None:
        """Print the score map."""
        for row in score_map:
            print(''.join(str(score) for score in row))

if __name__ == "__main__":
    print("======Day 4, Sample Input=======")
    puzzle_input_sample_txt_filename = "puzzle_input_sample.txt"
    locater = ForkliftAccessiblePaperRollLocater()
    print("Original Map:")
    locater.load_map(puzzle_input_sample_txt_filename)
    Printer.print_map(locater.map)
    print()
    print("Resolver's Answer:")
    result_map = locater.locate_forklift_accessible_paper_rolls()
    Printer.print_map(result_map)
    print()
    print("Expected Answer:")
    puzzle_input_sample_answer_txt_filename = "puzzle_input_sample_answer.txt"
    locater.load_map(puzzle_input_sample_answer_txt_filename)
    Printer.print_map(locater.map)

    print("======Day 4, Part 1=======")
    puzzle_input_txt_filename = "puzzle_input.txt"
    locater.load_map(puzzle_input_txt_filename)
    result_map = locater.locate_forklift_accessible_paper_rolls()
    n_folklift_accessible_paper_rolls = sum(row.count(Symbol.FORKLIFT_ACCESSIBLE_PAPER_ROLL) for row in result_map)
    print(f"Number of forklift-accessible paper rolls: {n_folklift_accessible_paper_rolls}")

    print("======Day 4, Part 2=======")
    print("Sample results:")
    locater.load_map(puzzle_input_sample_txt_filename)
    n_paperrolls_before = locater.count_paper_rolls()
    print(f"Number of paper rolls before iterations: {n_paperrolls_before}")
    locater.iteratively_remove_forklift_accessible_paper_rolls()
    n_paperrolls_after = locater.count_paper_rolls()
    print(f"Number of paper rolls after iterations: {n_paperrolls_after}")
    print(f"Number of removed paper rolls: {n_paperrolls_before - n_paperrolls_after}")
    print("")
    print("Puzzle results:")
    locater.load_map(puzzle_input_txt_filename)
    n_paperrolls_before = locater.count_paper_rolls()
    print(f"Number of paper rolls before iterations: {n_paperrolls_before}")
    locater.iteratively_remove_forklift_accessible_paper_rolls()
    n_paperrolls_after = locater.count_paper_rolls()
    print(f"Number of paper rolls after iterations: {n_paperrolls_after}")
    print(f"Number of removed paper rolls: {n_paperrolls_before - n_paperrolls_after}")
