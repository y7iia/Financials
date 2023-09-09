import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

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
    close = data['Close'][-2]

    P, R1, R2, R3, S1, S2, S3 = calculate_pivot_points(high, low, close, method)

    st.write(f"Ticker: {ticker}")
    st.write(f"===============R3 is: {R3:.2f}")
    st.write(f"==========R2 is: {R2:.2f}")
    st.write(f"=====R1 is: {R1:.2f}")
    st.write(f"Close is: {close:.2f}")
    st.write(f"=====S1 is: {S1:.2f}")
    st.write(f"==========S2 is: {S2:.2f}")
    st.write(f"===============S3 is: {S3:.2f}")


# get historical market data for the last week
data = yf.download(ticker, period="1wk")

fig = go.Figure(data=[
    go.Candlestick(x=data.index,
                   open=data['Open'],
                   high=data['High'],
                   low=data['Low'],
                   close=data['Close'])
])

# Add support and resistance levels
fig.add_trace(go.Scatter(x=data.index, y=[R1]*len(data.index), mode='lines', name='R1'))
fig.add_trace(go.Scatter(x=data.index, y=[R2]*len(data.index), mode='lines', name='R2'))
fig.add_trace(go.Scatter(x=data.index, y=[R3]*len(data.index), mode='lines', name='R3'))
fig.add_trace(go.Scatter(x=data.index, y=[S1]*len(data.index), mode='lines', name='S1'))
fig.add_trace(go.Scatter(x=data.index, y=[S2]*len(data.index), mode='lines', name='S2'))
fig.add_trace(go.Scatter(x=data.index, y=[S3]*len(data.index), mode='lines', name='S3'))

# Set titles
fig.update_layout(
    title=f'Candlestick chart for {ticker}',
    yaxis_title='Stock Price (Currency)',
    shapes = [dict(x0='2019-12-01', x1='2019-12-01', y0=0, y1=1, xref='x', yref='paper',
                   line_width=2)], # adding a vertical line
    annotations=[dict(x='2019-12-01', y=0.05, xref='x', yref='paper',
                      showarrow=False, xanchor='left', text='Increase Period Begins')]
)

st.plotly_chart(fig)
