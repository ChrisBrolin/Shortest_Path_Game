from car_temp import square_it
from pytest import approx

def test_square_it():
    assert approx(square_it(5.01), abs=0.001) == 25
