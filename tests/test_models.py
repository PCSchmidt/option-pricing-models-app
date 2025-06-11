import math
from models.black_scholes import black_scholes

def test_black_scholes_call():
    price = black_scholes(100, 100, 1, 0.05, 0.2, 'call')
    assert math.isclose(price, 10.4506, rel_tol=1e-4)
