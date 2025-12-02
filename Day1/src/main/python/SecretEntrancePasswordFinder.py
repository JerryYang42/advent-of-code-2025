import os
from typing import List

N_GRADUATIONS = 100
DIAL_STARTING_POSITION = 50
DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')
INPUT_P1_FILENAME = 'input_p1.txt'

# Part 1 Solution
class SecretEntrancePasswordFinder:
    """Class to find the secret entrance password based on cumulative summation."""
    
    def __init__(self, n_graduations: int, dial_starting_position: int, instruction_input_filename: str):
        self.n_graduations = n_graduations
        self.dial_starting_position = dial_starting_position
        self.instruction_input_filename = instruction_input_filename
        self.instruction_input_filepath = os.path.join(DATA_FOLDER, instruction_input_filename)
        self.instructions = self._load_instructions()
    
    def resolve_password(self) -> int:
        """Find the occurrences of zero position equivalent in the cumulative summation of shifts."""
        self.shifts = [self._parse_instruction(instr) for instr in self.instructions]
        self.cumulative_sums = self._cumulative_sum(self.shifts, self.dial_starting_position)
        return self._count_zero_position_equivalence(self.cumulative_sums)

    def _load_instructions(self) -> List[str]:
        """Load instructions from the input file."""
        def _is_valid_instruction(instruction: str) -> bool:
            return (instruction and 
                    instruction[0] in ('R', 'L') and 
                    instruction[1:].isdigit())
        
        with open(self.instruction_input_filepath, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            for line_num, line in enumerate(lines, start=1):
                if not _is_valid_instruction(line):
                    raise ValueError("Invalid instruction found on line {}: {}".format(line_num, line))
            return lines

    def _parse_instruction(self, instruction: str) -> int:
            """Map the instructions to shifts as signed integers, where R is positive and L is negative."""
            direction = 1 if instruction[0] == 'R' else -1
            magnitude = int(instruction[1:])
            return direction * magnitude
        
    def _cumulative_sum(self, shifts: List[int], starting_position: int = 0) -> List[int]:
        """Compute the cumulative sum of shifts starting from a given position."""  
        cumulative_sums = []
        current_sum = starting_position
        for shift in shifts:
            current_sum += shift
            cumulative_sums.append(current_sum)
        return cumulative_sums

    def _count_zero_position_equivalence(self, cumulative_summation: List[int]) -> int:
        """Count how many values in the cumulative summation are divisible by n_graduations."""
        
        def _is_divisible_by_n_graduations(position: int) -> bool:
            """zero position equivalent means divisible by n_graduations"""
            return position % self.n_graduations == 0
        
        count = sum(1 for x in cumulative_summation if _is_divisible_by_n_graduations(x))
        return count


if __name__ == "__main__":
    print("======Day 1, Part 1======")
    part_1_answer = SecretEntrancePasswordFinder(N_GRADUATIONS, DIAL_STARTING_POSITION, INPUT_P1_FILENAME).resolve_password()
    print("Answer: ", part_1_answer)
    print("")
    print("======Day 1, Part 2======")
    print("Not yet implemented")
