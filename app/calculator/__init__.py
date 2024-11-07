"basic REPL calculator"

"first integrate functions from opertions"
from app.operations import addition, subtraction, multiplication, division

def calculator():
    """Basic REPL calculator that performs addition, subtraction, multiplication, and division."""
    
    # print welcome message upon program initialization 
    print("Welcome to the calculator REPL! Type 'exit' to quit")
 
    while True: #this keeps the program running on a loop until told to exit
         user_input = input #defined variable for user inputs(operation, numbers, exit)
          
        