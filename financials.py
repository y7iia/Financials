import streamlit as st
import pandas as pd
import yfinance as yf
import logging



# Create a dictionary of sector to ticker symbols

tasi = {
'الطاقة': ['4030.SR', '2222.SR', '2382.SR', '4200.SR', '2381.SR', '2030.SR'],
'البتروكيماويات': ['2250.SR', '2310.SR', '2060.SR', '2170.SR', '2330.SR', '2010.SR', '2380.SR', '2210.SR', '2001.SR', '2020.SR', '2290.SR', '2350.SR'],
'التأمين': ['8210.SR', '8100.SR', '8040.SR', '8170.SR', '8160.SR', '8070.SR', '8260.SR', '8250.SR', '8020.SR', '8150.SR', '8012.SR', '8060.SR', '8190.SR', '8280.SR', '8240.SR', '8030.SR', '8230.SR', '8311.SR', '8180.SR', '8010.SR', '8200.SR', '8270.SR', '8310.SR', '8300.SR', '8050.SR', '8120.SR', '8313.SR'],
'أسمنت': ['3050.SR', '3092.SR', '3002.SR', '3005.SR', '3020.SR', '3010.SR', '3030.SR', '3001.SR', '3060.SR', '3004.SR', '3080.SR', '3090.SR', '3091.SR', '3003.SR', '3040.SR'],
'المواد الاساسية': ['1321.SR', '2223.SR', '1301.SR', '1211.SR', '1320.SR', '2300.SR', '3007.SR', '1322.SR', '2090.SR', '1210.SR', '2200.SR', '2150.SR', '2360.SR', '3008.SR', '2220.SR', '1202.SR', '1304.SR', '1201.SR', '2240.SR', '2180.SR'],
'إدارة وتطوير العقارات': ['4090.SR', '4321.SR', '4320.SR', '4150.SR', '4323.SR', '4020.SR', '4300.SR', '4250.SR', '4220.SR', '4322.SR', '4310.SR', '4100.SR', '4230.SR'],
'إنتاج الأغذية': ['2270.SR', '2280.SR', '2050.SR', '6070.SR', '6040.SR', '6020.SR', '6010.SR', '2281.SR', '6001.SR', '6050.SR', '2100.SR', '4080.SR', '6090.SR', '2283.SR', '2282.SR', '6060.SR', '2284.SR'],
'الاتصالات': ['7020.SR', '7040.SR', '7030.SR', '7010.SR'],
'البنوك': ['1080.SR', '1030.SR', '1010.SR', '1140.SR', '1020.SR', '1060.SR', '1120.SR', '1050.SR', '1150.SR', '1180.SR'],
'الرعاية الصحية': ['4013.SR', '2230.SR', '4005.SR', '4002.SR', '4014.SR', '4009.SR', '2140.SR', '4004.SR', '4007.SR', '4017.SR'],
'المواد الرأسمالية': ['1302.SR', '1214.SR', '1303.SR', '1212.SR', '2160.SR', '2040.SR', '4142.SR', '2370.SR', '4141.SR', '2320.SR', '4140.SR', '4110.SR', '2110.SR', '4143.SR'],
'الاعلام والترفيه': ['4210.SR', '4070.SR', '4072.SR', '4071.SR'],
'الخدمات المالية': ['4081.SR', '1182.SR', '2120.SR', '1183.SR', '1111.SR', '4280.SR', '4082.SR', '4130.SR'],
'تجزئة وتوزيع السلع الاستهلاكية': ['4006.SR', '4001.SR', '4160.SR', '4162.SR', '4163.SR', '4161.SR', '4164.SR', '4061.SR'],
'النقل': ['4261.SR', '4262.SR', '4260.SR', '4031.SR', '4040.SR', '2190.SR', '4263.SR'],
'المرافق العامة': ['2083.SR', '2081.SR', '2080.SR', '2082.SR', '5110.SR', '2084.SR'],
'الادوية': ['4016.SR', '4015.SR', '2070.SR'],
'الخدمات الاستهلاكية': ['4290.SR', '1820.SR', '1810.SR', '1830.SR', '4170.SR', '6002.SR', '6015.SR', '4292.SR', '6012.SR', '6013.SR', '6014.SR', '4291.SR'],
'الخدمات التجارية والمهنية': ['1832.SR', '1831.SR', '4270.SR', '1833.SR', '6004.SR', '1834.SR'],
'تجزئة وتوزيع السلع الكمالية': ['4051.SR', '4240.SR', '4192.SR', '4190.SR', '4003.SR', '4050.SR', '4191.SR', '4008.SR'],
'التطبيقات وخدمات التقنية': ['7203.SR', '7201.SR', '7204.SR', '7200.SR', '7202.SR'],
'السلع طويلة الاجل': ['2340.SR', '4012.SR', '4180.SR', '4011.SR', '2130.SR', '1213.SR'],
'تاسي' : ['^TASI.SR']
}


# Configure logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Function to fetch financial data
def fetch_financial_data(ticker, financial_type, frequency):
    try:
        t = yf.Ticker(ticker)
        if financial_type == 'income statement':
            data = t.financials if frequency == 'yearly' else t.quarterly_financials
        elif financial_type == 'balance sheet':
            data = t.balance_sheet if frequency == 'yearly' else t.quarterly_balance_sheet
        elif financial_type == 'cash flow':
            data = t.cashflow if frequency == 'yearly' else t.quarterly_cashflow
        else:
            logging.error(f"Invalid financial type: {financial_type}")
            return None

        return data.iloc[:, 0:1]
    except Exception as e:
        logging.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

def aggregate_financial_data(tickers, financial_type, frequency):
    # Empty dictionary to store data
    data = {}

    # Loop over tickers
    for ticker in tickers:
        ticker_data = fetch_financial_data(ticker, financial_type, frequency)
        if ticker_data is not None:
            data[ticker] = ticker_data

    # Combine all data into a single DataFrame and transpose
    try:
        df = pd.concat(data, axis=1).T
        df = df.reset_index(level=1, drop=True)  # Remove the date index
    except Exception as e:
        logging.error(f"Error processing data: {str(e)}")
        return None

    return df




# TASI dictionary (Always Update this dict)
tasi = {'الطاقة': ['2222.SR',	'4030.SR',	'4200.SR',	'2030.SR',	'2381.SR'],        
'البتروكيماويات': ['2350.SR',  '1211.SR',  '2310.SR',  '2380.SR',  '2001.SR',  '2330.SR',  '2060.SR',  '2010.SR',  '2170.SR',  '2250.SR',  '2290.SR',  '2210.SR',  '1210.SR',  '2020.SR',  '2223.SR'],
'الأسمنت': ['3020.SR',  '3040.SR',  '3030.SR',  '3090.SR',  '3091.SR',  '3005.SR',  '3004.SR',  '3003.SR',  '3080.SR',  '3050.SR',  '3010.SR',  '3002.SR',  '3001.SR',  '3060.SR'],
'البنوك': ['1180.SR',  '1010.SR',  '1150.SR',  '1050.SR',  '1140.SR',  '1020.SR',  '1182.SR',  '1120.SR',  '1030.SR',  '1080.SR',  '1060.SR',  '1183.SR'],
'التأمين': ['8210.SR',  '8250.SR',  '8030.SR',  '8160.SR',  '8280.SR',  '8240.SR',  '8070.SR',  '8120.SR',  '8170.SR',  '8270.SR',  '8050.SR',  '8100.SR',  '8012.SR',  '8150.SR',  '8311.SR',  '8260.SR',  '8200.SR',  '8310.SR',  '8180.SR',  '8060.SR',  '8312.SR',  '8190.SR',  '8020.SR',  '8040.SR',  '8300.SR',  '8230.SR',  '8010.SR'],
'الرعاية الصحية': ['4004.SR',  '4005.SR',  '4007.SR',  '4013.SR',  '4009.SR',  '4002.SR',  '2140.SR',  '2230.SR',  '4014.SR'],
'التطبيقات وخدمات التقنية': ['7203.SR','7201.SR','7200.SR',  '7202.SR',  '7204.SR'],
'الإتصالات': ['7020.SR', '7040.SR', '7030.SR', '7010.SR'],
'الإستثمار والتمويل': ['1111.SR',  '4280.SR',  '4080.SR',  '4081.SR',  '4130.SR',  '2120.SR',  '4082.SR'],
'إدارة وتطوير العقارات': ['4300.SR',  '4310.SR',  '4020.SR',  '4150.SR',  '4230.SR',  '4320.SR',  '4100.SR',  '4090.SR',  '4321.SR',  '4250.SR',  '4220.SR',  '4322.SR',  '4323.SR'],
'الأدوية': ['2070.SR', '4015.SR'],
'الإعلام والترفيه': ['4210.SR', '4070.SR', '4071.SR'],
'الخدمات الإستهلاكية': ['1810.SR',  '1830.SR',  '4291.SR',  '4290.SR',  '6012.SR','6013.SR','1820.SR',  '4292.SR',  '6002.SR',  '4010.SR',  '4170.SR','6014.SR', '6015.SR'],
'الخدمات التجارية والمهنية': ['4270.SR',  '1831.SR',  '6004.SR',  '1832.SR',  '1833.SR'],
'السلع الرأسمالية': ['2040.SR',  '1303.SR',  '1212.SR',  '2110.SR',  '2370.SR',  '2160.SR',  '4141.SR',  '2360.SR',  '1302.SR',  '2320.SR',  '4140.SR',  '4142.SR'],
'السلع طويلة الاجل': ['2340.SR','4180.SR',  '4012.SR',  '2130.SR',  '1213.SR',  '4011.SR'],
'المرافق العامة': ['2082.SR', '5110.SR', '2080.SR', '2081.SR', '2083.SR'],
'المواد الأساسية': ['1202.SR',  '2300.SR',  '1320.SR',  '1201.SR',  '3008.SR', '2220.SR',  '2200.SR',  '1301.SR',  '3007.SR',  '2180.SR',  '2240.SR',  '1321.SR',  '1304.SR',  '2090.SR',  '2150.SR',  '1322.SR'],
'النقل': ['4261.SR', '4260.SR', '4031.SR', '4040.SR', '4110.SR', '2190.SR'],
'انتاج الأغذية': ['2280.SR',  '2050.SR',  '2270.SR',  '6001.SR',  '6020.SR',  '6090.SR',  '6010.SR',  '2281.SR',  '6070.SR',  '2100.SR',  '6060.SR',  '6050.SR',  '6040.SR', '2282.SR',  '2283.SR'],
'تجزئة الأغذية': ['4161.SR',  '4001.SR',  '4162.SR',  '4160.SR',  '4061.SR',  '4006.SR',  '4163.SR',  '4164.SR'],
'تجزئة السلع الكمالية': ['4003.SR',  '4190.SR',  '4191.SR',  '1214.SR',  '4008.SR','4240.SR',  '4050.SR',  '4051.SR',  '4192.SR'],
}


# Streamlit code
st.title('القوائم المالية لقطاعات سوق الأسهم السعودي')
st.markdown(' @telmisany - برمجة يحيى التلمساني')

# Dropdown for selecting the sector
selected_sector = st.selectbox('اختر القطاع', [''] + list(tasi.keys()))

# Define a dictionary for English-Arabic financial type
dic = {
    'income statement': 'قائمة الدخل', 
    'balance sheet': 'قائمة المركز المالي', 
    'cash flow': 'التدفقات النقدية'
}

# Dropdown for selecting the financial type in Arabic
financial_type_ARABIC = st.selectbox('اختر القائمة المالية', [''] + list(dic.values()))

# Find the corresponding English term
financial_type = [k for k, v in dic.items() if v == financial_type_ARABIC][0] if financial_type_ARABIC else ""

# Define a dictionary for English-Arabic frequency
dic_frq = {'yearly': 'سنوي', 'quarterly': 'ربع سنوي'}

# Dropdown for selecting the frequency in Arabic
frequency_ARABIC = st.selectbox('اختر الفترة', [''] + list(dic_frq.values()))

# Find the corresponding English term
frequency = [k for k, v in dic_frq.items() if v == frequency_ARABIC][0] if frequency_ARABIC else ""


# Button for submitting the input
if st.button("Submit"):
    # Get the list of tickers for the selected sector
    tickers = tasi[selected_sector]

    # Fetch data
    df = aggregate_financial_data(tickers, financial_type, frequency)

    # Display data
    if df is not None:
        df.index.names = ['Ticker']
        df = df.rename(index=companies)
        df = df.round(2)  # Round all numbers in the DataFrame to 2 decimal places
        df = df.div(1000000)  # Divide all numbers in the DataFrame by 1,000,000
        st.write(df.T)
             
    else:
        st.error("تعذر جلب البيانات")

# Add a statement
st.write("> **ملاحظة: جميع الأرقام بالمليون ريال سعودي** ")
st.markdown('[تطبيقات أخرى قد تعجبك](https://twitter.com/telmisany/status/1702641486792159334)')
# Add three empty lines for spacing
st.write('\n\n\n')
# Add a hyperlink to your Twitter account
st.markdown('[X تابعني في منصة](https://twitter.com/telmisany)')

# Buy me coffee AD
image_url = 'https://i.ibb.co/WkHT8HP/buy-me-coffee_2.png'
link_url = 'https://www.buymeacoffee.com/y7iia'
st.markdown(f'<a href="{link_url}"><img src="{image_url}" alt="Image" width="200"/></a>', unsafe_allow_html=True)
