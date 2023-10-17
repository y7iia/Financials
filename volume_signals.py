import streamlit as st
import pandas as pd
import yfinance as yf
from ta.volatility import BollingerBands
from ta.volume import VolumeWeightedAveragePrice
import logging
import numpy as np
from ta.trend import EMAIndicator

# Create a dictionary of sector to ticker symbols
tasi = {
    #...
}

# Setup logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

def fetch_data_for_stock(stock):
    try:
        # Fetch historical data for a stock using yfinance
        data = yf.download(stock, period='90d')
        return data
    except Exception as e:
        logging.error(f"Error fetching data for stock {stock}: {e}")
        return pd.DataFrame()

def volume_signals(df):
    # Calculate EMA of volume
    ema_volume = EMAIndicator(df['Volume'], 90).ema_indicator()

    # Calculate Bollinger Bands
    bollinger = BollingerBands(df['Close'], 20, 2)
    upper_bollinger = bollinger.bollinger_hband()
    lower_bollinger = bollinger.bollinger_lband()

    # Count signals
    signals = (df['Volume'] > ema_volume) & (df['Close'] < upper_bollinger)
    return signals.sum()

def get_data_for_sector(sector):
    try:
        stock_codes = tasi[sector]
        data = {}
        for code in stock_codes:
            df = fetch_data_for_stock(code)
            if not df.empty:
                signals = volume_signals(df)
                latest_close = df['Close'].iloc[-1]
                data[code] = {
                    'ticker': code,
                    'sector': sector,
                    'latest_close': latest_close,
                    'volume_signals': signals
                }
        df = pd.DataFrame(data).T
        df = df.sort_values(by='volume_signals', ascending=False)
        return df
    except Exception as e:
        logging.error(f"Error getting data for sector {sector}: {e}")
        return pd.DataFrame()

# Streamlit code
st.title('حساب القيمة العادلة بأستخدام طريقة جراهام')
st.markdown('@telmisany - برمجة يحيى التلمساني')

# User input
sector = st.selectbox('اختار القطاع المطلوب', options=[''] + list(tasi.keys()))

# Submit button
if st.button('Submit'):
    if sector:
        # Fetch and display data
        sector_data = get_data_for_sector(sector)
        st.dataframe(sector_data)
    else:
        st.write(":أختار القطاع المطلوب")
