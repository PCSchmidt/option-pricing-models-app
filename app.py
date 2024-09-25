from flask import Flask, render_template, request
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Visualization route
@app.route('/visualize', methods=['POST'])
def visualize():
    # Extract input from form
    symbol = request.form['symbol']
    strike_price = float(request.form['strike_price'])
    option_type = request.form['option_type']
    volatility = float(request.form['volatility']) / 100  # Convert percentage to decimal
    risk_free_rate = float(request.form['risk_free_rate']) / 100
    model_type = request.form['model_type']
    steps = int(request.form['steps']) if 'steps' in request.form else 100
    simulations = int(request.form['simulations']) if 'simulations' in request.form else 10000

    # Get stock data
    stock = yf.Ticker(symbol)
    stock_price = stock.history(period='1d')['Close'][0]

    # Choose a parameter to vary for the visualization (e.g., volatility)
    x_vals = np.linspace(0.01, 1.0, 50)  # Volatility from 1% to 100%
    option_prices = []

    # Calculate option prices for different volatility levels
    for sigma in x_vals:
        if model_type == 'black_scholes':
            price = black_scholes(stock_price, strike_price, 1, risk_free_rate, sigma, option_type)
        elif model_type == 'binomial_tree':
            price = binomial_tree(stock_price, strike_price, 1, risk_free_rate, sigma, steps, option_type)
        elif model_type == 'monte_carlo':
            price = monte_carlo(stock_price, strike_price, 1, risk_free_rate, sigma, simulations, option_type)
        elif model_type == 'bjerksund_stensland':
            price = bjerksund_stensland(stock_price, strike_price, 1, risk_free_rate, sigma, option_type)
        option_prices.append(price)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals * 100, option_prices, label=model_type.capitalize())
    plt.title(f"Option Price vs. Volatility ({model_type.capitalize()})")
    plt.xlabel('Volatility (%)')
    plt.ylabel('Option Price')
    plt.legend()

    # Save plot to a string buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Render the image in the result page
    return render_template('visualize_result.html', plot_url=plot_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Extract input from form
    symbol = request.form['symbol']
    strike_price = float(request.form['strike_price'])
    option_type = request.form['option_type']
    maturity = float(request.form['maturity'])
    volatility = float(request.form['volatility']) / 100  # Convert percentage to decimal
    risk_free_rate = float(request.form['risk_free_rate']) / 100
    model_type = request.form['model_type']
    steps = int(request.form['steps']) if 'steps' in request.form else 100
    simulations = int(request.form['simulations']) if 'simulations' in request.form else 10000

    # Get stock data
    stock = yf.Ticker(symbol)
    stock_price = stock.history(period='1d')['Close'][0]

    # Compute option price based on selected model
    if model_type == 'black_scholes':
        option_price = black_scholes(stock_price, strike_price, maturity, risk_free_rate, volatility, option_type)
    elif model_type == 'binomial_tree':
        option_price = binomial_tree(stock_price, strike_price, maturity, risk_free_rate, volatility, steps, option_type)
    elif model_type == 'monte_carlo':
        option_price = monte_carlo(stock_price, strike_price, maturity, risk_free_rate, volatility, simulations, option_type)
    elif model_type == 'bjerksund_stensland':
        option_price = bjerksund_stensland(stock_price, strike_price, maturity, risk_free_rate, volatility, option_type)
    else:
        option_price = "Invalid model selected."

    return render_template('result.html', option_price=option_price, stock_price=stock_price)
