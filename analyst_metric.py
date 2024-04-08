import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta 

# Create a dictionary of ticker symbols to company names
companies = {
 '1010.SR': 'الرياض',
 '1020.SR': 'الجزيرة',
 '1030.SR': 'استثمار'}


# Streamlit interface elements
st.title('تقييم توصيات المحللين')
st.markdown(' @telmisany - برمجة يحيى التلمساني')
st.markdown(' برنامج يتيح للمستخدمين تقييم أداء توصيات المحللين الماليين عبر تحليل بيانات الأسهم التاريخية. يُمكن للمستخدم اختيار الشركة المُدرَجة في السوق السعودي، تحديد تاريخ التوصية، وإدخال السعر المستهدف الذي حدده المحلل. بعد ذلك، يقوم البرنامج بجلب بيانات السهم وتحديد ما إذا كان السعر قد وصل للهدف المُحدد ويُقدم تقريرًا يشمل العائد الأقصى والأدنى منذ تاريخ التوصية.')

# Select company
company_name = st.selectbox('اختر الشركة:', options=[""] + list(companies.values()))

# Input fields for the analyst information
analyst_date = st.date_input('أدخل تاريخ التوصية:')
analyst_name = st.text_input('أدخل اسم المحلل (اختياري):')
analyst_target = st.number_input('أدخل السعر المستهدف من المحلل:', min_value=0.0, format='%f')

# Function to fetch stock data and evaluate the analyst's recommendation
def evaluate_analyst_recommendation(ticker, target_date, target_price):
    try:
        # Define the end date as one year from the target date
        end_date = target_date + timedelta(days=365)

        # Fetch historical stock data from target date to end date
        stock_data = yf.download(ticker, start=target_date, end=end_date)

        if not stock_data.empty:
            # Calculate highest and lowest price since the target date
            highest_price = stock_data['High'].max()
            lowest_price = stock_data['Low'].min()
            highest_date = stock_data['High'].idxmax().strftime('%Y-%m-%d')
            lowest_date = stock_data['Low'].idxmin().strftime('%Y-%m-%d')
            initial_price = stock_data.iloc[0]['Open']
            highest_return = ((highest_price - initial_price) / initial_price) * 100
            lowest_return = ((lowest_price - initial_price) / initial_price) * 100

            # Check if the target was achieved within the year
            target_achieved = stock_data['High'] >= target_price
            if target_achieved.any():
                target_achieved_date = stock_data.loc[target_achieved].index[0].strftime('%Y-%m-%d')
                days_to_target = (target_achieved_date - target_date).days
                target_reached = 'نعم'
            else:
                target_achieved_date = 'N/A'
                days_to_target = 'N/A'
                target_reached = 'لا'

            # Create a results dictionary
            result_data = {
                'تاريخ التوصية': target_date.strftime('%Y-%m-%d'),
                'السعر المستهدف': round(target_price, 2),
                'تحقق الهدف': target_reached,
                'أعلى سعر وصل له السهم': f"{highest_price:.2f}",
                'تاريخ أعلى سعر': highest_date,
                'أعلى عائد %': f"{highest_return:.2f}%",
                'أدنى سعر وصل له السهم': f"{lowest_price:.2f}",
                'تاريخ أدنى سعر': lowest_date,
                'أدنى عائد %': f"{lowest_return:.2f}%",
                'تاريخ تحقق الهدف': target_achieved_date,
                'عدد الأيام لتحقيق الهدف': days_to_target
            }
            return result_data
        else:
            return "No data available for the selected stock and date range."
    except Exception as e:
        return f"An error occurred: {e}"


# Find the ticker symbol based on the selected company name
selected_ticker = None
for ticker, name in companies.items():
    if name == company_name:
        selected_ticker = ticker
        break

# Submit button
if st.button('تقييم التوصية'):
    if selected_ticker:
        # Pass all the required arguments to the function
        result = evaluate_analyst_recommendation(selected_ticker, analyst_date, analyst_target, analyst_name, company_name)
        if isinstance(result, pd.DataFrame):
            # Display results
            st.dataframe(result.T)
        else:
            # Display error message
            st.error(result)
    else:
        st.error('لم يتم العثور على الشركة في قائمة الرموز.')
