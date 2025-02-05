def add_numbers(a, b):
    """
    Converts inputs to integers and returns their sum.
    If conversion fails, it raises a ValueError.
    """
    try:
        return int(a) + int(b)
    except ValueError as e:
        raise ValueError(f"Both inputs must be convertible to an integer: {e}")

# Test with different types
print(add_numbers(5, "7"))  # Expected output: 12
