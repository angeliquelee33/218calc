import pytest 
from app.operations import addition, division, multiplication, subtraction

"addition test"
def test_addition():
    assert addition(1,1) == 2

"subtraction test"
def test_subtraction():
    assert subtraction(1,1) == 0

"multiplication test"
def test_multiplication():
    assert multiplication(2,2) == 4
    
"division test positive"
def test_division_positive():
    assert division(4,2) == 2

"division test negative"
def test_division_by_zero():
    with pytest.raises(ValueError, match="Division by zero is not allowed."):
        division(1, 0)
    