# Option Pricing Web App

This Flask application calculates and visualizes option prices using several pricing models. It now features a Bootstrap based interface and can display option Greeks.

## Features
- Black-Scholes, Binomial Tree, Monte Carlo and Bjerksund‑Stensland models
- Interactive volatility visualization
- Calculation of Greeks (Delta, Gamma, Vega, Theta, Rho)

## Architecture

The application is driven by a small Flask server (`app.py`). Pricing logic is
implemented in individual modules within `models/` and accessed via helper
functions in `services.py`. HTML templates and static assets live under
`templates/` and `static/`.

## Setup

Create a virtual environment with Python 3.11 or newer and install the
dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

## Running Tests

Execute the unit tests with `pytest`:

```bash
pytest
```

Tests cover all pricing models and a simple check of the Flask `/calculate`
route.

## Docker
Run the app in a container:
```bash
docker build -t option-app .
docker run -p 5000:5000 option-app
```

## License
MIT
