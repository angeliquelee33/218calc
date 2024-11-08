"basic REPL calculator"

"first integrate functions from opertions"
from app.operations import addition, subtraction, multiplication, division 

from app.history import History

def calculator():
    """Basic REPL calculator that performs addition, subtraction, multiplication, and division."""
    
    # print welcome message upon program initialization 
    print("Welcome to the calculator REPL! Type 'exit' to quit")
  
    while True:
        # define user input variable (for operation, numbers and exiting)
        
        user_input = input("Enter an operation (add, subtract, multiply, divide) and two numbers, or 'exit' to quit: ")

        #exit command
        if user_input.lower() == "exit":
            print("Exiting calculator...")
            break  # this breaks the loop to exit program

        try:
            #defines the user inputs- what operation and the numbers to calculate
            operation, num1, num2 = user_input.split()
            #floats ensure that it's numerical values that are input
            num1, num2 = float(num1), float(num2)
        except ValueError:
            #error message for improper input such as letters
            print("Invalid input. Please follow the format: <operation> <num1> <num2>")
            continue  #continue repeats the loop from the beginning

        # here is where we deal with the different correct user inputs
        if operation == "add":
            result = addition(num1, num2) 
        elif operation == "subtract":
            result = subtraction(num1, num2) 
        elif operation == "multiply":
            result = multiplication(num1, num2) 
        elif operation == "divide":
            try:
                result = division(num1, num2) 
            except ValueError as e:
               #this catches divinding by 0 and prints an error message
                print(e)  
                continue  # starts the loop again
        else:
            # if an error occurs when typing the desired operation it prints error message
            print(f"Unknown operation '{operation}'. Supported operations: add, subtract, multiply, divide.")
            continue #starts loop over

       
        print(f"Result: {result}") #prints results