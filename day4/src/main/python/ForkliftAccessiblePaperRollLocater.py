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
        self.board = None

    def iteratively_remove_forklift_accessible_paper_rolls(self):
        """Iteratively remove forklift-accessible paper rolls until none remain."""
        while True:
            result_board = self.locate_forklift_accessible_paper_rolls()
            n_forklift_accessible_paper_rolls = self.count_forklift_accessible_paper_rolls(result_board)
            if n_forklift_accessible_paper_rolls == 0:
                break
            self.board = result_board
            self.remove_forklift_accessible_paper_rolls(inplace=True)

    def count_paper_rolls(self):
        return sum(row.count(Symbol.PAPER_ROLL) for row in self.board) + sum(row.count(Symbol.FORKLIFT_ACCESSIBLE_PAPER_ROLL) for row in self.board)
    
    def count_forklift_accessible_paper_rolls(self, result_board):
        return sum(row.count(Symbol.FORKLIFT_ACCESSIBLE_PAPER_ROLL) for row in result_board)

    def remove_forklift_accessible_paper_rolls(self, inplace: bool = True):
        """Remove forklift-accessible paper rolls from the board."""
        rows = len(self.board)
        cols = len(self.board[0]) if rows > 0 else 0
        if inplace:
            for r in range(rows):
                for c in range(cols):
                    if self.board[r][c] == Symbol.FORKLIFT_ACCESSIBLE_PAPER_ROLL:
                        self.board[r][c] = Symbol.SPACE
                        return self.board
        else:
            new_board = deepcopy(self.board)
            for r in range(rows):
                for c in range(cols):
                    if new_board[r][c] == Symbol.FORKLIFT_ACCESSIBLE_PAPER_ROLL:
                        new_board[r][c] = Symbol.SPACE
            return new_board

    def locate_forklift_accessible_paper_rolls(self):
        """Locate forklift-accessible paper rolls in the board."""
        score_board = self._score_board(self.board)
        rows = len(self.board)
        cols = len(self.board[0]) if rows > 0 else 0
        
        answer_board = deepcopy(self.board)
        for r in range(rows):
            for c in range(cols):
                if self.board[r][c] == Symbol.PAPER_ROLL:
                    score = score_board[r][c]
                    if self._is_forklift_accessible(score):
                        answer_board[r][c] = Symbol.FORKLIFT_ACCESSIBLE_PAPER_ROLL
        return answer_board

    def _is_forklift_accessible(self, score: int) -> bool:
        """Determine if a paper roll is forklift-accessible based on its score."""
        return score < 4

    def _score_board(self, board: List[List[Symbol]]):
        """Every '@' will add one point to its 8 neighbors."""
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        score_board = [[0 for _ in range(cols)] for _ in range(rows)]
        
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == Symbol.PAPER_ROLL:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            score_board[nr][nc] += 1
        return score_board

    
    def load_board(self, filename):
        """Load ranges from a text file."""
        filepath = os.path.join(RESOURCE_DIR, filename)
        with open(filepath, 'r') as file:
            self.board = [[Symbol(char) for char in line.strip()] for line in file.readlines()]

class Printer:
    """Class to print the map of forklift-accessible paper rolls."""
    @staticmethod
    def print_board(board: List[List[Symbol]]) -> None:
        """Print the board."""
        for row in board:
            print(''.join(symbol.value for symbol in row))

    @staticmethod
    def print_score_board(score_board: List[List[int]]) -> None:
        """Print the score board."""
        for row in score_board:
            print(''.join(str(score) for score in row))

if __name__ == "__main__":
    print("======Day 4, Sample Input=======")
    puzzle_input_sample_txt_filename = "puzzle_input_sample.txt"
    locater = ForkliftAccessiblePaperRollLocater()
    print("Original Board:")
    locater.load_board(puzzle_input_sample_txt_filename)
    Printer.print_board(locater.board)
    print()
    print("Resolver's Answer:")
    result_board = locater.locate_forklift_accessible_paper_rolls()
    Printer.print_board(result_board)
    print()
    print("Expected Answer:")
    puzzle_input_sample_answer_txt_filename = "puzzle_input_sample_answer.txt"
    locater.load_board(puzzle_input_sample_answer_txt_filename)
    Printer.print_board(locater.board)

    print("======Day 4, Part 1=======")
    puzzle_input_txt_filename = "puzzle_input.txt"
    locater.load_board(puzzle_input_txt_filename)
    result_board = locater.locate_forklift_accessible_paper_rolls()
    n_folklift_accessible_paper_rolls = sum(row.count(Symbol.FORKLIFT_ACCESSIBLE_PAPER_ROLL) for row in result_board)
    print(f"Number of forklift-accessible paper rolls: {n_folklift_accessible_paper_rolls}")

    print("======Day 4, Part 2=======")
    print("Sample results:")
    locater.load_board(puzzle_input_sample_txt_filename)
    n_paperrolls_before = locater.count_paper_rolls()
    print(f"Number of paper rolls before iterations: {n_paperrolls_before}")
    locater.iteratively_remove_forklift_accessible_paper_rolls()
    n_paperrolls_after = locater.count_paper_rolls()
    print(f"Number of paper rolls after iterations: {n_paperrolls_after}")
    print(f"Number of removed paper rolls: {n_paperrolls_before - n_paperrolls_after}")
    print("")
    print("Puzzle results:")
    locater.load_board(puzzle_input_txt_filename)
    n_paperrolls_before = locater.count_paper_rolls()
    print(f"Number of paper rolls before iterations: {n_paperrolls_before}")
    locater.iteratively_remove_forklift_accessible_paper_rolls()
    n_paperrolls_after = locater.count_paper_rolls()
    print(f"Number of paper rolls after iterations: {n_paperrolls_after}")
    print(f"Number of removed paper rolls: {n_paperrolls_before - n_paperrolls_after}")
