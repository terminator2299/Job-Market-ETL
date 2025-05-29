# scripts/utils.py

import re

def parse_salary(salary_str):
    """
    Parse a salary string to extract a numeric value.
    This is a simplified example; customize as needed.
    """
    if not isinstance(salary_str, str):
        return None
    # Extract all numbers (could be ranges or single)
    numbers = re.findall(r'\d+', salary_str.replace(',', ''))
    if not numbers:
        return None
    # Return the average if a range, else the single number as int
    numbers = list(map(int, numbers))
    if len(numbers) == 1:
        return numbers[0]
    else:
        return sum(numbers) // len(numbers)
