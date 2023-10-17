import streamlit as st
import pandas as pd
import yfinance as yf
import ta
import numpy as np
import logging

# Dictionaries
# Create a dictionary of sector to ticker symbols
tasi = {}
# Create a dictionary of ticker symbols to company names
companies = {}

# Setup logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

def fetch_data_for_stock(stock):
    try:
        # Fetch historical market data using yfinance
        data = yf.download(stock, period='1y')
        return data
    except Exception as e:
        logging.error(f"Error fetching data for stock {stock}: {e}")
        return pd.DataFrame()

def convert_period_to_days(period):
    period_dict = {'1 month': 30, '3 months': 90, '6 months': 180}
    return period_dict.get(period, 30)  # default to 30 if period is not found

def volume_signals(data, period):
    try:
        # Filter data to only include the user-selected period
        data = data[-period:]

        data['Volume_EMA'] = data['Volume'].ewm(span=90, adjust=False).mean()
        conditions = (data['Volume'] > data['Volume_EMA']) & (data['Close'] < data['High'].shift().rolling(window=period).max())
        return sum(conditions)
    except Exception as e:
        logging.error(f"Error calculating volume signals: {e}")
        return np.nan

def get_data_for_sector(sector, period):
    try:
        stock_codes = tasi[sector]
        data = []
        period_in_days = convert_period_to_days(period)
        for code in stock_codes:
            stock_data = fetch_data_for_stock(code)
            signal_count = volume_signals(stock_data, period_in_days)
            latest_close = stock_data['Close'].iat[-1]
            data.append({
                'الرمز': code,
                'الاسم': companies.get(code),
                'القطاع': sector,
                'أحدث إغلاق': latest_close,
                'إشارات الحجم': signal_count
            })
        df = pd.DataFrame(data)
        df = df.sort_values(by='إشارات الحجم', ascending=False)
        return df
    except Exception as e:
        logging.error(f"Error getting data for sector {sector}: {e}")
        return pd.DataFrame()

# Streamlit code
st.title(' الأحجام الغير طبيعية خلال فترة زمنية معينة')
st.markdown(' @telmisany - برمجة يحيى التلمساني')

# User input
sector = st.selectbox('اختار القطاع المطلوب', options=[''] + list(tasi.keys()))
period = st.selectbox('اختار الفترة', options=['1 month', '3 months', '6 months'], index=0)

# Submit button
if st.button('Submit'):
    if sector:
        # Fetch and display data
        sector_data = get_data_for_sector(sector, period)
        st.dataframe(sector_data)
    else:
        st.write("أختار القطاع المطلوب")
