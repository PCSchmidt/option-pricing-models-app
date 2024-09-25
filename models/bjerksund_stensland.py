def bjerksund_stensland(S, K, T, r, sigma, option_type='call'):
    """
    Bjerksund-Stensland approximation to calculate American option prices
    S: Stock price
    K: Strike price
    T: Time to maturity (in years)
    r: Risk-free rate
    sigma: Volatility
    option_type: 'call' or 'put'
    """
    # Simplified implementation for educational purposes
    if option_type == 'call':
        return black_scholes(S, K, T, r, sigma, option_type)  # Placeholder for approximation
    elif option_type == 'put':
        return black_scholes(S, K, T, r, sigma, option_type)  # Placeholder for approximation
