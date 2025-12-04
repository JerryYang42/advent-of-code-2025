# Day 3

https://adventofcode.com/2025/day/4


## Considerations

I think the key here is about converting the board of symbols into a board of scores. 
Hereby I defined the score of a paper roll as the number of its neighbor paper rolls.

As for the part 2, it reminds me of a flooding algorithm on the score board to cut down the iteration number.
My solution is iterative on the actual symbol board, so there should be space for improvement.

## How to run

Init the project and with the lib. Make sure the root folder contains `pyproject.toml` file.

```zsh
uv init --lib
uv add --dev pytest
uv pip install -e .  # enable editable mode
```

Run the src file for printed out result

```zsh
python3 ./day4/src/main/python/ForkliftAccessiblePaperRollLocater.py
```

Run the tests

```zsh
# No unit test so far
```

Or run all tests:

```zsh
uv run pytest -v
```

With coverages

```zsh
uv add --dev pytest-cov
uv run pytest --cov=day2 --cov-report=term-missing
```
