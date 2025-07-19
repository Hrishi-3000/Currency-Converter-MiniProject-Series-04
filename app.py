from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = "fca_live_owp1mtFEfMngqk3GzxTp9KBG3WdaDkdLhAO7YezH"  # Your API key
BASE_URL = "https://api.freecurrencyapi.com/v1"

# Predefined list of common currencies (since the free plan doesn't include /currencies endpoint)
COMMON_CURRENCIES = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "JPY": "Japanese Yen",
    "GBP": "British Pound",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "INR": "Indian Rupee",
    "BRL": "Brazilian Real",
    "MXN": "Mexican Peso",
    "SGD": "Singapore Dollar",
    "KRW": "South Korean Won",
    "RUB": "Russian Ruble",
    "ZAR": "South African Rand"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            from_currency = request.form['from_currency']
            to_currency = request.form['to_currency']
            
            # Get conversion rate
            url = f"{BASE_URL}/latest?apikey={API_KEY}&base_currency={from_currency}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    rate = data['data'].get(to_currency)
                    if rate:
                        converted_amount = amount * rate
                        return render_template('index.html', 
                                            converted_amount=converted_amount,
                                            amount=amount,
                                            from_currency=from_currency,
                                            to_currency=to_currency,
                                            currencies=COMMON_CURRENCIES)
        
            error = "Error converting currencies. Please try again."
            return render_template('index.html', 
                                 error=error,
                                 currencies=COMMON_CURRENCIES)
        
        except ValueError:
            error = "Please enter a valid number"
            return render_template('index.html', 
                                error=error,
                                currencies=COMMON_CURRENCIES)
    
    # For GET request or initial load
    return render_template('index.html', currencies=COMMON_CURRENCIES)

if __name__ == '__main__':
    app.run(debug=True)