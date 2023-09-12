import streamlit as st
import yfinance as yf
import pandas as pd

pd.set_option('display.max_colwidth', 100)

st.title('اراء المحللين - Analyst Recommendations')
st.markdown('برمجة يحيى التلمساني - @telmisany')

# Define the ticker code
code = st.text_input('ادخل رمز السهم')

# Add a button for the user to click when they are ready to submit
if st.button('Submit'):
    if code:
        # Check if the ticker is numeric and append '.SR' if it is
        if code.isdigit():
            code = code + '.SR'

        # Fetch data
        ticker = yf.Ticker(code)
        info = ticker.info

        # Convert the data into a DataFrame
        df = pd.DataFrame.from_dict(info, orient='index').T

        # Define the columns to be selected
        col = ['shortName','recommendationKey','currentPrice','targetHighPrice','targetMeanPrice','targetLowPrice','numberOfAnalystOpinions']

        # Define the dictionary for renaming the columns
        col_dict = {
        'shortName': 'الشركة',
        'recommendationKey': 'توصيات المحللين',
        'currentPrice': 'السعر الحالي',
        'targetHighPrice': 'أعلى سعر مستهدف',
        'targetMeanPrice': 'متوسط السعر المستهدف',
        'targetLowPrice': 'أدني سعر مستهدف',
        'numberOfAnalystOpinions': 'عدد آراء المحللين'
        }

        # Select the columns from the DataFrame
        selected_df = df[col]

        # Rename the columns
        renamed_df = selected_df.rename(columns=col_dict)

        # Print the renamed DataFrame + Transpose the data
        table = renamed_df.T
        table['%'] = '-'

        for i , n in enumerate(table[0]):
            try:
                if  round((table[0][i] / table[0][2]-1)*100,2) > 0:
                    table['%'][i] = '+' + str(round((table[0][i] / table[0][2]-1)*100,1)) + '%'
                else:
                    table['%'][i] = str(round((table[0][i] / table[0][2]-1)*100,1)) + '%'
            except:
                continue

        table['%'][6] = '-' 
        table['%'][2] = '-'
        st.dataframe(table)
