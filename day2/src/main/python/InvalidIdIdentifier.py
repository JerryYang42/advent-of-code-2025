import os
from typing import List

RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')

class InvalidIdIdentifier():
    """Exception raised for invalid ID identifiers."""
    def __init__(self, input_filename: str):
        self.input_filename = input_filename
        self.ranges = self._load_ranges_from_txt(input_filename)
    
    def sum_of_invalid_ids_in_ranges(self, repeating_count: int) -> int:
        """Sum of invalid IDs in all loaded ranges."""
        invalid_ids = self.search_invalid_ids_in_ranges(repeating_count)
        return sum(invalid_ids)
    
    def search_invalid_ids_in_ranges(self, repeating_count: int) -> List[int]:
        """Search for invalid IDs in all loaded ranges."""
        invalid_ids = []
        ranges_of_same_magnitude = []
        for pair in self.ranges:
            start, end = pair
            ranges_of_same_magnitude.extend(self._breakdown_range_into_magnitudes(start, end))
        for pair in ranges_of_same_magnitude:
            start, end = pair
            invalid_ids.extend(self.generate_invalid_ids_in_range_within_same_magnitude(start, end, repeating_count))
        return invalid_ids

    def generate_invalid_ids_in_range_within_same_magnitude(self, start: int, end: int, repeating_count: int) -> list:
        """Search for invalid IDs in the given range."""
        assert self._digits(start) == self._digits(end), "Range must be within the same magnitude."
        if not self._is_a_probable_range(start, end, repeating_count):
            return []

        invalid_ids = []

        seed_window_start = self._left_half(start)
        seed_window_end = self._left_half(end)
        for half in range(seed_window_start, seed_window_end + 1):
            invalid_id = self._generating_invalid_ids(half, repeating_count)
            if start <= invalid_id <= end:
                invalid_ids.append(invalid_id)
        return invalid_ids
    
    def _breakdown_range_into_magnitudes(self, start: int, end: int) -> list:
        """Break down a range into sub-ranges of the same magnitude."""
        ranges = []
        current_start = start
        while current_start <= end:
            current_magnitude = self._digits(current_start)
            current_end = min(end, int('9' * current_magnitude))
            ranges.append((current_start, current_end))
            current_start = current_end + 1
        return ranges
    
    def _generating_invalid_ids(self, repeating_unit: int, repeat_count: int) -> int:
        """Generate an invalid ID by repeating a unit."""
        str_unit = str(repeating_unit)
        return int(str_unit * repeat_count)

    def _is_a_probable_range(self, start: int, end: int, repeating_count: int) -> bool:
        """A probable range is one where there is a chance of having invalid IDs."""
        if self._is_same_magnitude(start, end):
            return self._divisible_length_by(start, repeating_count)
        return True
    
    def _is_same_magnitude(self, start: int, end: int) -> bool:
        """Check if both numbers in the range have the same number of digits."""
        return self._digits(start) == self._digits(end)
    
    def _digits(self, value: int) -> int:
            return len(str(value))
    
    def _is_odd_length(self, value: int) -> bool:
        return self._digits(value) % 2 != 0
    
    def _divisible_length_by(self, value: int, divisor: int) -> bool:
        return self._digits(value) % divisor == 0
    
    def _left_half(self, value: int) -> int:
        """Get the left half of a number with an even number of digits."""
        assert self._divisible_length_by(value, 2), "Value must have an even number of digits."
        mid = self._digits(value) // 2
        str_value = str(value)
        return int(str_value[:mid])

    def _load_ranges_from_txt(self, filename: str) -> list:
        lines = []
        with open(os.path.join(RESOURCES_DIR, filename), 'r') as file:
            lines = file.readlines()
        line = lines[0]

        def _parse_ranges_from_line(line: str) -> list:
            BETWEEN_PAIR_SEPARATOR = ','
            IN_PAIR_SEPARATOR = '-'

            ranges = []

            parts = line.strip().split(BETWEEN_PAIR_SEPARATOR)
            for part in parts:
                def _validate_range_format(part: str) -> bool:
                    if IN_PAIR_SEPARATOR not in part:
                        raise ValueError(f"Invalid range format: {part}, missing separator.")
                    if part.count(IN_PAIR_SEPARATOR) != 1:
                        raise ValueError(f"Invalid range format: {part}, multiple separators found.")
                    if not part.replace(IN_PAIR_SEPARATOR, '').isdigit():
                        raise ValueError(f"Invalid range format: {part}, non-numeric values found.")
                    return True
                
                def _parse_range(part: str) -> tuple:
                    pair = list(filter(lambda x: x != IN_PAIR_SEPARATOR, part.split(IN_PAIR_SEPARATOR)))
                    try:
                        start = int(pair[0])
                        end = int(pair[1])
                        if start > end:
                            raise ValueError(f"Start of range {start} cannot be greater than end {end}.")
                        return (start, end)
                    except ValueError as e:
                        raise ValueError(f"Invalid numeric values in range: {part} with error {e}")
                
                _validate_range_format(part)
                pair = _parse_range(part)
                ranges.append(pair)
                    
            return ranges
        
        return _parse_ranges_from_line(line)


if __name__ == "__main__":
    identifier = InvalidIdIdentifier('input.txt')

    print("======Day 2, Part 1======")
    invalid_ids = identifier.search_invalid_ids_in_ranges(2)
    print("Number of invalid IDs found:", len(invalid_ids))
    print("Sum of invalid IDs found:", identifier.sum_of_invalid_ids_in_ranges(2))
    print("======Day 2, Part 2======")
    print("Not implemented yet.")
