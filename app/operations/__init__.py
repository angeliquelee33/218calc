
def addition(a: float, b: float) -> float:
    """Adds two numbers and returns the result."""
    return a + b

def subtraction(a: float, b: float) -> float:
    """Subtracts the second number from the first and returns the result."""
    return a - b

def multiplication(a: float, b: float) -> float:
    """Multiplies two numbers and returns the result."""
    return a * b

def division(a: float, b: float) -> float:
    """Divides the first number by the second and returns the result."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b
    
