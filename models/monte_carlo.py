def monte_carlo(S, K, T, r, sigma, simulations, option_type='call'):
    """
    Monte Carlo simulation to calculate option prices
    S: Stock price
    K: Strike price
    T: Time to maturity (in years)
    r: Risk-free rate
    sigma: Volatility
    simulations: Number of Monte Carlo simulations
    option_type: 'call' or 'put'
    """
    dt = T
    price_paths = np.zeros(simulations)
    for i in range(simulations):
        rand = np.random.normal(0, 1)
        stock_price = S * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * rand)
        if option_type == 'call':
            price_paths[i] = np.maximum(0, stock_price - K)
        elif option_type == 'put':
            price_paths[i] = np.maximum(0, K - stock_price)

    # Discounted average of the simulated payoffs
    return np.exp(-r * T) * np.mean(price_paths)
