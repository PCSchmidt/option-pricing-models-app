def binomial_tree(S, K, T, r, sigma, steps, option_type='call'):
    """
    Binomial tree model to calculate option prices
    S: Stock price
    K: Strike price
    T: Time to maturity (in years)
    r: Risk-free rate
    sigma: Volatility
    steps: Number of time steps in the binomial tree
    option_type: 'call' or 'put'
    """
    dt = T / steps  # Time step size
    u = np.exp(sigma * np.sqrt(dt))  # Up factor
    d = 1 / u  # Down factor
    p = (np.exp(r * dt) - d) / (u - d)  # Risk-neutral probability

    # Create a binomial price tree
    prices = np.zeros(steps + 1)
    for i in range(steps + 1):
        prices[i] = S * (u ** (steps - i)) * (d ** i)

    # Create the option value tree
    option_values = np.zeros(steps + 1)
    if option_type == 'call':
        option_values = np.maximum(prices - K, 0)
    elif option_type == 'put':
        option_values = np.maximum(K - prices, 0)

    # Work backwards through the tree
    for i in range(steps - 1, -1, -1):
        for j in range(i + 1):
            option_values[j] = (p * option_values[j] + (1 - p) * option_values[j + 1]) * np.exp(-r * dt)

    return option_values[0]
