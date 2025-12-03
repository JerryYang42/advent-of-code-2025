import os

RESOURCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')


class LargestPossibleJoltageResolver:

    def __init__(self):
        self.data = None

    def resolve(self, n_digit) -> int:
        result = []
        for line in self.data:
            # result.append(self.find_largest_two_digit_number(line))
            result.append(self.find_largest_n_digit_number(line, n_digit))
        return result
    
    def find_largest_n_digit_number(self, value_string: str, n: int) -> int:
        assert len(value_string) >= n, "Value string length must be at least n"
        positions = []
        start_index = 0
        for i in range(n):
            substring_length = len(value_string) - (n - i - 1)
            substring = value_string[start_index:substring_length]
            pos = self.find_largest_digit(substring)
            positions.append(pos + start_index)
            start_index = positions[-1] + 1
        largest_number = ''.join(value_string[pos] for pos in positions)
        return int(largest_number)
    
    @DeprecationWarning
    def find_largest_two_digit_number(self, value_string: str) -> int:
        first_digit_pos = self.find_largest_digit(value_string[:-1])
        second_digit_pos = self.find_largest_digit(value_string[first_digit_pos + 1:])
        return int(value_string[first_digit_pos] + value_string[second_digit_pos + first_digit_pos + 1])
    
    def find_largest_digit(self, value_string: str) -> int:
        largest = -1
        largest_pos = -1
        for curr in range(len(value_string)):
            if int(value_string[curr]) > largest:
                largest = int(value_string[curr])
                largest_pos = curr
        return largest_pos
    
    def load_data(self, filename: str) -> list[str]:
        with open(os.path.join(RESOURCE_DIR, filename), 'r') as file:
            adapters = [line.strip() for line in file.readlines()]
            self.data = adapters
        return self

if __name__ == "__main__":
    puzzle_input_filename = "puzzle_input_sample.txt"
    resolver = LargestPossibleJoltageResolver()
    n_digits = 2
    resolver.load_data(puzzle_input_filename)
    answer_for_sample = resolver.resolve(n_digits)
    assert answer_for_sample == [98, 89, 78, 92], f"Expected [98, 89, 78, 92], got {answer_for_sample}"
    print(f"Largest possible {n_digits}-digit joltage for device: {answer_for_sample}")

    print("======Day 3, Part 1======")
    puzzle_input_filename = "puzzle_input.txt"
    n_digits = 2
    resolver.load_data(puzzle_input_filename)
    answer_for_puzzle = resolver.resolve(n_digits)
    print(f"Summation of all largest possible joltage for device: {sum(answer_for_puzzle)}")

    print("======Day 3, Part 2======")
    resolver.load_data(puzzle_input_filename)
    n_digits = 12
    answer_for_puzzle = resolver.resolve(n_digits)
    print(f"Summation of all largest possible {n_digits}-digit joltage for device: {sum(answer_for_puzzle)}")
    

