import streamlit as st
import pandas as pd
import yfinance as yf
import logging

# Configure logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Create a dictionary of sector to ticker symbols
tasi = {
    'الطاقة': ['4030.SR', '2222.SR', '2382.SR', '4200.SR', '2381.SR', '2030.SR'],
    'البتروكيماويات': ['2250.SR', '2310.SR', '2060.SR', '2170.SR', '2330.SR', '2010.SR', '2380.SR', '2210.SR', '2001.SR', '2020.SR', '2290.SR', '2350.SR'],
}

# Create a dictionary of ticker symbols to company names
companies = {
    '1010.SR': 'الرياض',
    '1020.SR': 'الجزيرة',
}

# Dictionary for converting financial ratio names to Arabic
ratio_translation = {
    'Stock Price': 'سعر السهم',
    'Current Ratio': 'نسبة التداول',
    'Quick Ratio': 'نسبة السيولة السريعة',
    'Debt-to-Equity Ratio': 'نسبة الدين إلى حقوق الملكية',
    'ROE': 'العائد على حقوق الملكية',
    'P/E Ratio': 'مكرر الأرباح',
    'Book Value, M$': 'حقوق المساهمين، مليون دولار',
    'BV Multiple': 'مضاعف القيمة الدفترية',
    'Number of Shares, M': 'عدد الأسهم، مليون',
    'Market Cap, B$': 'القيمة السوقية، مليار دولار',
    'Book Value per Share': 'القيمة الدفترية لكل سهم',
    'EPS': 'ربحية السهم',
    'Dividend Payout Ratio': 'نسبة توزيع الأرباح',
    'Operating Cash Flow Ratio': 'نسبة التدفق النقدي التشغيلي',
    'Free Cash Flow, M$': 'التدفق النقدي الحر، مليون دولار',
    'Profit Margins': 'هامش الربحية',
    'PEG Ratio': 'نسبة PEG',
    'Float Shares, M': 'الأسهم الحرة، مليون'
}

# Function to calculate financial ratios for a single company
def calculate_financial_ratios(ticker):
    company = yf.Ticker(ticker)
    ratios = {}
    try:
        # Fetch balance sheet, financials, cash flow, and stock info
        balance_sheet = company.balance_sheet
        financials = company.financials
        cash_flow = company.cashflow
        stock_info = company.info

        # Fetch current stock price
        current_price = company.history(period="1d")['Close'].iloc[-1]

        try:
            shares_outstanding = stock_info.get('sharesOutstanding', "-")
            ratios['Number of Shares, M'] = shares_outstanding / 1_000_000
        except Exception as e:
            print(f"Error calculating Number of Shares for {ticker}: {e}")
            ratios['Number of Shares, M'] = "-"

        # Calculate financial ratios with exception handling
        try:
            current_assets = balance_sheet.loc['Current Assets'][0]
            current_liabilities = balance_sheet.loc['Current Liabilities'][0]
            ratios['Current Ratio'] = current_assets / current_liabilities
        except Exception as e:
            print(f"Error calculating Current Ratio for {ticker}: {e}")
            ratios['Current Ratio'] = "-"

        try:
            cash_and_equivalents = balance_sheet.loc['Cash And Cash Equivalents'][0]
            ratios['Quick Ratio'] = (cash_and_equivalents + balance_sheet.loc['Receivables'][0]) / current_liabilities
        except Exception as e:
            print(f"Error calculating Quick Ratio for {ticker}: {e}")
            ratios['Quick Ratio'] = "-"

        try:
            total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest'][0]
            total_equity = balance_sheet.loc['Stockholders Equity'][0]
            ratios['Debt-to-Equity Ratio'] = total_liabilities / total_equity
        except Exception as e:
            print(f"Error calculating Debt-to-Equity Ratio for {ticker}: {e}")
            ratios['Debt-to-Equity Ratio'] = "-"

        try:
            net_income = financials.loc['Net Income'][0]
            ratios['ROE'] = net_income / total_equity
        except Exception as e:
            print(f"Error calculating ROE for {ticker}: {e}")
            ratios['ROE'] = "-"

        try:
            ratios['P/E Ratio'] = stock_info.get('trailingPE', "-")
        except Exception as e:
            print(f"Error calculating P/E Ratio for {ticker}: {e}")
            ratios['P/E Ratio'] = "-"

        try:
            if 'Stockholders Equity' in balance_sheet.index:
                total_equity = balance_sheet.loc['Stockholders Equity'][0]
                ratios['Book Value, M$'] = total_equity / 1_000_000
            else:
                print(f"Stockholders Equity not found in balance sheet for {ticker}")
                ratios['Book Value, M$'] = "-"
        except Exception as e:
            print(f"Error calculating Book Value for {ticker}: {e}")
            ratios['Book Value, M$'] = "-"

        try:
            market_cap = stock_info.get('marketCap', "-")
            ratios['BV Multiple'] = market_cap / total_equity if total_equity != 0 else "-"
        except Exception as e:
            print(f"Error calculating BV Multiple for {ticker}: {e}")
            ratios['BV Multiple'] = "-"

        try:
            shares_outstanding = stock_info.get('sharesOutstanding', "-")
            ratios['Number of Shares, M'] = shares_outstanding / 1_000_000
        except Exception as e:
            print(f"Error calculating Number of Shares for {ticker}: {e}")
            ratios['Number of Shares, M'] = "-"

        try:
            ratios['Stock Price'] = current_price
        except Exception as e:
            print(f"Error calculating Stock Price for {ticker}: {e}")
            ratios['Stock Price'] = "-"

        try:
            ratios['Market Cap, B$'] = market_cap / 1_000_000_000
        except Exception as e:
            print(f"Error calculating Market Cap for {ticker}: {e}")
            ratios['Market Cap, B$'] = "-"

        try:
            ratios['Book Value per Share'] = total_equity / shares_outstanding
        except Exception as e:
            print(f"Error calculating Book Value per Share for {ticker}: {e}")
            ratios['Book Value per Share'] = "-"

        try:
            diluted_eps = financials.loc['Diluted EPS'][0]
            ratios['EPS'] = diluted_eps
        except Exception as e:
            print(f"Error calculating EPS for {ticker}: {e}")
            ratios['EPS'] = "-"

        try:
            dividends_paid = cash_flow.loc['Cash Dividends Paid'][0]
            ratios['Dividend Payout Ratio'] = dividends_paid / net_income
        except Exception as e:
            print(f"Error calculating Dividend Payout Ratio for {ticker}: {e}")
            ratios['Dividend Payout Ratio'] = "-"

        try:
            operating_cash_flow = cash_flow.loc['Operating Cash Flow'][0]
            ratios['Operating Cash Flow Ratio'] = operating_cash_flow / current_liabilities
        except Exception as e:
            print(f"Error calculating Operating Cash Flow Ratio for {ticker}: {e}")
            ratios['Operating Cash Flow Ratio'] = "-"

        try:
            free_cash_flow = cash_flow.loc['Free Cash Flow'][0]
            ratios['Free Cash Flow, M$'] = free_cash_flow / 1_000_000
        except Exception as e:
            print(f"Error calculating Free Cash Flow for {ticker}: {e}")
            ratios['Free Cash Flow, M$'] = "-"

        # Additional financial ratios
        try:
            ratios['Profit Margins'] = stock_info.get('profitMargins', "-")
        except Exception as e:
            print(f"Error calculating Profit Margins for {ticker}: {e}")
            ratios['Profit Margins'] = "-"

        try:
            ratios['PEG Ratio'] = stock_info.get('pegRatio', "-")
        except Exception as e:
            print(f"Error calculating PEG Ratio for {ticker}: {e}")
            ratios['PEG Ratio'] = "-"

        try:
            float_shares = stock_info.get('floatShares', "-")
            ratios['Float Shares, M'] = float_shares / 1_000_000
        except Exception as e:
            print(f"Error calculating Float Shares for {ticker}: {e}")
            ratios['Float Shares, M'] = "-"

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")

    # Round numbers to 2 decimal places and use comma separator for thousands
    for key, value in ratios.items():
        if isinstance(value, (int, float)):
            ratios[key] = f"{value:,.2f}"

    return ratios

# Function to calculate financial ratios for the selected sector
def calculate_sector_ratios(tickers):
    sector_ratios = []
    for ticker in tickers:
        ratios = calculate_financial_ratios(ticker)
        if ratios:
            ratios['Ticker'] = ticker
            sector_ratios.append(ratios)

    # Convert the list of dictionaries to a DataFrame
    df_ratios = pd.DataFrame(sector_ratios)

    # Calculate the sector average for each financial ratio
    sector_avg = df_ratios.apply(pd.to_numeric, errors='coerce').mean(axis=0).fillna("-")

    # Round the sector averages to 2 decimal places and convert to string with comma separator
    sector_avg = sector_avg.apply(lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x)

    # Add the sector average to the DataFrame as a new column
    df_ratios['Sector Avg'] = sector_avg

    return df_ratios

# Streamlit code
st.title('نسب مالية للشركات في القطاعات المختارة')
st.markdown('@telmisany - برمجة يحيى التلمساني')

# Dropdown for selecting the sector
selected_sector = st.selectbox('اختر القطاع', [''] + list(tasi.keys()))

# Button for submitting the input
if st.button("Submit"):
    if selected_sector:
        # Get the list of tickers for the selected sector
        tickers = tasi[selected_sector]
        
        # Fetch and calculate financial ratios
        df = calculate_sector_ratios(tickers)
        
        # Display data
        if not df.empty:
            # Map the Ticker column to the values in the companies dictionary
            df['الشركة'] = df['Ticker'].map(companies)
            
            # Set 'الشركة' as the index of the DataFrame
            df.set_index('الشركة', inplace=True)
            
            # Drop the 'Ticker' column as it's no longer needed
            df.drop(columns=['Ticker'], inplace=True)
            
            # Re-order the columns to have 'Sector Avg' next to the mapped tickers
            columns_order = ['Sector Avg'] + [col for col in df.columns if col != 'Sector Avg']
            df = df[columns_order]
            
            # Apply the ratio translations to the index
            df = df.rename(index=ratio_translation)
            
            # Display data with Streamlit
            st.write(df.T)
        else:
            st.error("تعذر جلب البيانات")
