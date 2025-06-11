"""Service layer for option pricing and Greeks."""

import logging
from typing import Dict

import numpy as np

from models.black_scholes import black_scholes, black_scholes_greeks
from models.binomial_tree import binomial_tree
from models.monte_carlo import monte_carlo
from models.bjerksund_stensland import bjerksund_stensland

logger = logging.getLogger(__name__)


def calculate_price(model: str, S: float, K: float, T: float, r: float, sigma: float,
                     option_type: str, steps: int = 100, simulations: int = 10000) -> float:
    """Return option price using the selected model."""
    logger.debug("Calculating price using %s", model)
    if model == 'black_scholes':
        return black_scholes(S, K, T, r, sigma, option_type)
    if model == 'binomial_tree':
        return binomial_tree(S, K, T, r, sigma, steps, option_type)
    if model == 'monte_carlo':
        return monte_carlo(S, K, T, r, sigma, simulations, option_type)
    if model == 'bjerksund_stensland':
        return bjerksund_stensland(S, K, T, r, sigma, option_type)
    raise ValueError(f"Unknown model {model}")


def calculate_greeks(S: float, K: float, T: float, r: float, sigma: float,
                     option_type: str) -> Dict[str, float]:
    """Return option Greeks using the Black-Scholes formula."""
    return black_scholes_greeks(S, K, T, r, sigma, option_type)
