# About

This is my solution to [Advent of Code Day 1](https://adventofcode.com/2025/day/1).

## Progress
Cracked Day 1 in a hacky way. 

TODOs:
- use online data instead of data file

## How to run

Init the project and with the lib. Make sure the root folder contains `pyproject.toml` file.

```zsh
uv init --lib
uv add --dev pytest
uv pip install -e .  # enable editable mode
```

Run the src file for print out result

```zsh
python3 day1/src/main/P1.py
```

Run the tests

```zsh
uv run pytest day1/src/test/test_SecretEntrancePasswordFinder.py.py -v
```

Or run all tests:

```zsh
uv run pytest -v
```

With coverages

```zsh
uv add --dev pytest-cov
uv run pytest --cov=day1 --cov-report=term-missing
```

FAQ

What benefit does `uv`'s editable mode bring?

With editable mode, you can use clean imports:

```
# No sys.path manipulation needed!
from day1.src.main.SecretEntrancePasswordFinder import SecretEntrancePasswordFinder

# Otherwise, have to use sys.path hacks:
sys.path.insert(0, str(Path(__file__).parent.parent))
from main.SecretEntrancePasswordFinder import SecretEntrancePasswordFinder
```

It generates a link from site-packages to your source directory. Perfect for development.

