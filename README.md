# Option Pricing Web App

This project is a Flask-based web application that allows users to compute and visualize stock option prices using various models, including:
- Black-Scholes
- Binomial Tree
- Monte Carlo
- Bjerksund-Stensland

The goal is to highlight my development skills to have some fun and maybe, just maybe, make some money.

## Features
- Calculate stock option prices based on user inputs.
- Visualize option prices as a function of volatility, strike price, or time to maturity.
- Supports multiple pricing models.

## Prerequisites
- Python 3.x
- Flask
- Matplotlib
- NumPy
- SciPy
- yfinance

## Setup
1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/option_pricing_app.git
    ```

2. Navigate to the project directory:
    ```bash
    cd option_pricing_app
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables by creating a `.env` file:
    ```bash
    touch .env
    ```

   Inside the `.env` file, add the following:
    ```bash
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    ```

5. Run the app:
    ```bash
    python app.py
    ```

6. Access the web app on `http://127.0.0.1:5000`.

## License
This project is licensed under the MIT License.
