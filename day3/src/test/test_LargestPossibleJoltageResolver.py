import pytest
from unittest.mock import mock_open, patch
from day3.src.main.python.LargestPossibleJoltageResolver import LargestPossibleJoltageResolver

class TestLargestPossibleJoltageResolver:
    
    @patch("builtins.open", new_callable=mock_open, read_data="123456\n987654\n")
    def test_load_data(self, mock_file):
        resolver = LargestPossibleJoltageResolver()
        resolver.load_data("dummy.txt")
        assert resolver.data == ["123456", "987654"]
        # mock_file.assert_called_once_with(resolver.RESOURCE_DIR + "/dummy.txt", 'r')

    def test_find_largest_digit(self):
        resolver = LargestPossibleJoltageResolver()
        assert resolver.find_largest_digit("123456") == 5
        assert resolver.find_largest_digit("987654") == 0
        assert resolver.find_largest_digit("543216") == 5

    def test_find_largest_n_digit_number(self):
        resolver = LargestPossibleJoltageResolver()
        assert resolver.find_largest_n_digit_number("123456", 2) == 56
        assert resolver.find_largest_n_digit_number("987654", 3) == 987
        assert resolver.find_largest_n_digit_number("543216", 4) == 5436

    @patch("builtins.open", new_callable=mock_open, read_data="123456\n987654\n")
    def test_resolve(self, mock_file):
        resolver = LargestPossibleJoltageResolver()
        resolver.load_data("dummy.txt")
        result = resolver.resolve(2)
        assert result == [56, 98]