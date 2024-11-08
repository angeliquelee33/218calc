# Import necessary modules and classes
from app.operations import addition, subtraction, multiplication, division
from app.history import History

def calculator():
    """Basic REPL calculator with history support."""

    # Create a History object
    history = History()

    # Welcome message
    print("Welcome to the calculator REPL! Type 'exit' to quit.")
    print("You can also type 'history' to view past calculations, 'clear' to clear history, or 'undo' to remove the last calculation.")

    # Start the REPL loop
    while True:
        user_input = input("Enter an operation (add, subtract, multiply, divide) and two numbers, or a command: ")

        # Handle special commands
        if user_input.lower() == "exit":
            print("Exiting calculator...")
            break
        elif user_input.lower() == "history":
            print("Calculation History:")
            for calc in history.get_history():
                print(calc)
            continue
        elif user_input.lower() == "clear":
            history.clear_history()
            print("History cleared.")
            continue
        elif user_input.lower() == "undo":
            history.undo_last()
            print("Last calculation undone.")
            continue

        # Process calculation input
        else:
            try:
                operation, num1, num2 = user_input.split()
                num1, num2 = float(num1), float(num2)
            except ValueError:
                print("Invalid input. Please follow the format: <operation> <num1> <num2>")
                continue

            # Perform the requested operation
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
                    print(e)
                    continue
            else:
                print(f"Unknown operation '{operation}'. Supported operations: add, subtract, multiply, divide.")
                continue

            # Store the calculation in history
            calculation_str = f"{operation} {num1} {num2} = {result}"
            history.add_calculation(calculation_str)

            # Display the result
            print(f"Result: {result}")