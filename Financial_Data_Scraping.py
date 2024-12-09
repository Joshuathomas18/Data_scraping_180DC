import pandas as pd
import requests
import os

def get_income_statement(ticker, limit, key, period):
    URL = f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period={period}&limit={limit}&apikey={key}'
    try:
        r = requests.get(URL)
        r.raise_for_status()  # Check if the request was successful
        print(f"Received Income Statement for {ticker}")
        income_statement = pd.DataFrame.from_dict(r.json())
        return income_statement
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError for {ticker}: {str(e)}")
        print(f"Response: {r.text}")  
    except Exception as e:
        print(f"Unexpected ERROR while requesting Income Statement for {ticker}: {str(e)}")

# (Other functions remain the same...)

if __name__ == "__main__":
    # Reading API key and ticker list
    try:
        # Check if the key.txt file exists
        if not os.path.exists('key.txt'):
            raise FileNotFoundError("API key file 'key.txt' not found.")
        
        # Load the API key
        key = pd.read_csv('key.txt', header=None)[0][0]
        
        # Check if the tickers.txt file exists
        if not os.path.exists('tickers.txt'):
            raise FileNotFoundError("Ticker list file 'tickers.txt' not found.")
        
        # Load the tickers from tickers.txt
        tickers = pd.read_csv('tickers.txt', header=None)[0]
        
        if tickers.empty:
            raise ValueError("The tickers list is empty. Please provide valid tickers in 'tickers.txt'.")
        
        print(f"API Key: {key}")
        print(f"Tickers: {tickers}")
    except FileNotFoundError as e:
        print(f"File not found: {str(e)}")
    except pd.errors.EmptyDataError:
        print("Error: 'tickers.txt' or 'key.txt' is empty.")
    except Exception as e:
        print(f"Error reading files: {str(e)}")
    
    # Check if 'tickers' was successfully defined
    if 'tickers' in locals():
        # Process each ticker
        for ticker in tickers:
            print(f"\nProcessing ticker: {ticker}")
            IS = get_income_statement(ticker=ticker, limit=6, key=key, period='annual')
            # ... (Other API calls and Excel writing steps remain the same) ...
    else:
        print("Error: 'tickers' is not defined. Please check the 'tickers.txt' file.")
