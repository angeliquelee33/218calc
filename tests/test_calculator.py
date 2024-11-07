# tests for the calculator itself

import sys
from io import StringIO
from app.calculator import calculator

def run_calculator_with_input(monkeypatch, inputs):
    #simulates user inputs. Monkeypatch allows you to test functionality without messing with the source code. 
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

 # Captures output of the calculator
    captured_output = StringIO()
    sys.stdout = captured_output
    calculator()
    sys.stdout = sys.__stdout__  
    return captured_output.getvalue()

#positive input tests


#test addition
def test_addition(monkeypatch):
    inputs = ["add 2 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output

#REPL test for subtraction
def test_subtraction(monkeypatch):
    inputs = ["subtract 5 2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 3.0" in output

#REPL multiplication test
def test_multiplication(monkeypatch):
    inputs = ["multiply 4 5", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 20.0" in output

#REPL division test
def test_division(monkeypatch):
    inputs = ["divide 10 2", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 5.0" in output

# Negative tests

#REPL test for invalid operation input
def test_invalid_operation(monkeypatch):
    inputs = ["modulus 5 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Unknown operation" in output

#input format test (user inputs not put numerically)
def test_invalid_input_format(monkeypatch):
    inputs = ["add two three", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid input. Please follow the format" in output
    