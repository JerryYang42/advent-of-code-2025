# Day 5

https://adventofcode.com/2025/day/5


## Considerations

It's about merging overlapped ranges, that makes the complexity to be O(n), while
n is the number of ranges.

## How to run

Init the project and with the lib. Make sure the root folder contains `pyproject.toml` file.

```zsh
uv init --lib
uv add --dev pytest
uv pip install -e .  # enable editable mode
```

Run the src file for printed out result

```zsh
python3 ./day5/src/main/python/FreshIngredientIdChecker.py
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
uv run pytest --cov=day5 --cov-report=term-missing
```
