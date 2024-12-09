import os
from bs4 import BeautifulSoup
import pandas as pd

# Function to extract financial data from a filing
def extract_financial_data(filing_path):
    with open(filing_path, 'r') as file:
        filing_content = file.read()
    
    soup = BeautifulSoup(filing_content, 'html.parser')
    
    # Example: Extracting revenue and net income
    revenue = soup.find(text="Revenue").find_next('td').get_text()
    net_income = soup.find(text="Net Income").find_next('td').get_text()
    
    return {
        'Revenue': float(revenue.replace(',', '').strip()),
        'Net Income': float(net_income.replace(',', '').strip())
    }

# Collect data from all downloaded filings
financial_data = []
for filename in os.listdir(filing_path):
    if filename.endswith('.html'):
        data = extract_financial_data(os.path.join(filing_path, filename))
        financial_data.append(data)

# Create DataFrame
df = pd.DataFrame(financial_data)