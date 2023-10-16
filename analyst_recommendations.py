import streamlit as st
import yfinance as yf
import pandas as pd

def fetch_data(ticker_code):
    # Fetch data
    ticker = yf.Ticker(ticker_code)
    info = ticker.info

    # Convert the data into a DataFrame
    df = pd.DataFrame.from_dict(info, orient='index').T

    # Define the columns to be selected
    col = ['shortName','recommendationKey','currentPrice','targetHighPrice','targetMeanPrice','targetLowPrice','numberOfAnalystOpinions']

    # Check and select only existing columns
    col = [c for c in col if c in df.columns]

    # Continue if there are any columns to select
    if not col:
        raise ValueError('No financial information for this ticker, select another one')

    # Define the dictionary for renaming the columns
    col_dict = {
    'shortName': 'Company الشركة',
    'recommendationKey': 'Recommendation توصيات المحللين',
    'currentPrice': 'Current Price السعر الحالي',
    'targetHighPrice': 'Target High أعلى سعر مستهدف',
    'targetMeanPrice': 'Target Mean متوسط السعر المستهدف',
    'targetLowPrice': 'Target Low أدني سعر مستهدف',
    'numberOfAnalystOpinions': 'Analyst Opinions عدد آراء المحلين'
    }

    # Select the columns from the DataFrame
    selected_df = df[col]

    # Rename the columns
    renamed_df = selected_df.rename(columns=col_dict)

    # Transpose the data
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

    table['%'][2] = '-'
    table['%'][6] = '-'
    table.rename(columns={0: 'المستهدف'}, inplace=True)

    return table

st.title('اراء المحللين - Analyst Recommendations')
st.markdown(' @telmisany - برمجة يحيى التلمساني')

# Define the ticker code
code = st.text_input('Enter Ticker ادخل رمز السهم')

# Add a button for the user to click when they are ready to submit
if st.button('Submit'):
    if code:
        # Check if the ticker is numeric and append '.SR' if it is
        if code.isdigit():
            code = code + '.SR'
        
        try:
            table = fetch_data(code)

            # Convert DataFrame to HTML and use inline style to control width
            html_table = table.to_html(classes='table table-striped', header="true", table_id="html_table").replace('<table ','<table style="width:100% !important;" ')
            
            # Display the HTML table in Streamlit
            st.markdown(html_table, unsafe_allow_html=True)
        except Exception as e:
            st.error(f'Error fetching data: {e}')

st.markdown('[تطبيقات أخرى قد تعجبك](https://twitter.com/telmisany/status/1702641486792159334)')
# Add three empty lines for spacing
st.write('\n\n\n')
# Add a hyperlink to your Twitter account
st.markdown('[X تابعني في منصة](https://twitter.com/telmisany)')

# Buy me coffee AD:
image_url = 'https://i.ibb.co/dM0tT0f/buy-me-coffee.png'
link_url = 'https://www.buymeacoffee.com/y7iia'
st.markdown(f'<a href="{link_url}"><img src="{image_url}" alt="Image" width="200"/></a>', unsafe_allow_html=True)

