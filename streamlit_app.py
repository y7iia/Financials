import streamlit as st
import numpy as np
import pandas as pd
from yahooquery import Ticker

def get_retained_earnings(ticker):
    code = Ticker(ticker)
    code = code.all_financial_data(frequency = 'q').reset_index()
    code['RetainedEarnings'] = code['RetainedEarnings'] / 1000000

    # Rename the column
    code = code.rename(columns={'RetainedEarnings': 'الأرباح المبقاة بالمليون',
                                'symbol': 'الشركة',
                                'asOfDate': 'التاريخ' })

    data = code[['الشركة','التاريخ','الأرباح المبقاة بالمليون']]
    return data

ticker_input = st.text_input("ادخل رمز الشركة:")

if st.button("Submit"):
    if ticker_input:
        if ticker_input.isdigit():
            ticker_input = int(ticker_input)
            if 1111 <= ticker_input <= 9999:
                ticker = str(ticker_input) + '.SR'
            else:
                st.write("ادخل رمز الشركة: ")
        else:
            ticker = ticker_input

        df = get_retained_earnings(ticker)
        st.dataframe(df)
