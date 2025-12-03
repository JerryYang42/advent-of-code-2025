import pytest
import os
import tempfile
from day2.src.main.python.InvalidIdIdentifier import InvalidIdIdentifier
import day2.src.main.python.InvalidIdIdentifier as module


@pytest.fixture
def temp_test_dir():
    """Create and cleanup temporary directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)


@pytest.fixture
def mock_resources_dir(temp_test_dir):
    """Mock RESOURCES_DIR for testing."""
    original = module.RESOURCES_DIR
    module.RESOURCES_DIR = temp_test_dir
    yield temp_test_dir
    module.RESOURCES_DIR = original


@pytest.fixture
def identifier(mock_resources_dir):
    """Create InvalidIdIdentifier instance for testing."""
    test_file = os.path.join(mock_resources_dir, 'test.txt')
    with open(test_file, 'w') as f:
        f.write('1-10')
    return InvalidIdIdentifier('test.txt')


class TestIsAProbableRange:
    
    def test_probable_range_both_even_length(self, identifier):
        """Test range with both even-length numbers."""
        assert identifier._is_a_probable_range((10, 99), 2) is True
    
    def test_probable_range_both_odd_length_same_digits(self, identifier):
        """Test range with both odd-length numbers with same digit count."""
        assert identifier._is_a_probable_range((100, 999), 2) is False
    
    def test_probable_range_both_odd_length_different_digits(self, identifier):
        """Test range with both odd-length numbers with different digit counts."""
        assert identifier._is_a_probable_range((100, 10000), 2) is True
    
    def test_probable_range_start_odd_end_even(self, identifier):
        """Test range with odd-length start and even-length end."""
        assert identifier._is_a_probable_range((100, 1000), 2) is True
    
    def test_probable_range_start_even_end_odd(self, identifier):
        """Test range with even-length start and odd-length end."""
        assert identifier._is_a_probable_range((10, 100), 2) is True
    
    def test_probable_range_single_digit_odd(self, identifier):
        """Test range with single-digit (odd-length) numbers."""
        assert identifier._is_a_probable_range((1, 9), 2) is False


class TestLoadRangesFromTxt:
    
    def test_load_single_range(self, mock_resources_dir):
        """Test loading a single range."""
        filename = 'test1.txt'
        with open(os.path.join(mock_resources_dir, filename), 'w') as f:
            f.write('1-10')
        identifier = InvalidIdIdentifier(filename)
        assert identifier.ranges == [(1, 10)]
    
    def test_load_multiple_ranges(self, mock_resources_dir):
        """Test loading multiple ranges."""
        filename = 'test2.txt'
        with open(os.path.join(mock_resources_dir, filename), 'w') as f:
            f.write('1-10,20-30,100-200')
        identifier = InvalidIdIdentifier(filename)
        assert identifier.ranges == [(1, 10), (20, 30), (100, 200)]
    
    def test_invalid_format_no_separator(self, mock_resources_dir):
        """Test invalid format without separator."""
        filename = 'test3.txt'
        with open(os.path.join(mock_resources_dir, filename), 'w') as f:
            f.write('110')
        with pytest.raises(ValueError):
            InvalidIdIdentifier(filename)
    
    def test_invalid_format_multiple_separators(self, mock_resources_dir):
        """Test invalid format with multiple separators."""
        filename = 'test4.txt'
        with open(os.path.join(mock_resources_dir, filename), 'w') as f:
            f.write('1-10-20')
        with pytest.raises(ValueError):
            InvalidIdIdentifier(filename)
    
    def test_invalid_format_non_numeric(self, mock_resources_dir):
        """Test invalid format with non-numeric values."""
        filename = 'test5.txt'
        with open(os.path.join(mock_resources_dir, filename), 'w') as f:
            f.write('a-b')
        with pytest.raises(ValueError):
            InvalidIdIdentifier(filename)
    
    def test_invalid_range_start_greater_than_end(self, mock_resources_dir):
        """Test invalid range where start > end."""
        filename = 'test6.txt'
        with open(os.path.join(mock_resources_dir, filename), 'w') as f:
            f.write('10-1')
        with pytest.raises(ValueError):
            InvalidIdIdentifier(filename)

class TestLeftHalf:
    
    def test_left_half_even_length(self, identifier):
        """Test left half extraction for even-length number."""
        assert identifier._left_half(1234) == 12
    
    def test_left_half_single_digit(self, identifier):
        """Test left half extraction for single-digit number."""
        with pytest.raises(AssertionError):
            identifier._left_half(7)
    
    def test_left_half_odd_length_raises(self, identifier):
        """Test that odd-length number raises assertion error."""
        with pytest.raises(AssertionError):
            identifier._left_half(12345)

class TestDivisiableLengthBy:
    
    def test_divisible_length_by_true(self, identifier):
        """Test divisible length by returns True."""
        assert identifier._divisible_length_by(1234, 2) is True
        assert identifier._divisible_length_by(123456, 3) is True
    
    def test_divisible_length_by_false(self, identifier):
        """Test divisible length by returns False."""
        assert identifier._divisible_length_by(12345, 2) is False
        assert identifier._divisible_length_by(1234, 3) is False

class TestGenerateInvalidIdsInRangeWithinSameMagnitude:
    
    def test_generate_invalid_ids_in_range(self, identifier):
        """Test generating invalid IDs in a given range."""
        result = identifier.generate_invalid_ids_in_range_within_same_magnitude((1000, 1999), 2)
        expected = [1010, 1111, 1212, 1313, 1414, 1515, 1616, 1717, 1818, 1919]
        assert result == expected
    
    def test_generate_invalid_ids_no_invalids(self, identifier):
        """Test range with no invalid IDs."""
        result = identifier.generate_invalid_ids_in_range_within_same_magnitude((100, 199), 2)
        assert result == []
    
    def test_generate_invalid_ids_single_value_range(self, identifier):
        """Test range with a single value that is invalid."""
        result = identifier.generate_invalid_ids_in_range_within_same_magnitude((1212, 1212), 2)
        assert result == [1212]
    
    def test_generate_invalid_ids_single_value_range_not_invalid(self, identifier):
        """Test range with a single value that is not invalid."""
        result = identifier.generate_invalid_ids_in_range_within_same_magnitude((1234, 1234), 2)
        assert result == []

class TestBreakdownRangeIntoMagnitudes:
    
    def test_breakdown_range_single_magnitude(self, identifier):
        """Test breakdown of range within single magnitude."""
        result = identifier._breakdown_range_into_magnitudes((10, 99))
        assert result == [(10, 99)]
    
    def test_breakdown_range_multiple_magnitudes(self, identifier):
        """Test breakdown of range across multiple magnitudes."""
        result = identifier._breakdown_range_into_magnitudes((95, 1050))
        assert result == [(95, 99), (100, 999), (1000, 1050)]
    
    def test_breakdown_range_single_value(self, identifier):
        """Test breakdown of range with single value."""
        result = identifier._breakdown_range_into_magnitudes((500, 500))
        assert result == [(500, 500)]
