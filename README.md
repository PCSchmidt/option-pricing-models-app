# Option Pricing Web App

This Flask application calculates and visualizes option prices using several pricing models. It now features a Bootstrap based interface and can display option Greeks.

## Features
- Black-Scholes, Binomial Tree, Monte Carlo and Bjerksund‑Stensland models
- Interactive volatility visualization
- Calculation of Greeks (Delta, Gamma, Vega, Theta, Rho)

## Setup
```bash
pip install -r requirements.txt
python app.py
```
Visit `http://127.0.0.1:5000`.

## Docker
Run the app in a container:
```bash
docker build -t option-app .
docker run -p 5000:5000 option-app
```

## License
MIT
