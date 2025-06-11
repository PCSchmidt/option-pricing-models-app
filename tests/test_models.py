import math
import numpy as np
import pytest
from flask import Flask

from models.black_scholes import black_scholes
from models.binomial_tree import binomial_tree
from models.monte_carlo import monte_carlo
from models.bjerksund_stensland import bjerksund_stensland
from app import app
from unittest.mock import patch


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_black_scholes_call():
    price = black_scholes(100, 100, 1, 0.05, 0.2, 'call')
    assert math.isclose(price, 10.4506, rel_tol=1e-4)


def test_binomial_tree_put():
    price = binomial_tree(100, 100, 1, 0.05, 0.2, 100, 'put')
    assert math.isclose(price, 5.5536, rel_tol=1e-2)


def test_monte_carlo_put_seeded():
    np.random.seed(0)
    price = monte_carlo(100, 100, 1, 0.05, 0.2, 50000, 'put')
    assert math.isclose(price, 5.53, rel_tol=5e-2)


def test_bjerksund_equals_black_scholes_call():
    price = bjerksund_stensland(100, 100, 1, 0.05, 0.2, 'call')
    bs_price = black_scholes(100, 100, 1, 0.05, 0.2, 'call')
    assert math.isclose(price, bs_price, rel_tol=1e-8)


def test_calculate_route(client):
    class DummyTicker:
        def history(self, period='1d'):
            import pandas as pd
            return pd.DataFrame({'Close': [150.0]})

    with patch('yfinance.Ticker', return_value=DummyTicker()):
        response = client.post('/calculate', data={
            'symbol': 'AAPL',
            'strike_price': '100',
            'maturity': '1',
            'option_type': 'call',
            'volatility': '20',
            'risk_free_rate': '5',
            'model_type': 'black_scholes',
            'steps': '100',
            'simulations': '1000',
        })
    assert response.status_code == 200



