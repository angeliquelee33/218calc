"addition function, with floats for decimals"

def addition(a: float, b: float) -> float:
    return a + b 

"subtraction operation"
def subtraction(a: float, b: float) -> float:
    return a - b

"multiplication operation"
def multiplication(a: float, b: float) -> float:
    return a * b

"division operation"
def division(a: float, b: float) -> float:
    if b == 0:
     raise ValueError("Division by zero is not allowed.")
    return a / b

       
    
