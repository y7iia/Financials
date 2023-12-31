import streamlit as st
import pandas as pd
import yfinance as yf
import logging

companies = {'2222.SR': 'أرامكو السعودية',
 '1180.SR': 'الأهلي السعودي',
 '2082.SR': 'أكوا باور',
 '1010.SR': 'الرياض',
 '1150.SR': 'الإنماء',
 '2350.SR': 'كيان السـعودية',
 '1211.SR': 'معادن',
 '2310.SR': 'سبكيم العالمية',
 '7020.SR': 'اتحاد اتصالات',
 '2380.SR': 'بترو رابغ',
 '2001.SR': 'كيمانول',
 '2330.SR': 'المتقدمة',
 '2060.SR': 'التصنيع',
 '7203.SR': 'علم',
 '1050.SR': 'السعودي الفرنسي',
 '1202.SR': 'مبكو',
 '4261.SR': 'ذيب',
 '4004.SR': 'دله الصحية',
 '1111.SR': 'مجموعة تداول',
 '5110.SR': 'كهرباء السعودية',
 '2010.SR': 'سابك',
 '1140.SR': 'البلاد',
 '1810.SR': 'سيرا القابضة',
 '2280.SR': 'المراعي',
 '2170.SR': 'اللجين القابضة',
 '8210.SR': 'بوبا العربية',
 '3020.SR': 'أسمنت اليمامة',
 '2250.SR': 'المجموعة السعودية',
 '4300.SR': 'دار الأركان',
 '1830.SR': 'وقت اللياقة',
 '4030.SR': 'البحري',
 '4291.SR': 'الوطنية للتربية والتعليم',
 '2050.SR': 'صافولا',
 '4005.SR': 'رعاية',
 '4007.SR': 'الحمادي',
 '2290.SR': 'ينساب',
 '2300.SR': 'صناعة الورق',
 '2270.SR': 'سدافكو',
 '8250.SR': 'جي آي جي',
 '4013.SR': 'د. سليمان الحبيب',
 '4210.SR': 'الأبحاث والتسويق',
 '4003.SR': 'إكسترا',
 '3040.SR': 'أسمنت القصيم',
 '4161.SR': 'بن داود',
 '3030.SR': 'أسمنت السعودية',
 '4009.SR': 'المستشفى السعودي الألماني',
 '4260.SR': 'بدجت السعودية',
 '4347.SR': 'بنيان ريت',
 '4290.SR': 'الخليج للتدريب',
 '4344.SR': 'سدكو كابيتال ريت',
 '4310.SR': 'مدينة المعرفة',
 '3090.SR': 'أسمنت تبوك',
 '4334.SR': 'المعذر ريت',
 '3091.SR': 'أسمنت الجوف',
 '8030.SR': 'ميدغلف للتأمين',
 '4280.SR': 'المملكة',
 '4336.SR': 'ملكية ريت',
 '4332.SR': 'جدوى ريت الحرمين',
 '4345.SR': 'الأنماء ريت للتجزئة',
 '4031.SR': 'الخدمات الأرضية',
 '4340.SR': 'الراجحي ريت',
 '4338.SR': 'الأهلي ريت 1',
 '8160.SR': 'التأمين العربية',
 '4002.SR': 'المواساة',
 '2210.SR': 'نماء للكيماويات',
 '8280.SR': 'العالمية',
 '4333.SR': 'تعليم ريت',
 '4020.SR': 'العقارية',
 '4001.SR': 'أسواق ع العثيم',
 '4346.SR': 'ميفك ريت',
 '3005.SR': 'أم القرى',
 '8240.SR': 'تشب العربية',
 '8070.SR': 'الدرع العربي',
 '2040.SR': 'الخزف السعودي',
 '8120.SR': 'إتحاد الخليج الأهلية',
 '3004.SR': 'أسمنت الشمالية',
 '4348.SR': 'الخبير ريت',
 '4162.SR': 'المنجم',
 '2070.SR': 'الدوائية',
 '8170.SR': 'الاتحاد للتأمين',
 '4150.SR': 'التعمير',
 '4330.SR': 'الرياض ريت',
 '8270.SR': 'بروج للتأمين',
 '6001.SR': 'حلواني إخوان',
 '4342.SR': 'جدوى ريت السعودية',
 '8050.SR': 'سلامة',
 '4230.SR': 'البحر الأحمر',
 '4335.SR': 'مشاركة ريت',
 '3003.SR': 'أسمنت المدينة',
 '6012.SR': 'ريدان الغذائية',
 '4160.SR': 'ثمار',
 '3080.SR': 'أسمنت الشرقية',
 '4061.SR': 'أنعام القابضة',
 '3050.SR': 'أسمنت الجنوبية',
 '8100.SR': 'سايكو',
 '1820.SR': 'مجموعة الحكير',
 '8012.SR': 'جزيرة تكافل',
 '4320.SR': 'الأندلس',
 '4006.SR': 'أسواق المزرعة',
 '1303.SR': 'صناعات كهربائية',
 '3010.SR': 'أسمنت العربية',
 '4337.SR': 'مشاعر ريت',
 '8150.SR': 'أسيج',
 '1320.SR': 'الأنابيب السعودية',
 '4292.SR': 'عطاء التعليمية',
 '3002.SR': 'أسمنت نجران',
 '4190.SR': 'جرير',
 '2340.SR': 'العبداللطيف',
 '1201.SR': 'تكوين',
 '6020.SR': 'جاكو',
 '6002.SR': 'هرفي للأغذية',
 '3008.SR': 'الكثيري القابضة',
 '4191.SR': 'أبو معطي',
 '4339.SR': 'دراية ريت',
 '4270.SR': 'طباعة وتغليف',
 '8311.SR': 'عناية',
 '3001.SR': 'أسمنت حائل',
 '8260.SR': 'الخليجية العامة',
 '4010.SR': 'دور',
 '6090.SR': 'جازادكو',
 '4180.SR': 'مجموعة فتيحي',
 '8200.SR': 'الإعادة السعودية',
 '4100.SR': 'مكة للإنشاء',
 '4012.SR': 'ثوب الأصيل',
 '8310.SR': 'أمانة للتأمين',
 '6010.SR': 'نادك',
 '4040.SR': 'سابتكو',
 '2130.SR': 'صدق',
 '1214.SR': 'الحسن شاكر',
 '2080.SR': 'غازكو',
 '8180.SR': 'الصقر للتأمين',
 '1212.SR': 'أسترا الصناعية',
 '8060.SR': 'ولاء للتأمين',
 '2140.SR': 'أيان للاستثمار',
 '8312.SR': 'الإنماء طوكيو م',
 '2281.SR': 'تنمية',
 '4200.SR': 'الدريس',
 '2110.SR': 'الكابلات',
 '7201.SR': 'بحر العرب',
 '2370.SR': 'مسك',
 '6070.SR': 'الجوف',
 '4008.SR': 'ساكو',
 '8190.SR': 'المتحدة للتأمين',
 '1210.SR': 'بي سي آى',
 '4331.SR': 'الجزيرة ريت',
 '2220.SR': 'معدنية',
 '1213.SR': 'نسيج',
 '2160.SR': 'أميانتيت',
 '2200.SR': 'أنابيب',
 '1301.SR': 'أسلاك',
 '4141.SR': 'العمران للصناعة والتجارة',
 '4110.SR': 'باتك',
 '2100.SR': 'وفرة',
 '2081.SR': 'الخريف',
 '1831.SR': 'مهارة',
 '3060.SR': 'أسمنت ينبع',
 '4080.SR': 'سناد القابضة',
 '2360.SR': 'الفخارية',
 '6004.SR': 'التموين',
 '8020.SR': 'ملاذ للتأمين',
 '1020.SR': 'الجزيرة',
 '1182.SR': 'أملاك',
 '6060.SR': 'الشرقية للتنمية',
 '3007.SR': 'زهرة الواحة للتجارة',
 '8040.SR': 'أليانز إس إف',
 '2180.SR': 'فيبكو',
 '8300.SR': 'الوطنية',
 '6050.SR': 'الأسماك',
 '2240.SR': 'الزامل للصناعة',
 '8230.SR': 'تكافل الراجحي',
 '6013.SR': 'التطويرية الغذائية',
 '6040.SR': 'تبوك الزراعية',
 '7200.SR': 'إم آي إس',
 '4090.SR': 'طيبة',
 '4240.SR': 'سينومي ريتيل',
 '4050.SR': 'ساسكو',
 '4011.SR': 'لازوردي',
 '2230.SR': 'الكيميائية',
 '1321.SR': 'أنابيب الشرق',
 '1302.SR': 'بوان',
 '4051.SR': 'باعظيم',
 '7040.SR': 'عذيب للاتصالات',
 '2320.SR': 'البابطين',
 '8010.SR': 'التعاونية',
 '1304.SR': 'اليمامة للحديد',
 '2090.SR': 'جبسكو',
 '4140.SR': 'صادرات',
 '4070.SR': 'تهامة للإعلان',
 '4081.SR': 'النايفات',
 '2030.SR': 'المصافي',
 '4321.SR': 'سينومي سنترز',
 '7202.SR': 'سلوشنز',
 '7030.SR': 'زين السعودية',
 '4250.SR': 'جبل عمر',
 '2190.SR': 'سيسكو',
 '4130.SR': 'الباحة',
 '4071.SR': 'العربية',
 '2150.SR': 'زجاج',
 '4220.SR': 'إعمار',
 '4014.SR': 'دار المعدات الطبية',
 '4170.SR': 'شمس',
 '1832.SR': 'صدر',
 '2120.SR': 'المتطورة',
 '1120.SR': 'الراجحي',
 '2020.SR': 'سابك للمغذيات الزراعية',
 '1030.SR': 'استثمار',
 '1080.SR': 'العربي الوطني',
 '1060.SR': 'ساب',
 '7010.SR': 'اس تي سي',
 '4163.SR': 'الدواء',
 '4164.SR': 'النهدي',
 '1322.SR': 'أماك',
 '4701.SR': 'الخبير للدخل',
 '1183.SR': 'سهل',
 '4322.SR': 'رتال',
 '6014.SR': 'الآمار',
 '2282.SR': 'نقي',
 '2381.SR': 'الحفر العربية',
 '2083.SR': 'مرافق',
 '6015.SR': 'أمريكانا',
 '4142.SR': 'كابلات الرياض',
 '2223.SR': 'لوبريف',
 '4192.SR': 'السيف غاليري',
 '7204.SR': 'توبي',
 '1833.SR': 'الموارد',
 '4015.SR': 'جمحوم فارما',
 '4082.SR': 'مرنة',
 '2283.SR': 'المطاحن الأولى',
 '4323.SR': 'سمو'}


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
image_url = 'https://i.ibb.co/dM0tT0f/buy-me-coffee.png'
link_url = 'https://www.buymeacoffee.com/y7iia'
st.markdown(f'<a href="{link_url}"><img src="{image_url}" alt="Image" width="200"/></a>', unsafe_allow_html=True)
