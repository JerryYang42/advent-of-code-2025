# Day 3

https://adventofcode.com/2025/day/3


## Considerations

It's a easy greedy search. Each round of search is independent with its sub problem. So it's easy to change the recurrence to a loop.

## How to run

Init the project and with the lib. Make sure the root folder contains `pyproject.toml` file.

```zsh
uv init --lib
uv add --dev pytest
uv pip install -e .  # enable editable mode
```

Run the src file for printed out result

```zsh
python3 ./day3/src/main/python/LargestPossibleJoltageResolver.py
```

Run the tests

```zsh
uv run pytest day3/src/test/test_LargestPossibleJoltageResolver.py -v
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
