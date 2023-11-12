import streamlit as st
import yfinance as yf
import pandas as pd


def calculate_pivot_points(high, low, close, method):
    if method == "standard":
        P = (high + low + close) / 3
        R1 = (2 * P) - low
        R2 = P + (high - low)
        R3 = high + 2*(P - low)
        S1 = (2 * P) - high
        S2 = P - (high - low)
        S3 = low - 2*(high - P)
    elif method == "woodie":
        P = (high + low + 2 * close) / 4
        R1 = (2 * P) - low
        R2 = P + (high - low)
        R3 = R1 + (high - low)
        S1 = (2 * P) - high
        S2 = P - (high - low)
        S3 = S1 - (high - low)
    elif method == "camarilla":
        P = (high + low + close) / 3
        R1 = close + ((high - low) * 1.1 / 12)
        R2 = close + ((high - low) * 1.1 / 6)
        R3 = close + ((high - low) * 1.1 / 4)
        S1 = close - ((high - low) * 1.1 / 12)
        S2 = close - ((high - low) * 1.1 / 6)
        S3 = close - ((high - low) * 1.1 / 4)
    else:
        raise ValueError("Invalid method. Use either 'standard', 'woodie', or 'camarilla'.")
    return P, R1, R2, R3, S1, S2, S3

st.title('حاسبة الدعوم والمقاومات Pivot Point Calculator')
st.markdown(' @telmisany - برمجة يحيى التلمساني')

ticker = st.text_input("ادخل رمز السهم Enter the stock ticker: ")

# if ticker is a number between 999 and 9999, add '.SR' to it
try:
    ticker_number = int(ticker)
    if 999 < ticker_number < 9999:
        ticker += '.SR'
except ValueError:
    pass

method = st.selectbox("اختر طريقة الحساب Choose the calculation method:", ('standard', 'woodie', 'camarilla'))

if st.button('أحسب Calculate Pivot Points'):
    # get historical market data
    data = yf.download(ticker, period="1d")
    high = data['High'][-1]
    low = data['Low'][-1]
    
   #currently info method is not working. so, use download method to get the close prices
    close = data['Close'][-1]
    
    # Fetch accurate close prices [use this way whenever, info method is working]
    # data2 = yf.Ticker(ticker).info
    # close = pd.DataFrame(data2).T[0]['currentPrice']
    

    P, R1, R2, R3, S1, S2, S3 = calculate_pivot_points(high, low, close, method)

    st.write(f"Ticker: {ticker}")
    st.write(f"===============R3 is: {R3:.2f}")
    st.write(f"==========R2 is: {R2:.2f}")
    st.write(f"=====R1 is: {R1:.2f}")
    st.write(f"Close is: {close:.2f}")
    st.write(f"=====S1 is: {S1:.2f}")
    st.write(f"==========S2 is: {S2:.2f}")
    st.write(f"===============S3 is: {S3:.2f}")


st.markdown('[تطبيقات أخرى قد تعجبك](https://twitter.com/telmisany/status/1702641486792159334)')
# Add three empty lines for spacing
st.write('\n\n\n')
# Add a hyperlink to your Twitter account
st.markdown('[X تابعني في منصة](https://twitter.com/telmisany)')

# Buy me coffee AD:
image_url = 'https://i.ibb.co/dM0tT0f/buy-me-coffee.png'
link_url = 'https://www.buymeacoffee.com/y7iia'
st.markdown(f'<a href="{link_url}"><img src="{image_url}" alt="Image" width="200"/></a>', unsafe_allow_html=True)

