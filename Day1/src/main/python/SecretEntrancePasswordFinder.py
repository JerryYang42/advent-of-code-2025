import os
from typing import List

N_GRADUATIONS = 100
DIAL_STARTING_POSITION = 50
DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')
INPUT_P1_FILENAME = 'input_p1.txt'
INPUT_P2_FILENAME = 'input_p1.txt'

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

    def resolve_password_par2_2(self) -> int:
        """Find the occurrences of zero position equivalent in the cumulative summation of shifts and during the dial rotation."""
        self.shifts = [self._parse_instruction(instr) for instr in self.instructions]
        self.cumulative_sums = self._cumulative_sum(self.shifts, self.dial_starting_position)
        total_zero_position_equivalences = self._count_zero_position_equivalence(self.cumulative_sums)
        total_zero_position_equivalences_during_rotation = sum([self._count_zero_position_equivalences_exclusively_between(x, y, self.n_graduations) for x, y in zip(self.cumulative_sums, self.shifts)])
        return total_zero_position_equivalences + total_zero_position_equivalences_during_rotation
    
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
    
    def _count_zero_position_equivalences_exclusively_between(self, starting_position: int, shift: int, n_graduations: int) -> int:
        """Count how many zero position equivalents are found between two positions. Both positions exclusive."""
        count = 0

        step = 1 if shift > 0 else -1
        for position in range(starting_position + step, starting_position + shift, step):
            if position % n_graduations == 0:
                count += 1
        return count


if __name__ == "__main__":
    print("======Day 1, Part 1======")
    part_1_answer = SecretEntrancePasswordFinder(N_GRADUATIONS, DIAL_STARTING_POSITION, INPUT_P1_FILENAME).resolve_password()
    print("Answer: ", part_1_answer)
    print("")
    print("======Day 1, Part 2======")
    part_2_answer = SecretEntrancePasswordFinder(N_GRADUATIONS, DIAL_STARTING_POSITION, INPUT_P2_FILENAME).resolve_password_par2_2()
    print("Answer: ", part_2_answer)