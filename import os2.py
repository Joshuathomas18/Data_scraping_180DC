import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from sec_edgar_downloader import Downloader
from bs4 import BeautifulSoup

# Step 1: Download 10-K filings
downloader = Downloader()
ticker_symbol = 'AAPL'  # Example: Apple Inc.
downloader.get("10-K", ticker_symbol, amount=5)  # Download the last 5 filings

# Step 2: Extract financial data from the filings
def extract_financial_data(filing_path):
    with open(filing_path, 'r', encoding='utf-8') as file:
        filing_content = file.read()
    
    soup = BeautifulSoup(filing_content, 'html.parser')
    
    # Extracting revenue and net income using regex (this may vary based on filing format)
    revenue_pattern = r'Revenue.*?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)'
    net_income_pattern = r'Net Income.*?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)'
    
    revenue_matches = re.findall(revenue_pattern, filing_content)
    net_income_matches = re.findall(net_income_pattern, filing_content)
    
    # Convert extracted values to float and remove commas
    revenues = [float(revenue.replace(',', '').strip()) for revenue in revenue_matches]
    net_incomes = [float(net_income.replace(',', '').strip()) for net_income in net_income_matches]
    
    return revenues, net_incomes

# Collecting data from all downloaded filings
financial_data = []
for filename in os.listdir(f"sec_edgar_filings/{ticker_symbol}/10-K/"):
    if filename.endswith('.html'):
        revenues, net_incomes = extract_financial_data(os.path.join(f"sec_edgar_filings/{ticker_symbol}/10-K/", filename))
        financial_data.append({'Revenue': revenues[0], 'Net Income': net_incomes[0]})

# Step 3: Create a DataFrame
df = pd.DataFrame(financial_data)

# Adding years based on the number of filings (this assumes the most recent filing is the latest year)
df['Year'] = pd.date_range(end=pd.Timestamp.now(), periods=len(df), freq='Y').year

# Step 4: Calculate Year-over-Year Growth Rates
df['Revenue Growth'] = df['Revenue'].pct_change() * 100
df['Net Income Growth'] = df['Net Income'].pct_change() * 100

# Step 5: Visualize Financial Metrics Over Time
plt.figure(figsize=(12, 6))

# Plot Revenue and Net Income
plt.subplot(2, 1, 1)
plt.plot(df['Year'], df['Revenue'], marker='o', label='Revenue', color='blue')
plt.plot(df['Year'], df['Net Income'], marker='o', label='Net Income', color='green')
plt.title('Financial Metrics Over Time')
plt.ylabel('Amount ($)')
plt.xticks(df['Year'])
plt.legend()
plt.grid()

# Plot Growth Rates
plt.subplot(2, 1, 2)
plt.plot(df['Year'], df['Revenue Growth'], marker='o', label='Revenue Growth (%)', color='orange')
plt.plot(df['Year'], df['Net Income Growth'], marker='o', label='Net Income Growth (%)', color='red')
plt.ylabel('Growth Rate (%)')
plt.xlabel('Year')
plt.xticks(df['Year'])
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()