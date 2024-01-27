# Test Conventions

This document outlines the conventions for writing tests for this project. 

## Test Framework

Tests should be written using the [unittest](https://docs.python.org/3/library/unittest.html) module.

## Running Tests

From the root of the project, run the following command:
```bash
python -m unittest discover -s ./tests/
```

## Naming
The file name should be the same as the file being tested, but with prefix of `test_`.
- `file.py` should be`test_file.py`