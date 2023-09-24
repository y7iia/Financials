import streamlit as st
import pandas as pd
import yfinance as yf
import logging

# Configure logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Function to fetch financial data
def fetch_financial_data(ticker, financial_type, frequency):
    try:
        t = yf.Ticker(ticker)
        if financial_type == 'income statement':
            data = t.financials if frequency == 'yearly' else t.quarterly_financials
        elif financial_type == 'balance sheet':
            data = t.balance_sheet if frequency == 'yearly' else t.quarterly_balance_sheet
        elif financial_type == 'cash flow':
            data = t.cashflow if frequency == 'yearly' else t.quarterly_cashflow
        else:
            logging.error(f"Invalid financial type: {financial_type}")
            return None

        return data.iloc[:, 0:1]
    except Exception as e:
        logging.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

def aggregate_financial_data(tickers, financial_type, frequency):
    # Empty dictionary to store data
    data = {}

    # Loop over tickers
    for ticker in tickers:
        ticker_data = fetch_financial_data(ticker, financial_type, frequency)
        if ticker_data is not None:
            data[ticker] = ticker_data

    # Combine all data into a single DataFrame and transpose
    try:
        df = pd.concat(data, axis=1).T
        df = df.reset_index(level=1, drop=True)  # Remove the date index
    except Exception as e:
        logging.error(f"Error processing data: {str(e)}")
        return None

    return df

# TASI dictionary (example)
tasi = {
    "Technology": ["AAPL", "MSFT"],
    "Healthcare": ["JNJ", "PFE"],
    "Consumer Discretionary": ["AMZN", "MCD"],
    # Add more sectors and their companies...
}

st.title('Financial Data Fetcher')

# Dropdown for selecting the sector
selected_sector = st.selectbox('Select sector', list(tasi.keys()))

# Dropdown for selecting the financial type
financial_type = st.selectbox('Enter financial type', ['income statement', 'balance sheet', 'cash flow'])

# Dropdown for selecting the frequency
frequency = st.selectbox('Enter frequency', ['yearly', 'quarterly'])

# Button for submitting the input
if st.button("Fetch Data"):
    # Get the list of tickers for the selected sector
    tickers = tasi[selected_sector]

    # Fetch data
    df = aggregate_financial_data(tickers, financial_type, frequency)

    # Display data
    if df is not None:
        df.index.names = ['Ticker']
        # df = df.rename(index=companies)
        df = df.round(2)  # Round all numbers in the DataFrame to 2 decimal places
        df = df.div(1000000)  # Divide all numbers in the DataFrame by 1,000,000

        st.write(df.T)
    else:
        st.error("Unable to fetch data.")
