import io
import base64
import logging

import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from flask import Flask, render_template, request

from services import calculate_price, calculate_greeks

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/visualize', methods=['POST'])
def visualize():
    """Visualize option price against volatility using the chosen model."""
    try:
        symbol = request.form['symbol']
        strike_price = float(request.form['strike_price'])
        option_type = request.form['option_type']
        volatility = float(request.form['volatility']) / 100
        risk_free_rate = float(request.form['risk_free_rate']) / 100
        model_type = request.form['model_type']
        steps = int(request.form.get('steps', 100))
        simulations = int(request.form.get('simulations', 10000))

        stock = yf.Ticker(symbol)
        stock_price = stock.history(period='1d')['Close'][0]

        x_vals = np.linspace(0.01, 1.0, 50)
        option_prices = [
            calculate_price(model_type, stock_price, strike_price, 1, risk_free_rate, sigma,
                             option_type, steps, simulations)
            for sigma in x_vals
        ]

        fig = plt.figure(figsize=(10, 6))
        plt.plot(x_vals * 100, option_prices, label=model_type.capitalize())
        plt.title(f"Option Price vs. Volatility ({model_type.capitalize()})")
        plt.xlabel('Volatility (%)')
        plt.ylabel('Option Price')
        plt.legend()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        return render_template('visualize_result.html', plot_url=plot_url)
    except Exception as exc:
        logger.exception("Visualization failed")
        return f"Error: {exc}", 400


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate option price and Greeks."""
    try:
        symbol = request.form['symbol']
        strike_price = float(request.form['strike_price'])
        option_type = request.form['option_type']
        maturity = float(request.form['maturity'])
        volatility = float(request.form['volatility']) / 100
        risk_free_rate = float(request.form['risk_free_rate']) / 100
        model_type = request.form['model_type']
        steps = int(request.form.get('steps', 100))
        simulations = int(request.form.get('simulations', 10000))

        stock = yf.Ticker(symbol)
        stock_price = stock.history(period='1d')['Close'][0]

        option_price = calculate_price(model_type, stock_price, strike_price, maturity,
                                       risk_free_rate, volatility, option_type,
                                       steps, simulations)
        greeks = calculate_greeks(stock_price, strike_price, maturity,
                                  risk_free_rate, volatility, option_type)

        return render_template('result.html', option_price=option_price,
                               stock_price=stock_price, greeks=greeks)
    except Exception as exc:
        logger.exception("Calculation failed")
        return f"Error: {exc}", 400


if __name__ == '__main__':
    app.run(debug=True)
