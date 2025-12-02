# Day 2

https://adventofcode.com/2025/day/2


## Considerations

The difficulties is the design of the data structure to store range, and enumerate the integers within the range. 

## How to run

Init the project and with the lib. Make sure the root folder contains `pyproject.toml` file.

```zsh
uv init --lib
uv add --dev pytest
uv pip install -e .  # enable editable mode
```

Run the src file for printed out result

```zsh
python3 ./day2/src/main/python/InvalidIdIdentifier.py
```

Run the tests

```zsh
uv run pytest day2/src/test/test_InvalidIdIdentifier.py -v
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
