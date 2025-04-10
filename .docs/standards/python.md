# Python Coding Standards

This document outlines our Python coding standards and best practices. Following these guidelines ensures consistency, readability, and maintainability across all Python codebases in the project.

## Table of Contents

1. [PEP 8 Compliance](#1-pep-8-compliance)
2. [Code Formatting](#2-code-formatting)
3. [Naming Conventions](#3-naming-conventions)
4. [Imports Organization](#4-imports-organization)
5. [Documentation Standards](#5-documentation-standards)
6. [Code Structure](#6-code-structure)
7. [Type Annotations](#7-type-annotations)
8. [Error Handling](#8-error-handling)
9. [Testing Strategy](#9-testing-strategy)
10. [Code Quality Tools](#10-code-quality-tools)

## 1. PEP 8 Compliance

All Python code must follow the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/) for consistent formatting and style.

## 2. Code Formatting

### 2.1 Indentation and Line Length
- Use 4 spaces per indentation level (no tabs)
- Limit lines to 79 characters for code, 72 for comments/docstrings
- Use line continuation for long expressions (wrap after operators)

```python
# Correct
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Incorrect
def long_function_name(var_one, var_two, var_three,
    var_four):
    print(var_one)
```

## 3. Naming Conventions

### 3.1 Casing Standards
- `snake_case` for functions, variables, and modules
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Prefix private attributes with underscore: `_private_var`

### 3.2 Descriptive Naming
- Use clear, meaningful names that explain purpose
- Avoid abbreviations unless widely understood
- Function names should indicate actions (e.g., `calculate_total`, `get_user_data`)
- Boolean variables should read as conditions (e.g., `is_valid`, `has_permission`)

```python
# Correct
def calculate_average_score(student_scores):
    total_score = sum(student_scores)
    count = len(student_scores)
    return total_score / count if count > 0 else 0

# Incorrect
def calc_avg(s):
    t = sum(s)
    c = len(s)
    return t / c if c > 0 else 0
```

## 4. Imports Organization

- Group imports in the following order:
  1. Standard library imports
  2. Third-party library imports
  3. Local application imports
- Separate each group with a blank line
- Alphabetize imports within each group

```python
# Standard library
import os
import sys

# Third-party libraries
import numpy as np
import pandas as pd

# Local application
from mypackage import utils
from mypackage.models import User
```

## 5. Documentation Standards

- Use docstrings for all public modules, functions, classes, and methods
- Follow Google style or NumPy style docstrings consistently
- Write comments that explain WHY, not WHAT the code does

```python
def calculate_discount(price, discount_percentage):
    """Calculate the discounted price.

    Args:
        price (float): The original price
        discount_percentage (float): The discount percentage (0-100)

    Returns:
        float: The price after applying the discount

    Raises:
        ValueError: If discount_percentage is not between 0 and 100
    """
    if not 0 <= discount_percentage <= 100:
        raise ValueError("Discount percentage must be between 0 and 100")
    
    discount_factor = 1 - (discount_percentage / 100)
    return price * discount_factor
```

## 6. Code Structure

### 6.1 Modularity
- Design functions with single responsibilities
- Keep functions short and focused (generally under 50 lines)
- Avoid deep nesting of code blocks (maximum 3-4 levels)
- Extract repeated code patterns into separate functions

```python
# Correct: Separate responsibilities
def validate_input(data):
    """Validate the input data."""
    # Validation logic

def process_data(data):
    """Process the validated data."""
    # Processing logic

def main():
    data = get_data()
    if validate_input(data):
        process_data(data)

# Incorrect: Mixed responsibilities
def process_data(data):
    # Validation logic mixed with processing
    # Error handling mixed with business logic
    # ...
```

## 7. Type Annotations

- Use type hints for function parameters and return values
- Implement static type checking with mypy
- Use `Optional[]` for parameters that may be None

```python
from typing import List, Dict, Optional, Union, Tuple

def process_user_data(
    user_id: int,
    data: Dict[str, str],
    options: Optional[List[str]] = None
) -> Tuple[bool, Union[Dict[str, str], str]]:
    """Process user data with optional settings.
    
    Args:
        user_id: The user identifier
        data: Key-value data to process
        options: Optional processing directives
        
    Returns:
        A tuple containing success status and either result data or error message
    """
    options = options or []
    # Processing logic
    success = True
    result = {"processed": "data"}
    return success, result
```

## 8. Error Handling

- Use specific exception types rather than broad exceptions
- Handle exceptions at the appropriate level of abstraction
- Include contextual information in error messages
- Use context managers (`with` statements) for resource management

```python
# Correct
def read_config_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"Configuration file {filename} not found")
        return default_config()
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filename}: {e}")
        return default_config()

# Incorrect
def read_config_file(filename):
    try:
        file = open(filename, 'r')
        return json.load(file)
    except Exception as e:
        logger.error(f"Error: {e}")
        return {}
```

## 9. Testing Strategy

- Write unit tests for all public functions and methods
- Use pytest as the testing framework
- Achieve high test coverage for critical code paths
- Include both positive and negative test cases
- Implement parameterized tests for comprehensive coverage

```python
# file: test_calculator.py
import pytest
from calculator import add

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2
    
def test_add_mixed_numbers():
    assert add(-5, 10) == 5

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (10, -5, 5),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

## 10. Code Quality Tools

Enforce these standards using the following tools:

| Tool | Purpose | Configuration |
|------|---------|--------------|
| flake8 | Linting | `.flake8` file in project root |
| black | Formatting | `pyproject.toml` with line-length=79 |
| isort | Import sorting | Configuration in `pyproject.toml` |
| mypy | Type checking | `mypy.ini` in project root |
| pytest | Testing | `pytest.ini` or `conftest.py` |

Run these tools as part of your development workflow and CI/CD pipeline.