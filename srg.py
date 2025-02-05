def add_numbers(a, b):
    """
    Convert two values to integers and return their sum.
    
    This function attempts to convert both inputs, `a` and `b`, into integers and then computes their sum. If either conversion fails, a ValueError is raised with a message that includes the original error details.
    
    Parameters:
        a (Any): A value that must be convertible to an integer.
        b (Any): A value that must be convertible to an integer.
    
    Returns:
        int: The sum of the integer representations of `a` and `b`.
    
    Raises:
        ValueError: If either `a` or `b` cannot be converted to an integer.
    """
    try:
        return int(a) + int(b)
    except ValueError as e:
        raise ValueError(f"Both inputs must be convertible to an integer: {e}")

# Test with different types
print(add_numbers(5, "7"))  # Expected output: 12
