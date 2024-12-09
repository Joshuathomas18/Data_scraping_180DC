"""
This is a script that will scrape financial information using the
FinancialModelingPrep API.
Website: https://financialmodelingprep.com/developer/
Free plan with 250 requests per day.

Includes: 
    - Income Statements 
    - Balance Sheets 
    - Cash Flow Statements 
    - Financial Ratios 
    - Key Metrics 
    - Daily Prices 
    - Enterprise Value

Parameter specification:
    - ticker: Company stock name (e.g., AAPL for Apple)
    - limit: Number of records you'd like (e.g., for annual, 6 will give 6 years)
    - key: API key generated from the Financial Modeling Prep account
    - period: 'annual' or 'quarter'
"""
import Financial_Data_Scraping as fds
import pandas as pd

if __name__ == "__main__":
    """Running the scraper to obtain financial data."""

    # Load API key from a file
    key = pd.read_csv('key.txt', header=None)[0][0]

    # Load list of tickers from a file
    tickers = pd.read_csv('tickers.txt', header=None)[0]

    # Loop through each ticker to scrape data
    for ticker in tickers:
        print(f"Starting scraping for: {ticker}")

        # Scrape financial data using the custom module 'Financial_Data_Scraping'
        IS = fds.get_income_statement(ticker=ticker, limit=6, key=key, period='annual')
        BS = fds.get_balance_sheet(ticker=ticker, limit=6, key=key, period='annual')
        CF = fds.get_cash_flow_statement(ticker=ticker, limit=6, key=key, period='annual')
        FR = fds.get_financial_ratios(ticker=ticker, limit=6, key=key, period='annual')
        KM = fds.get_key_metrics(ticker=ticker, limit=6, key=key, period='annual')
        P = fds.get_daily_prices(ticker=ticker, timeseries=5 * 261, key=key)  # 5 years of daily prices
        EV = fds.get_enterprise_value(ticker=ticker, rate=5 * 261, key=key, period='annual')  # 5 years of enterprise value

        # Creating an Excel writer object to save data to an Excel file
        writer = pd.ExcelWriter(f'{ticker}.xlsx', engine='xlsxwriter')

        # Write data to separate sheets within the Excel file
        IS.to_excel(writer, sheet_name='Income Statement')
        BS.to_excel(writer, sheet_name='Balance Sheet Statement')
        CF.to_excel(writer, sheet_name='Cash Flow Statement')
        FR.to_excel(writer, sheet_name='Financial Ratios')
        KM.to_excel(writer, sheet_name='Key Metrics')
        P.to_excel(writer, sheet_name='Daily Prices')
        EV.to_excel(writer, sheet_name='Enterprise Value')

        # Save the Excel file
        writer.save()

        print(f'Finished scraping for: {ticker}')

    print("All tickers processed.")
