from calculator import plus, minus, multiplicate, devide, square_root

def main():
    test_plus()
    test_minus()
    test_multiplicate()
    test_devide()
    test_square_root()

def test_plus():
    assert plus(10,30) == 40
    assert plus(3500, 6500) == 10000
    assert plus(9749, 251) == 10000

def test_minus():
    assert minus(100,50) == 50
    assert minus(50,100) == -50
    assert minus(100,100) == 0

def test_multiplicate():
    assert multiplicate(100,100) == 10000
    assert multiplicate(11,11) == 121
    assert multiplicate(11,0) == 0

def test_devide():
    try:
        assert devide(100, 10) == 10
        assert devide(100, 0) == "It's impossible to divide by zero."
        assert devide(0, 100) == 0
        assert devide(1000, 5) == 200
    except ZeroDivisionError:
        pass  # Expected ZeroDivisionError, do nothing
    else:
        assert False, "ZeroDivisionError not raised"

def test_square_root():
    assert square_root(100) == "√100 = 10.0"
    assert square_root(25) == "√25 = 5.0"
    assert square_root(64) == "√64 = 8.0"
if __name__ == "__main__":
    main()