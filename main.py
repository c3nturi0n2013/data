import json
import subprocess
import pandas as pd
import yfinance as yf

# run this program to update the ETF stock prices to the latest price
# use: python3 main.py in the terminal to run this code
# it should update on the data git repo & on the bitcoinsprinkles.com site

def fetch_prices(tickers):
    """Fetch the latest prices for ETFs using yfinance."""
    # Ensure tickers are a list for the download method
    ticker_list = list(tickers.values())
    data = yf.download(ticker_list, period="1d")['Close']
    # If data is fetched for only one day, it returns a Series instead of DataFrame:
    if isinstance(data, pd.Series):
        data = pd.DataFrame(data).T
    # Extract the last close prices for each ticker and format to two decimal places
    prices = {ticker: f"{data.iloc[-1][ticker]:.2f}" for ticker in ticker_list}
    return prices

def update_etf_price(file_path, new_prices):
    # Load the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Update prices in the JSON object
    data['GBTC']['price'] = new_prices['GBTC']
    data['IBIT']['price'] = new_prices['IBIT']
    data['FBTC']['price'] = new_prices['FBTC']

    # Write the updated JSON back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    # Git commands to add, commit, and push the changes
    try:
        subprocess.run(['git', 'add', file_path], check=True)
        subprocess.run(['git', 'commit', '-m', 'Updated ETF prices'], check=True)
        subprocess.run(['git', 'push'], check=True)
        print("Successfully updated the repository.")
    except subprocess.CalledProcessError as e:
        print("Failed to update repository:", e)

# Example usage:
etf_tickers = {
    'GBTC': 'GBTC',  # You would replace this with the actual ticker if different
    'IBIT': 'IBIT',  # You would replace this with the actual ticker if different
    'FBTC': 'FBTC'   # You would replace this with the actual ticker if different
}

new_prices = fetch_prices(etf_tickers)  # Fetch new prices

file_path = './btcetf.json'  # Change to the correct path
update_etf_price(file_path, new_prices)
