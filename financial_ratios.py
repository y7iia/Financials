import streamlit as st
import yfinance as yf
import pandas as pd

# Define the sectors and companies
tasi = {
    'الطاقة': ['4030.SR', '2222.SR', '2382.SR', '4200.SR', '2381.SR', '2030.SR']
}

companies = {
    '1010.SR': 'الرياض',
    '1020.SR': 'الجزيرة'
}

# Function to calculate financial ratios for a single company
def calculate_financial_ratios(ticker):
    company = yf.Ticker(ticker)
    ratios = {}
    try:
        balance_sheet = company.balance_sheet
        financials = company.financials
        cash_flow = company.cashflow
        stock_info = company.info
        current_price = company.history(period="1d")['Close'].iloc[-1]
        
        try:
            shares_outstanding = stock_info.get('sharesOutstanding', "-")
            ratios['Number of Shares, M'] = shares_outstanding / 1_000_000
        except Exception as e:
            ratios['Number of Shares, M'] = "-"
        
        try:
            current_assets = balance_sheet.loc['Current Assets'][0]
            current_liabilities = balance_sheet.loc['Current Liabilities'][0]
            ratios['Current Ratio'] = current_assets / current_liabilities
        except Exception as e:
            ratios['Current Ratio'] = "-"
        
        try:
            cash_and_equivalents = balance_sheet.loc['Cash And Cash Equivalents'][0]
            ratios['Quick Ratio'] = (cash_and_equivalents + balance_sheet.loc['Receivables'][0]) / current_liabilities
        except Exception as e:
            ratios['Quick Ratio'] = "-"
        
        try:
            total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest'][0]
            total_equity = balance_sheet.loc['Stockholders Equity'][0]
            ratios['Debt-to-Equity Ratio'] = total_liabilities / total_equity
        except Exception as e:
            ratios['Debt-to-Equity Ratio'] = "-"
        
        try:
            net_income = financials.loc['Net Income'][0]
            ratios['ROE'] = net_income / total_equity
        except Exception as e:
            ratios['ROE'] = "-"
        
        try:
            ratios['P/E Ratio'] = stock_info.get('trailingPE', "-")
        except Exception as e:
            ratios['P/E Ratio'] = "-"
        
        try:
            if 'Stockholders Equity' in balance_sheet.index:
                total_equity = balance_sheet.loc['Stockholders Equity'][0]
                ratios['Book Value, M$'] = total_equity / 1_000_000
            else:
                ratios['Book Value, M$'] = "-"
        except Exception as e:
            ratios['Book Value, M$'] = "-"
        
        try:
            market_cap = stock_info.get('marketCap', "-")
            ratios['BV Multiple'] = market_cap / total_equity if total_equity != 0 else "-"
        except Exception as e:
            ratios['BV Multiple'] = "-"
        
        try:
            shares_outstanding = stock_info.get('sharesOutstanding', "-")
            ratios['Number of Shares, M'] = shares_outstanding / 1_000_000
        except Exception as e:
            ratios['Number of Shares, M'] = "-"
        
        try:
            ratios['Stock Price'] = current_price
        except Exception as e:
            ratios['Stock Price'] = "-"
        
        try:
            ratios['Market Cap, B$'] = market_cap / 1_000_000_000
        except Exception as e:
            ratios['Market Cap, B$'] = "-"
        
        try:
            ratios['Book Value per Share'] = total_equity / shares_outstanding
        except Exception as e:
            ratios['Book Value per Share'] = "-"
        
        try:
            diluted_eps = financials.loc['Diluted EPS'][0]
            ratios['EPS'] = diluted_eps
        except Exception as e:
            ratios['EPS'] = "-"
        
        try:
            dividends_paid = cash_flow.loc['Cash Dividends Paid'][0]
            ratios['Dividend Payout Ratio'] = dividends_paid / net_income
        except Exception as e:
            ratios['Dividend Payout Ratio'] = "-"
        
        try:
            operating_cash_flow = cash_flow.loc['Operating Cash Flow'][0]
            ratios['Operating Cash Flow Ratio'] = operating_cash_flow / current_liabilities
        except Exception as e:
            ratios['Operating Cash Flow Ratio'] = "-"
        
        try:
            free_cash_flow = cash_flow.loc['Free Cash Flow'][0]
            ratios['Free Cash Flow, M$'] = free_cash_flow / 1_000_000
        except Exception as e:
            ratios['Free Cash Flow, M$'] = "-"
        
        try:
            ratios['Profit Margins'] = stock_info.get('profitMargins', "-")
        except Exception as e:
            ratios['Profit Margins'] = "-"
        
        try:
            ratios['PEG Ratio'] = stock_info.get('pegRatio', "-")
        except Exception as e:
            ratios['PEG Ratio'] = "-"
        
        try:
            float_shares = stock_info.get('floatShares', "-")
            ratios['Float Shares, M'] = float_shares / 1_000_000
        except Exception as e:
            ratios['Float Shares, M'] = "-"
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
    
    for key, value in ratios.items():
        if isinstance(value, (int, float)):
            ratios[key] = f"{value:,.2f}"
    
    return ratios

# Streamlit code
st.title('النسب المالية لشركات سوق الأسهم السعودي حسب القطاع')
st.markdown('@telmisany - برمجة يحيى التلمساني')

# Sector selection
sector = st.selectbox('اختار القطاع', list(tasi.keys()))

# Submit button
if st.button('Submit'):
    tickers = tasi[sector]
    sector_ratios = {}
    
    for ticker in tickers:
        ratios = calculate_financial_ratios(ticker)
        if ratios:
            sector_ratios[ticker] = ratios
    
    if sector_ratios:
        df_ratios = pd.DataFrame(sector_ratios)
        
        # Exclude 'Stock Price' from sector average calculation
        ratios_for_avg = df_ratios.drop('Stock Price', errors='ignore')
        sector_avg = ratios_for_avg.apply(pd.to_numeric, errors='coerce').mean(axis=1).fillna("-")
        sector_avg = sector_avg.apply(lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x)
        df_ratios['Sector Avg'] = sector_avg
        
        ratio_sequence = [
            'Stock Price', 'Market Cap, B$', 'Number of Shares, M', 'Float Shares, M', 'P/E Ratio', 'EPS',
            'Book Value per Share', 'BV Multiple', 'ROE', 'Book Value, M$', 'Debt-to-Equity Ratio', 'Current Ratio',
            'Quick Ratio', 'Dividend Payout Ratio', 'Operating Cash Flow Ratio', 'Free Cash Flow, M$', 'Profit Margins',
            'PEG Ratio'
        ]
        
        columns = ['Sector Avg'] + tickers
        df_ratios = df_ratios.reindex(ratio_sequence, axis=0).reindex(columns, axis=1)
        
        ratio_translation = {
            'Stock Price': 'سعر السهم', 'Current Ratio': 'نسبة التداول', 'Quick Ratio': 'نسبة السيولة السريعة',
            'Debt-to-Equity Ratio': 'نسبة الدين إلى حقوق الملكية', 'ROE': 'العائد على حقوق الملكية', 'P/E Ratio': 'مكرر الأرباح',
            'Book Value, M$': 'حقوق المساهمين، مليون دولار', 'BV Multiple': 'مضاعف القيمة الدفترية',
            'Number of Shares, M': 'عدد الأسهم، مليون', 'Market Cap, B$': 'القيمة السوقية، مليار دولار',
            'Book Value per Share': 'القيمة الدفترية لكل سهم', 'EPS': 'ربحية السهم', 'Dividend Payout Ratio': 'نسبة توزيع الأرباح',
            'Operating Cash Flow Ratio': 'نسبة التدفق النقدي التشغيلي', 'Free Cash Flow, M$': 'التدفق النقدي الحر، مليون دولار',
            'Profit Margins': 'هامش الربحية', 'PEG Ratio': 'نسبة PEG', 'Float Shares, M': 'الأسهم الحرة، مليون'
        }
        
        df_ratios_arabic = df_ratios.rename(index=ratio_translation)
        df_ratios_arabic = df_ratios_arabic.rename(columns=companies)
        df_ratios_arabic = df_ratios_arabic.rename(columns={'Sector Avg': 'معدل القطاع'})
        
        st.dataframe(df_ratios_arabic)
    else:
        st.write('No data available for the selected sector')

# Add a hyperlink to your Twitter account
st.markdown('[تابعني على تويتر](https://twitter.com/telmisany)')

# Buy me a coffee AD
image_url = 'https://i.ibb.co/dM0tT0f/buy-me-coffee.png'
link_url = 'https://www.buymeacoffee.com/y7iia'
st.markdown(f'<a href="{link_url}"><img src="{image_url}" alt="Buy me a coffee" width="200"/></a>', unsafe_allow_html=True)
