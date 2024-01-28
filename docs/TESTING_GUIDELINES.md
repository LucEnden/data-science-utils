# Test Guidelines

This document outlines guidelines & conventions for writing tests for this project.

As an example, we will outline the conventions for writing tests using the following example file:
```python
# dsutils/foo.py
def foo():
    print("foo")
```

## Test Frameworks

Tests should be written using the [unittest](https://docs.python.org/3/library/unittest.html) module.

For coverage, we will use [coverage.py](https://coverage.readthedocs.io/en/7.4.1/).

```bash
python3 -m pip install coverage
```

## Running Tests

From the root of the project, run the following command:
```bash
# From the root of the project
python -m unittest discover -s ./tests/
```

Running a single test file:
```bash
# From the root of the project
python -m unittest tests/test_foo.py
```

Running all tests with coverage report:
```bash
# From the root of the project
coverage run --source="./dsutils/" -m unittest discover -v -s ./tests/ && coverage report
```

Running all tests with a more readable coverage report:
```bash
coverage run --source="./dsutils/" -m unittest discover -v -s ./tests/ && coverage html
```

## Naming
Bellow are the naming conventions for the various test files and methods.

### Test Files
The file name should be the same as the file being tested, but with prefix of `test_`. For example: `foo.py`'s test should be`test_foo.py`

### Test Methods
The test method name should be named as followed: `test_<test type>_<method name>_<test description>`, where test type is either `UNIT`, `SYSTEM` or `CONVENTION`. For example:
```python
def test_UNIT_foo_does_not_raise_exception(self):
    ...
def test_SYSTEM_foo_works_when_called_from_cli(self):
    ...
def test_CONVENTION_has_docstring(self):
    ...
```

The body of the test method should be as followed:
```python
def test_UNIT_foo_does_not_raise_exception(self):
    #====      Arange      ====#
    ...
    #====       Act        ====#
    ...
    #====      Assert      ====#
    ...
```

Every test method should also have a docstring that describes what the test is testing. For example:
```python
def test_UNIT_foo_does_not_raise_exception(self):
    """
    Tests that the foo function does not raise an exception.
    """
    #====      Arange      ====#
    ...
    #====       Act        ====#
    ...
    #====      Assert      ====#
    ...
```

## Tests requiring files or directories
If any test requires a file or directory, the directory should be named after the test file, but with a postfix of `_dir`. For example: `test_file.py`'s directory should be `test_file_dir`. This directory should be placed in the same directory as the test file. This would make for the following directory structure:
```bash
tests/
    test_file.py
    test_file_dir/
```

This directories should only be created in the `setUp` method of the test file. They should be deleted in the `tearDown` method of the test file.

Every test of a file that reads or writes to a file should have a test that tests how that file handles common.

## Coverage requirements

The coverage report should be at least 80% for all files. If an argument is being made about the fact the file does not need to meet this coverage requirement, the argument should be made in the pull request.