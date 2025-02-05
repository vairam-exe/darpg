def add_numbers(a, b):
    """
    Return the sum of a and b.
    
    This function returns the result of adding the two provided arguments using Python's built-in addition operator.
    It does not perform type checking, so supplying incompatible types (such as an integer and a string) will raise a TypeError.
    
    Parameters:
        a: Any type that supports the addition operator.
        b: Any type that supports the addition operator.
    
    Returns:
        The result of a + b, with the type determined by the operands.
    
    Examples:
        >>> add_numbers(3, 7)
        10
        >>> add_numbers("Foo", "Bar")
        'FooBar'
    """
    return a + b

# Test with different types
print(add_numbers(5, "7"))
