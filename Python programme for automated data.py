import sqlite3
import pandas as pd
import yfinance as yf

# 1. Define the Indian stock tickers (NSE)
tickers = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'SBIN.NS']

# 2. Connect to SQLite database (creates 'indian_stocks.db' automatically in the same folder)
conn = sqlite3.connect('indian_stocks.db')

print('Starting data download...')

# 3. Fetch data for each stock and store it in SQLite
for ticker in tickers:
  print(f'Fetching data for {ticker}...')

  # Download 1 year of historical end-of-day data
  df = yf.download(ticker, period='1y', progress=False)

  # Reset index so the 'Date' becomes a regular column
  df = df.reset_index()

  # Flatten multi-level headers if present
  if isinstance(df.columns, pd.MultiIndex):
    df.columns = [col[0] for col in df.columns]

  # Clean column names (lowercase, remove spaces)
  df.columns = [str(col).lower().replace(' ', '_') for col in df.columns]

  # Add ticker column
  df['ticker'] = ticker

  # Write the rows into the 'stock_prices' table inside SQLite
  df.to_sql('stock_prices', conn, if_exists='append', index=False)

# 4. Save and close connection
conn.close()

print('\nSuccess! All stock data has been stored in indian_stocks.db')
