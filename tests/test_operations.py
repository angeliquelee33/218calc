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
    
"division test"
def test_division():
    assert division(4,2) == 2
    