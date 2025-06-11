import numpy as np
from scipy.stats import norm
from .black_scholes import black_scholes


def _phi(S, T, gamma, H, I, r, b, sigma):
    lamb = -r * T + gamma * b * T + 0.5 * gamma * (gamma - 1) * sigma ** 2 * T
    d = -(np.log(S / H) + (b + (gamma - 0.5) * sigma ** 2) * T) / (sigma * np.sqrt(T))
    kappa = 2 * b / sigma ** 2 + (2 * gamma - 1)
    return np.exp(lamb) * S ** gamma * (
        norm.cdf(d) - (I / S) ** kappa * norm.cdf(d - 2 * np.log(I / S) / (sigma * np.sqrt(T)))
    )


def _d2(S, K, T, r, b, sigma):
    d1 = (np.log(S / K) + (b + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return d1 - sigma * np.sqrt(T)


def bjerksund_stensland(S, K, T, r, sigma, option_type='call', q=0.0):
    """Approximate American option price using the Bjerksund-Stensland method."""
    b = r - q
    if option_type == 'call':
        if b >= r:
            return black_scholes(S, K, T, r, sigma, 'call')
        beta = 0.5 - b / sigma ** 2 + np.sqrt((b / sigma ** 2 - 0.5) ** 2 + 2 * r / sigma ** 2)
        B_inf = beta / (beta - 1) * K
        B0 = max(K, r / (r - b) * K)
        h = -(b * T + 2 * sigma * np.sqrt(T)) * B0 / (B_inf - B0)
        I = B0 + (B_inf - B0) * (1 - np.exp(h))
        alpha = (I - K) * I ** (-beta)
        if S >= I:
            return S - K
        return (
            alpha * S ** beta
            - alpha * _phi(S, T, beta, I, I, r, b, sigma)
            + _phi(S, T, 1, I, I, r, b, sigma)
            - _phi(S, T, 1, K, I, r, b, sigma)
            - K * np.exp(-r * T) * norm.cdf(_d2(S, K, T, r, b, sigma))
            + S * np.exp((b - r) * T) * norm.cdf(_d2(S, K, T, r, b, sigma) - sigma * np.sqrt(T))
        )
    else:
        call_price = bjerksund_stensland(S, K, T, r, sigma, 'call', q)
        return call_price - S + K * np.exp(-r * T)


