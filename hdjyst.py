def add_numbers(a, b):
    """
    Add two values and return their sum.
    
    This function returns the sum of the two supplied parameters without performing any type checking.
    If the provided values are of incompatible types (for example, an integer and a string), a TypeError will be raised.
    
    Parameters:
        a: The first value.
        b: The second value.
    
    Returns:
        The result of adding a and b.
    
    Example:
        >>> add_numbers(3, 4)
        7
        
        >>> add_numbers(5, "7")
        Traceback (most recent call last):
          ...
        TypeError: unsupported operand type(s) for +: 'int' and 'str'
    """
    return a + b

# Test with different types
print(add_numbers(5, "7"))
