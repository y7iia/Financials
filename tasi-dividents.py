import streamlit as st
import pandas as pd
import yfinance as yf
import logging


companies = {'2222.SR': 'أرامكو السعودية',
 '1180.SR': 'الأهلي السعودي',
 '2082.SR': 'أكوا باور',
 '1010.SR': 'الرياض',
 }


# TASI dictionary (Always Update this dict)
tasi = {'الطاقة': ['2222.SR',	'4030.SR',	'4200.SR',	'2030.SR',	'2381.SR'],        
'البتروكيماويات': ['2350.SR',  '1211.SR',  '2310.SR',  '2380.SR',  '2001.SR',  '2330.SR',  '2060.SR',  '2010.SR',  '2170.SR',  '2250.SR',  '2290.SR',  '2210.SR',  '1210.SR',  '2020.SR',  '2223.SR'],
'الأسمنت': ['3020.SR',  '3040.SR',  '3030.SR',  '3090.SR',  '3091.SR',  '3005.SR',  '3004.SR',  '3003.SR',  '3080.SR',  '3050.SR',  '3010.SR',  '3002.SR',  '3001.SR',  '3060.SR'],

'أفضل 30 سهم من حيث مجموع التوزيعات': list(companies.keys())
       }

def fetch_dividends(tickers):
    logging.info(f"Fetching dividends for the following tickers: {tickers}")
    dividends = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="max")  # Fetch all available historical data
            if 'Dividends' in hist.columns:
                # Filter out the rows where Dividends is 0
                div = hist[hist['Dividends'] != 0]['Dividends']

                if not div.empty:
                    # add the ticker as a column to the dividends DataFrame
                    div = div.to_frame(name='dividends')
                    div['ticker'] = ticker
                    dividends.append(div)
                else:
                    logging.warning(f"No dividends data found for {ticker}")
            else:
                logging.warning(f"No dividends column found for {ticker}")
        except Exception as e:
            logging.error(f"Error fetching data for {ticker}: {e}")

    # concatenate all the dividends DataFrames
    dividends = pd.concat(dividends) if dividends else pd.DataFrame()

    # map the tickers to their Arabic names
    dividends['ticker'] = dividends['ticker'].map(companies)

    # pivot the DataFrame and group by year
    dividends = dividends.pivot_table(index='ticker', columns=dividends.index.year, values='dividends', aggfunc='sum')

    # Calculate total dividends for each company and create a new column
    dividends['مجموع التوزيعات'] = dividends.sum(axis=1)

    # replace NaN values with '-' and round to 2 decimal places
    dividends = dividends.fillna('-').applymap(lambda x: round(x, 2) if isinstance(x, float) else x)

    return dividends

# Streamlit app
st.title('التوزيعات النقدية لسوق الأسهم السعودي - حسب القطاع')
st.markdown(' @telmisany - برمجة يحيى التلمساني')

# Dropdown menu
sector = st.selectbox('أختر قطاع', list([''] + list(tasi.keys())))

# Submit button
if st.button('Submit'):
    if sector == '':
        st.warning('الرجاء اختيار قطاع.')
    else:
        # Fetch tickers for the selected sector
        tickers = tasi[sector]

        # Fetch dividends
        dividends = fetch_dividends(tickers)

        # Sort the DataFrame by 'مجموع التوزيعات' in descending order
        sorted_dividends = dividends.sort_values('مجموع التوزيعات', ascending=False)

        # Display the sorted DataFrame in Streamlit
        st.dataframe(sorted_dividends)
     
# Add a statement
st.write("> ** ملاحظة مهمة: الأرباح في الجدول مجمعة حسب سنة التوزيع وليس بحسب السنة المالية** ")
st.write('\n')
st.markdown('[تطبيقات أخرى قد تعجبك:](https://twitter.com/telmisany/status/1702641486792159334)')


# Add three empty lines for spacing
st.write('\n\n\n')

# Add a hyperlink to your Twitter account
st.markdown('[X تابعني في منصة](https://twitter.com/telmisany)')
