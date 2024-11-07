# tests for the calculator itself

import sys
from io import StringIO
from app.calculator import calculator

def run_calculator_with_input(monkeypatch, inputs):
    #simulates user inputs. Monkeypatch allows you to test functionality without messing with the source code
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