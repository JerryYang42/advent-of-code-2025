import pytest
from day1.src.main.python.SecretEntrancePasswordFinder import SecretEntrancePasswordFinder

class TestSecretEntrancePasswordFinder:
    """Test suite for SecretEntrancePasswordFinder class"""
    
    @pytest.fixture
    def finder(self, tmp_path):
        """Create a test instance with a temporary input file"""
        # Create a temporary test file
        test_file = tmp_path / "test_input.txt"
        test_file.write_text("R5\nL3\nR10")
        
        # Create finder instance pointing to test file
        finder = SecretEntrancePasswordFinder.__new__(SecretEntrancePasswordFinder)
        finder.n_graduations = 100
        finder.dial_starting_position = 50
        finder.instruction_input_filepath = str(test_file)
        finder.instructions = finder._load_instructions()
        return finder
    
    # Tests for _parse_instruction
    def test_parse_instruction_right_single_digit(self, finder):
        """Test right turn with single digit magnitude"""
        assert finder._parse_instruction('R5') == 5

    def test_parse_instruction_right_multiple_digits(self, finder):
        """Test right turn with multiple digit magnitude"""
        assert finder._parse_instruction('R123') == 123

    def test_parse_instruction_left_single_digit(self, finder):
        """Test left turn with single digit magnitude"""
        assert finder._parse_instruction('L7') == -7

    def test_parse_instruction_left_multiple_digits(self, finder):
        """Test left turn with multiple digit magnitude"""
        assert finder._parse_instruction('L456') == -456

    def test_parse_instruction_right_zero(self, finder):
        """Test right turn with zero magnitude"""
        assert finder._parse_instruction('R0') == 0

    def test_parse_instruction_left_zero(self, finder):
        """Test left turn with zero magnitude"""
        assert finder._parse_instruction('L0') == 0

    def test_parse_instruction_large_magnitude(self, finder):
        """Test instruction with large magnitude"""
        assert finder._parse_instruction('R9999') == 9999
        assert finder._parse_instruction('L9999') == -9999

    # Tests for _cumulative_sum
    def test_cumulative_sum_empty_list(self, finder):
        """Test with empty list of shifts"""
        assert finder._cumulative_sum([]) == []
    
    def test_cumulative_sum_single_element(self, finder):
        """Test with single shift"""
        assert finder._cumulative_sum([5]) == [5]
    
    def test_cumulative_sum_multiple_elements(self, finder):
        """Test with multiple shifts"""
        assert finder._cumulative_sum([1, 2, 3, 4]) == [1, 3, 6, 10]
    
    def test_cumulative_sum_with_starting_position(self, finder):
        """Test cumulative sum with non-zero starting position"""
        assert finder._cumulative_sum([1, 2, 3], starting_position=10) == [11, 13, 16]
    
    def test_cumulative_sum_negative_shifts(self, finder):
        """Test with negative shifts"""
        assert finder._cumulative_sum([-5, -3, -2]) == [-5, -8, -10]
    
    def test_cumulative_sum_mixed_shifts(self, finder):
        """Test with mixed positive and negative shifts"""
        assert finder._cumulative_sum([10, -5, 3, -8]) == [10, 5, 8, 0]
    
    def test_cumulative_sum_with_zeros(self, finder):
        """Test with zero shifts"""
        assert finder._cumulative_sum([0, 5, 0, -3]) == [0, 5, 5, 2]
    
    def test_cumulative_sum_negative_starting_position(self, finder):
        """Test with negative starting position"""
        assert finder._cumulative_sum([5, 10, -3], starting_position=-20) == [-15, -5, -8]
    
    # Tests for _count_zero_position_equivalence_after_rotation
    def test_count_zero_position_equivalence_no_matches(self, finder):
        """Test when no positions are divisible by n_graduations"""
        assert finder._count_zero_position_equivalence_after_rotation([1, 2, 3, 50, 99]) == 0
    
    def test_count_zero_position_equivalence_single_match(self, finder):
        """Test with single position divisible by n_graduations"""
        assert finder._count_zero_position_equivalence_after_rotation([50, 100, 150]) == 1
    
    def test_count_zero_position_equivalence_multiple_matches(self, finder):
        """Test with multiple positions divisible by n_graduations"""
        assert finder._count_zero_position_equivalence_after_rotation([100, 200, 300, 50]) == 3
    
    def test_count_zero_position_equivalence_with_zero(self, finder):
        """Test with zero in the list"""
        assert finder._count_zero_position_equivalence_after_rotation([0, 50, 100]) == 2
    
    def test_count_zero_position_equivalence_negative_multiples(self, finder):
        """Test with negative multiples of n_graduations"""
        assert finder._count_zero_position_equivalence_after_rotation([-100, -200, 0, 100]) == 4
    
    # Tests for _load_instructions
    def test_load_instructions_valid(self, tmp_path):
        """Test loading valid instructions from file"""
        test_file = tmp_path / "valid_input.txt"
        test_file.write_text("R5\nL10\nR3")
        
        finder = SecretEntrancePasswordFinder.__new__(SecretEntrancePasswordFinder)
        finder.instruction_input_filepath = str(test_file)
        instructions = finder._load_instructions()
        
        assert instructions == ['R5', 'L10', 'R3']
    
    def test_load_instructions_invalid_prefix(self, tmp_path):
        """Test that invalid instruction prefix raises ValueError"""
        test_file = tmp_path / "invalid_input.txt"
        test_file.write_text("R5\nX10\nL3")
        
        finder = SecretEntrancePasswordFinder.__new__(SecretEntrancePasswordFinder)
        finder.instruction_input_filepath = str(test_file)
        
        with pytest.raises(ValueError, match="Invalid instruction found on line 2"):
            finder._load_instructions()
    
    def test_load_instructions_invalid_magnitude(self, tmp_path):
        """Test that non-numeric magnitude raises ValueError"""
        test_file = tmp_path / "invalid_input.txt"
        test_file.write_text("R5\nLabc")
        
        finder = SecretEntrancePasswordFinder.__new__(SecretEntrancePasswordFinder)
        finder.instruction_input_filepath = str(test_file)
        
        with pytest.raises(ValueError, match="Invalid instruction found on line 2"):
            finder._load_instructions()
    
    def test_load_instructions_empty_lines_stripped(self, tmp_path):
        """Test that empty lines are handled correctly"""
        test_file = tmp_path / "input_with_empty.txt"
        test_file.write_text("R5\n\nL10")
        
        finder = SecretEntrancePasswordFinder.__new__(SecretEntrancePasswordFinder)
        finder.instruction_input_filepath = str(test_file)
        
        with pytest.raises(ValueError, match="Invalid instruction found on line 2"):
            finder._load_instructions()

    # Tests for _count_zero_position_equivalences_exclusively_between
    def test_count_zero_position_equivalences_exclusively_between_positive_shift_no_matches(self, finder):
        """Test positive shift with no zero position equivalents in between"""
        assert finder._count_zero_position_equivalences_exclusively_between(10, 20, 100) == 0

    def test_count_zero_position_equivalences_exclusively_between_positive_shift_single_match(self, finder):
        """Test positive shift crossing one zero position equivalent"""
        assert finder._count_zero_position_equivalences_exclusively_between(50, 60, 100) == 1

    def test_count_zero_position_equivalences_exclusively_between_positive_shift_multiple_matches(self, finder):
        """Test positive shift crossing multiple zero position equivalents"""
        assert finder._count_zero_position_equivalences_exclusively_between(50, 250, 100) == 2

    def test_count_zero_position_equivalences_exclusively_between_negative_shift_no_matches(self, finder):
        """Test negative shift with no zero position equivalents in between"""
        assert finder._count_zero_position_equivalences_exclusively_between(30, -20, 100) == 0

    def test_count_zero_position_equivalences_exclusively_between_negative_shift_single_match(self, finder):
        """Test negative shift crossing one zero position equivalent"""
        assert finder._count_zero_position_equivalences_exclusively_between(150, -60, 100) == 1

    def test_count_zero_position_equivalences_exclusively_between_negative_shift_multiple_matches(self, finder):
        """Test negative shift crossing multiple zero position equivalents"""
        assert finder._count_zero_position_equivalences_exclusively_between(250, -250, 100) == 2

    def test_count_zero_position_equivalences_exclusively_between_zero_shift(self, finder):
        """Test with zero shift (no movement)"""
        assert finder._count_zero_position_equivalences_exclusively_between(50, 0, 100) == 0

    def test_count_zero_position_equivalences_exclusively_between_starting_at_zero_equivalent(self, finder):
        """Test starting exactly at zero position equivalent"""
        assert finder._count_zero_position_equivalences_exclusively_between(100, 50, 100) == 0

    def test_count_zero_position_equivalences_exclusively_between_ending_at_zero_equivalent(self, finder):
        """Test ending exactly at zero position equivalent (exclusive)"""
        assert finder._count_zero_position_equivalences_exclusively_between(50, 50, 100) == 0

    def test_count_zero_position_equivalences_exclusively_between_both_positions_exclusive(self, finder):
        """Test that both start and end positions are exclusive"""
        # From 0 to 200, should count 100 but not 0 or 200
        assert finder._count_zero_position_equivalences_exclusively_between(0, 200, 100) == 1

    def test_count_zero_position_equivalences_exclusively_between_negative_positions(self, finder):
        """Test with negative starting position crossing zero"""
        assert finder._count_zero_position_equivalences_exclusively_between(-150, 250, 100) == 2
        assert finder._count_zero_position_equivalences_exclusively_between(-150, 251, 100) == 3

    def test_count_zero_position_equivalences_exclusively_between_small_shift(self, finder):
        """Test with shift smaller than n_graduations"""
        assert finder._count_zero_position_equivalences_exclusively_between(95, 5, 100) == 0

    def test_count_zero_position_equivalences_exclusively_between_exact_graduation_span(self, finder):
        """Test shift that is exactly n_graduations"""
        assert finder._count_zero_position_equivalences_exclusively_between(0, 100, 100) == 0
        assert finder._count_zero_position_equivalences_exclusively_between(50, 100, 100) == 1

