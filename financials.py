import streamlit as st
import pandas as pd
import yfinance as yf
import logging


# Create a dictionary of ticker symbols to company names
companies = {1010: 'الرياض',
 1020: 'الجزيرة',
 1030: 'استثمار',
 1050: 'السعودي الفرنسي',
 1060: 'الأول',
 1080: 'العربي الوطني',
 1111: 'مجموعة تداول',
 1120: 'الراجحي',
 1140: 'البلاد',
 1150: 'الإنماء',
 1180: 'الأهلي السعودي',
 1182: 'أملاك العالمية',
 1183: 'سهل',
 1201: 'تكوين ',
 1202: 'مبكو',
 1210: 'بي سي آى',
 1211: 'معادن',
 1212: 'أسترا الصناعية',
 1213: 'نسيج',
 1214: 'الحسن شاكر',
 1301: 'أسلاك',
 1302: 'بوان',
 1303: 'صناعات كهربائية',
 1304: 'اليمامة للحديد',
 1320: 'الأنابيب السعودية',
 1321: 'أنابيب الشرق',
 1322: 'اماك',
 1810: 'سيرا القابضة',
 1820: 'مجموعة الحكير',
 1830: 'وقت اللياقة',
 1831: 'مهارة',
 1832: 'صدر',
 1833: 'الموارد',
 2001: 'كيمانول',
 2010: 'سابك',
 2020: 'سابك للمغذيات الزراعية',
 2030: 'المصافي',
 2040: 'الخزف السعودي',
 2050: 'صافولا',
 2060: 'التصنيع',
 2070: 'الدوائية',
 2080: 'غازكو',
 2081: 'الخريّف لتقنية المياه والطاقة',
 2082: 'اكوا باور',
 2083: 'مرافق',
 2090: 'جبسكو',
 2100: 'وفرة',
 2110: 'الكابلات',
 2120: 'المتطورة',
 2130: 'صدق',
 2140: 'أيان للاستثمار',
 2150: 'زجاج',
 2160: 'أميانتيت ',
 2170: 'اللجين القابضة',
 2180: 'فيبكو',
 2190: 'سيسكو القابضة',
 2200: 'أنابيب *',
 2210: 'نماء للكيماويات',
 2220: 'معدنية ',
 2222: 'أرامكو السعودية',
 2223: 'لوبريف',
 2230: 'الكيميائية السعودية القابضة',
 2240: 'الزامل للصناعة',
 2250: 'المجموعة السعودية',
 2270: 'سدافكو',
 2280: 'المراعي',
 2281: 'تنمية',
 2282: 'نقي',
 2283: 'المطاحن الأولى',
 2284: 'المطاحن الحديثة',
 2290: 'ينساب',
 2300: 'صناعة الورق ',
 2310: 'سبكيم العالمية',
 2320: 'البابطين',
 2330: 'المتقدمة',
 2340: 'العبداللطيف',
 2350: 'كيان السعودية',
 2360: 'الفخارية',
 2370: 'مسك',
 2380: 'بترو رابغ ',
 2381: 'الحفر العربية',
 2382: 'أديس القابضة',
 3001: 'أسمنت حائل',
 3002: 'أسمنت نجران',
 3003: 'أسمنت المدينة',
 3004: 'أسمنت الشمالية',
 3005: 'ام القرى',
 3007: 'زهرة الواحة للتجارة',
 3008: 'الكثيري القابضة',
 3010: 'أسمنت العربية',
 3020: 'أسمنت اليمامة',
 3030: 'أسمنت السعودية',
 3040: 'أسمنت القصيم',
 3050: 'أسمنت الجنوبية',
 3060: 'أسمنت ينبع',
 3080: 'أسمنت الشرقية',
 3090: 'أسمنت تبوك',
 3091: 'أسمنت الجوف',
 3092: 'أسمنت الرياض',
 4001: 'أسواق ع العثيم',
 4002: 'المواساة',
 4003: 'إكسترا',
 4004: 'دله الصحية',
 4005: 'رعاية',
 4006: 'أسواق المزرعة',
 4007: 'الحمادي',
 4008: 'ساكو',
 4009: 'المستشفى السعودي الألماني',
 4011: 'لازوردي',
 4012: 'الأصيل',
 4013: 'د. سليمان الحبيب',
 4014: 'دار المعدات ',
 4015: 'جمجوم فارما',
 4016: 'أفالون فارما',
 4020: 'العقارية',
 4030: 'البحري',
 4031: 'الخدمات الأرضية',
 4040: 'سابتكو ',
 4050: 'ساسكو',
 4051: 'باعظيم',
 4061: 'أنعام القابضة',
 4070: 'تهامة للإعلان',
 4071: 'العربية',
 4072: 'مجموعة إم بي سي',
 4080: 'سناد القابضة',
 4081: 'النايفات',
 4082: 'مرنة',
 4090: 'طيبة',
 4100: 'مكة للإنشاء',
 4110: 'باتك',
 4130: 'الباحة ',
 4140: 'صادرات',
 4141: 'العمران',
 4142: 'كابلات الرياض',
 4150: 'التعمير',
 4160: 'ثمار ',
 4161: 'بن داود',
 4162: 'المنجم للأغذية',
 4163: 'الدواء',
 4164: 'النهدي',
 4170: 'شمس ',
 4180: 'مجموعة فتيحي',
 4190: 'جرير',
 4191: 'أبو معطي',
 4192: 'السيف غاليري',
 4200: 'الدريس',
 4210: 'الأبحاث و الإعلام',
 4220: 'إعمار ',
 4230: 'البحر الأحمر ',
 4240: 'الحكير',
 4250: 'جبل عمر',
 4260: 'بدجت السعودية',
 4261: 'ذيب',
 4262: 'لومي',
 4263: 'سال',
 4270: 'طباعة وتغليف',
 4280: 'المملكة ',
 4290: 'الخليج للتدريب',
 4291: 'الوطنية للتربية والتعليم',
 4292: 'عطاء التعليمية',
 4300: 'دار الأركان',
 4310: 'مدينة المعرفة',
 4320: 'الأندلس العقارية',
 4321: 'المراكز العربية',
 4322: 'رتال',
 4323: 'سمو ',
 5110: 'كهرباء السعودية',
 6001: 'حلواني إخوان',
 6002: 'هرفي للأغذية',
 6004: 'كاتريون',
 6010: 'نادك',
 6012: 'ريدان الغذائية',
 6013: 'التطويرية الغذائية',
 6014: 'الأمار',
 6015: 'أمريكانا',
 6020: 'جاكو',
 6040: 'تبوك الزراعية ',
 6050: 'الأسماك ',
 6060: 'الشرقية للتنمية',
 6070: 'الجوف',
 6090: 'جازادكو',
 7010: 'اس تي سي',
 7020: 'إتحاد إتصالات',
 7030: 'زين السعودية ',
 7040: 'عذيب للاتصالات',
 7200: 'ام آي اس',
 7201: 'بحر العرب',
 7202: 'سلوشنز',
 7203: 'عِلم',
 7204: 'توبي',
 8010: 'التعاونية',
 8012: 'جزيرة تكافل',
 8020: 'ملاذ للتأمين',
 8030: 'ميدغلف للتأمين ',
 8040: 'أليانز إس إف',
 8050: 'سلامة',
 8060: 'ولاء للتأمين',
 8070: 'الدرع العربي',
 8100: 'سايكو ',
 8120: 'إتحاد الخليج الأهلية ',
 8150: 'أسيج ',
 8160: 'التأمين العربية',
 8170: 'الاتحاد للتأمين',
 8180: 'الصقر للتأمين *',
 8190: 'المتحدة للتأمين',
 8200: 'الإعادة السعودية',
 8210: 'بوبا العربية',
 8230: 'تكافل الراجحي',
 8240: 'تشب العربية',
 8250: 'جي آي جي',
 8260: 'الخليجية العامة',
 8270: 'بروج للتأمين',
 8280: 'العالمية',
 8300: 'الوطنية',
 8310: 'أمانة للتأمين ',
 8311: 'عناية'}

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
