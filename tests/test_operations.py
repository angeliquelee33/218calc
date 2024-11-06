from app.operations import addition, multiplication, subtraction

"addition test"
def test_addition():
    assert addition(1,1) == 2

"subtraction test"
def test_subtraction():
    assert subtraction(1,1) == 0

"multiplication test"
def test_multiplication():
    assert multiplication(2,2) == 4
    
