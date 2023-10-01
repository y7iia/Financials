import streamlit as st
import pandas as pd
import yfinance as yf
import ta

# Define your company dictionary
companies = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Tesla': 'TSLA',
    'Amazon': 'AMZN',
    'Google': 'GOOGL',
    'Facebook': 'META',
    'Netflix': 'NFLX',
    'Alibaba': 'BABA',
    'Twitter': 'TWTR',
    'Nvidia': 'NVDA'
}

def EMA_points(df):
    # Calculate EMAs
    ema10 = ta.trend.EMAIndicator(df['Close'], window=10).ema_indicator()
    ema20 = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
    ema50 = ta.trend.EMAIndicator(df['Close'], window=50).ema_indicator()
    ema100 = ta.trend.EMAIndicator(df['Close'], window=100).ema_indicator()
    ema250 = ta.trend.EMAIndicator(df['Close'], window=250).ema_indicator()

    # Apply your conditions
    if df['Close'].iloc[-1] > ema10.iloc[-1] > ema20.iloc[-1] > ema50.iloc[-1] > ema100.iloc[-1] > ema250.iloc[-1]:
        return 5
    elif df['Close'].iloc[-1] > ema20.iloc[-1] > ema50.iloc[-1] > ema100.iloc[-1] > ema250.iloc[-1]:
        return 4
    elif df['Close'].iloc[-1] > ema50.iloc[-1] > ema100.iloc[-1] > ema250.iloc[-1]:
        return 3
    elif df['Close'].iloc[-1] > ema100.iloc[-1] > ema250.iloc[-1]:
        return 2
    elif df['Close'].iloc[-1] > ema250.iloc[-1]:
        return 1
    elif ema250.iloc[-1] > ema100.iloc[-1] > ema50.iloc[-1] > ema20.iloc[-1] > ema10.iloc[-1]:
        return -4
    elif ema250.iloc[-1] > ema100.iloc[-1] > ema50.iloc[-1] > ema20.iloc[-1]:
        return -3
    elif ema250.iloc[-1] > ema100.iloc[-1] > ema50.iloc[-1]:
        return -2
    elif ema250.iloc[-1] > ema100.iloc[-1]:
        return -1
    else:
        return 0

# Placeholder functions
def EMA_Volume_points(df):
    return 0

def EMA_Whale_points(df):
    return 0

def RSI_points(df):
    return 0

def MACD_points(df):
    return 0

def Bolinger_Bands_points(df):
    return 0

def OBV_points(df):
    return 0

def Divergence_points(df):
    return 0

# Calculate points for each company
data = []
for name, ticker in companies.items():
    df = yf.download(ticker, period='1y')
    try:
        points = EMA_points(df) + EMA_Volume_points(df) + EMA_Whale_points(df) + RSI_points(df) + MACD_points(df) + Bolinger_Bands_points(df) + OBV_points(df) + Divergence_points(df)
    except Exception as e:
        print(f"Error calculating points for {ticker}: {e}")
    data.append({'Company': name, 'Ticker': ticker, 'Points': points})

# Create a DataFrame and sort by Points
df = pd.DataFrame(data)
df = df.sort_values('Points', ascending=False)

# Display the DataFrame in Streamlit
st.dataframe(df)
