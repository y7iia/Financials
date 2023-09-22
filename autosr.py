import streamlit as st
import yfinance as yf


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
    data = yf.download(ticker, period="2d")
    high = data['High'][-2]
    low = data['Low'][-2]
    
    # Fetch accurate close prices
    data2 = yf.Ticker(ticker).info
    
    # Check if data2 is not empty
    if data2:
        df = pd.DataFrame(data2, index=[0])
        close = df.get('currentPrice')[0]
    else:
        st.error("Failed to get data for ticker: " + ticker)
    

    P, R1, R2, R3, S1, S2, S3 = calculate_pivot_points(high, low, close, method)

    st.write(f"Ticker: {ticker}")
    st.write(f"===============R3 is: {R3:.2f}")
    st.write(f"==========R2 is: {R2:.2f}")
    st.write(f"=====R1 is: {R1:.2f}")
    st.write(f"Close is: {close:.2f}")
    st.write(f"=====S1 is: {S1:.2f}")
    st.write(f"==========S2 is: {S2:.2f}")
    st.write(f"===============S3 is: {S3:.2f}")


st.write('\n')
st.markdown('[أنظر ايضا: آراء المحللين](https://twitter.com/telmisany/status/1701640774138445878)')
st.write('\n')
st.markdown('[أنظر ايضا: الأرباح المبقاة](https://twitter.com/telmisany/status/1700128870349811959)')

# Add three empty lines for spacing
st.write('\n\n\n')

# Add a hyperlink to your Twitter account
st.markdown('[X تابعني في منصة](https://twitter.com/telmisany)')
