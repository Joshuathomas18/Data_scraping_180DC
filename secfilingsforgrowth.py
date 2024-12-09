# -*- coding: utf-8 -*-
"""
SEC Filing Scraper
@author: AdamGetbags
"""

# import modules
import requests
import pandas as pd
import matplotlib.pyplot as plt

# create request header
headers = {'User-Agent': "email@address.com"}

# get all companies data from SEC
company_tickers_url = "https://www.sec.gov/files/company_tickers.json"
company_tickers_response = requests.get(company_tickers_url, headers=headers)

# format response to dictionary and get first key/value
company_tickers_dict = company_tickers_response.json()
first_entry = company_tickers_dict['0']

# parse CIK without leading zeros
direct_cik = first_entry['cik_str']

# dictionary to dataframe
company_data = pd.DataFrame.from_dict(company_tickers_dict, orient='index')

# add leading zeros to CIK
company_data['cik_str'] = company_data['cik_str'].astype(str).str.zfill(10)

# review first entry
print(company_data.head(1))

# Get the first company's CIK
cik = company_data.iloc[0]['cik_str']

# get company specific filing metadata from SEC's EDGAR API
filing_metadata_url = f'https://data.sec.gov/submissions/CIK{cik}.json'
filing_metadata_response = requests.get(filing_metadata_url, headers=headers)

# review keys
filing_metadata_json = filing_metadata_response.json()
print(filing_metadata_json.keys())

# parse filings
filings = filing_metadata_json['filings']['recent']

# dictionary to dataframe
all_forms = pd.DataFrame.from_dict(filings)

# review columns and extract specific filing metadata
print(all_forms[['accessionNumber', 'reportDate', 'form']].head(50))

# Example: get metadata for 10-Q filings
form_10q_metadata = all_forms[all_forms['form'] == '10-Q']
print(form_10q_metadata.head())

# get company facts data (e.g., stock shares outstanding)
company_facts_url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
company_facts_response = requests.get(company_facts_url, headers=headers)

# parse facts
company_facts_json = company_facts_response.json()
print(company_facts_json['facts'].keys())

# example: get stock shares outstanding
stock_shares_outstanding = company_facts_json['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'][0]
print(stock_shares_outstanding)

# get company concept data (e.g., Assets from filings)
company_concept_url = f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/Assets.json'
company_concept_response = requests.get(company_concept_url, headers=headers)

# parse concept data
company_concept_json = company_concept_response.json()
assets_data = pd.DataFrame.from_dict(company_concept_json['units']['USD'])

# filter assets data for 10-Q forms and reset index
assets_10k = assets_data[assets_data['form'] == '10-K'].reset_index(drop=True)

# plot assets over time for 10-Q filings
assets_10k.plot(x='end', y='val', kind='line', title='Assets (10-K) Over Time')
plt.xlabel('Filing Date')
plt.ylabel('Assets (USD)')
plt.show()
