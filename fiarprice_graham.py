import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
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
'السلع طويلة الاجل': ['2340.SR', '4012.SR', '4180.SR', '4011.SR', '2130.SR', '1213.SR']
}


# Create a dictionary of ticker symbols to company names
companies = {'1010.SR': 'الرياض',
 '1020.SR': 'الجزيرة',
 '1030.SR': 'استثمار',
 '1050.SR': 'السعودي الفرنسي',
 '1060.SR': 'الأول',
 '1080.SR': 'العربي الوطني',
 '1111.SR': 'مجموعة تداول',
 '1120.SR': 'الراجحي',
 '1140.SR': 'البلاد',
 '1150.SR': 'الإنماء',
 '1180.SR': 'الأهلي السعودي',
 '1182.SR': 'أملاك العالمية',
 '1183.SR': 'سهل',
 '1201.SR': 'تكوين',
 '1202.SR': 'مبكو',
 '1210.SR': 'بي سي آى',
 '1211.SR': 'معادن',
 '1212.SR': 'أسترا الصناعية',
 '1213.SR': 'نسيج',
 '1214.SR': 'الحسن شاكر',
 '1301.SR': 'أسلاك',
 '1302.SR': 'بوان',
 '1303.SR': 'صناعات كهربائية',
 '1304.SR': 'اليمامة للحديد',
 '1320.SR': 'الأنابيب السعودية',
 '1321.SR': 'أنابيب الشرق',
 '1322.SR': 'اماك',
 '1810.SR': 'سيرا القابضة',
 '1820.SR': 'مجموعة الحكير',
 '1830.SR': 'وقت اللياقة',
 '1831.SR': 'مهارة',
 '1832.SR': 'صدر',
 '1833.SR': 'الموارد',
 '1834.SR': 'سماسكو',
 '2001.SR': 'كيمانول',
 '2010.SR': 'سابك',
 '2020.SR': 'سابك للمغذيات الزراعية',
 '2030.SR': 'المصافي',
 '2040.SR': 'الخزف السعودي',
 '2050.SR': 'صافولا',
 '2060.SR': 'التصنيع',
 '2070.SR': 'الدوائية',
 '2080.SR': 'غازكو',
 '2081.SR': 'الخريّف لتقنية المياه والطاقة',
 '2082.SR': 'اكوا باور',
 '2083.SR': 'مرافق',
 '2084.SR': 'مياهنا',
 '2090.SR': 'جبسكو',
 '2100.SR': 'وفرة',
 '2110.SR': 'الكابلات',
 '2120.SR': 'المتطورة',
 '2130.SR': 'صدق',
 '2140.SR': 'أيان للاستثمار',
 '2150.SR': 'زجاج',
 '2160.SR': 'أميانتيت',
 '2170.SR': 'اللجين القابضة',
 '2180.SR': 'فيبكو',
 '2190.SR': 'سيسكو القابضة',
 '2200.SR': 'أنابيب *',
 '2210.SR': 'نماء للكيماويات',
 '2220.SR': 'معدنية',
 '2222.SR': 'أرامكو السعودية',
 '2223.SR': 'لوبريف',
 '2230.SR': 'الكيميائية السعودية القابضة',
 '2240.SR': 'الزامل للصناعة',
 '2250.SR': 'المجموعة السعودية',
 '2270.SR': 'سدافكو',
 '2280.SR': 'المراعي',
 '2281.SR': 'تنمية',
 '2282.SR': 'نقي',
 '2283.SR': 'المطاحن الأولى',
 '2284.SR': 'المطاحن الحديثة',
 '2290.SR': 'ينساب',
 '2300.SR': 'صناعة الورق',
 '2310.SR': 'سبكيم العالمية',
 '2320.SR': 'البابطين',
 '2330.SR': 'المتقدمة',
 '2340.SR': 'العبداللطيف',
 '2350.SR': 'كيان السعودية',
 '2360.SR': 'الفخارية',
 '2370.SR': 'مسك',
 '2380.SR': 'بترو رابغ',
 '2381.SR': 'الحفر العربية',
 '2382.SR': 'أديس القابضة',
 '3001.SR': 'أسمنت حائل',
 '3002.SR': 'أسمنت نجران',
 '3003.SR': 'أسمنت المدينة',
 '3004.SR': 'أسمنت الشمالية',
 '3005.SR': 'ام القرى',
 '3007.SR': 'زهرة الواحة للتجارة',
 '3008.SR': 'الكثيري القابضة',
 '3010.SR': 'أسمنت العربية',
 '3020.SR': 'أسمنت اليمامة',
 '3030.SR': 'أسمنت السعودية',
 '3040.SR': 'أسمنت القصيم',
 '3050.SR': 'أسمنت الجنوبية',
 '3060.SR': 'أسمنت ينبع',
 '3080.SR': 'أسمنت الشرقية',
 '3090.SR': 'أسمنت تبوك',
 '3091.SR': 'أسمنت الجوف',
 '3092.SR': 'أسمنت الرياض',
 '4001.SR': 'أسواق ع العثيم',
 '4002.SR': 'المواساة',
 '4003.SR': 'إكسترا',
 '4004.SR': 'دله الصحية',
 '4005.SR': 'رعاية',
 '4006.SR': 'أسواق المزرعة',
 '4007.SR': 'الحمادي',
 '4008.SR': 'ساكو',
 '4009.SR': 'المستشفى السعودي الألماني',
 '4011.SR': 'لازوردي',
 '4012.SR': 'الأصيل',
 '4013.SR': 'د. سليمان الحبيب',
 '4014.SR': 'دار المعدات',
 '4015.SR': 'جمجوم فارما',
 '4016.SR': 'أفالون فارما',
 '4017.SR': 'فقيه الطبية',
 '4020.SR': 'العقارية',
 '4030.SR': 'البحري',
 '4031.SR': 'الخدمات الأرضية',
 '4040.SR': 'سابتكو',
 '4050.SR': 'ساسكو',
 '4051.SR': 'باعظيم',
 '4061.SR': 'أنعام القابضة',
 '4070.SR': 'تهامة للإعلان',
 '4071.SR': 'العربية',
 '4072.SR': 'مجموعة إم بي سي',
 '4080.SR': 'سناد القابضة',
 '4081.SR': 'النايفات',
 '4082.SR': 'مرنة',
 '4090.SR': 'طيبة',
 '4100.SR': 'مكة للإنشاء',
 '4110.SR': 'باتك',
 '4130.SR': 'الباحة',
 '4140.SR': 'صادرات *',
 '4141.SR': 'العمران',
 '4142.SR': 'كابلات الرياض',
 '4143.SR': 'تالكو',
 '4150.SR': 'التعمير',
 '4160.SR': 'ثمار',
 '4161.SR': 'بن داود',
 '4162.SR': 'المنجم للأغذية',
 '4163.SR': 'الدواء',
 '4164.SR': 'النهدي',
 '4170.SR': 'شمس',
 '4180.SR': 'مجموعة فتيحي',
 '4190.SR': 'جرير',
 '4191.SR': 'أبو معطي',
 '4192.SR': 'السيف غاليري',
 '4200.SR': 'الدريس',
 '4210.SR': 'الأبحاث و الإعلام',
 '4220.SR': 'إعمار',
 '4230.SR': 'البحر الأحمر',
 '4240.SR': 'الحكير',
 '4250.SR': 'جبل عمر',
 '4260.SR': 'بدجت السعودية',
 '4261.SR': 'ذيب',
 '4262.SR': 'لومي',
 '4263.SR': 'سال',
 '4270.SR': 'طباعة وتغليف',
 '4280.SR': 'المملكة',
 '4290.SR': 'الخليج للتدريب',
 '4291.SR': 'الوطنية للتربية والتعليم',
 '4292.SR': 'عطاء التعليمية',
 '4300.SR': 'دار الأركان',
 '4310.SR': 'مدينة المعرفة',
 '4320.SR': 'الأندلس العقارية',
 '4321.SR': 'المراكز العربية',
 '4322.SR': 'رتال',
 '4323.SR': 'سمو',
 '4330.SR': 'الرياض ريت',
 '4331.SR': 'الجزيرة ريت',
 '4332.SR': 'جدوى ريت الحرمين',
 '4333.SR': 'تعليم ريت',
 '4334.SR': 'المعذر ريت',
 '4335.SR': 'مشاركة ريت',
 '4336.SR': 'ملكية ريت',
 '4337.SR': 'المشاعر ريت',
 '4338.SR': 'الأهلي ريت 1',
 '4339.SR': 'صندوق دراية ريت',
 '4340.SR': 'الراجحي ريت',
 '4342.SR': 'جدوى ريت السعودية',
 '4344.SR': 'سدكو كابيتال ريت',
 '4345.SR': 'الإنماء ريت',
 '4346.SR': 'ميفك ريت',
 '4347.SR': 'بنيان ريت',
 '4348.SR': 'الخبير ريت',
 '4349.SR': 'الإنماء ريت الفندقي',
 '4701.SR': 'الخبير للنمو والدخل',
 '5110.SR': 'كهرباء السعودية',
 '6001.SR': 'حلواني إخوان',
 '6002.SR': 'هرفي للأغذية',
 '6004.SR': 'كاتريون',
 '6010.SR': 'نادك',
 '6012.SR': 'ريدان الغذائية',
 '6013.SR': 'التطويرية الغذائية',
 '6014.SR': 'الأمار',
 '6015.SR': 'أمريكانا',
 '6020.SR': 'جاكو',
 '6040.SR': 'تبوك الزراعية',
 '6050.SR': 'الأسماك',
 '6060.SR': 'الشرقية للتنمية',
 '6070.SR': 'الجوف',
 '6090.SR': 'جازادكو',
 '7010.SR': 'اس تي سي',
 '7020.SR': 'إتحاد إتصالات',
 '7030.SR': 'زين السعودية',
 '7040.SR': 'عذيب للاتصالات',
 '7200.SR': 'ام آي اس',
 '7201.SR': 'بحر العرب',
 '7202.SR': 'سلوشنز',
 '7203.SR': 'عِلم',
 '7204.SR': 'توبي',
 '8010.SR': 'التعاونية',
 '8012.SR': 'جزيرة تكافل',
 '8020.SR': 'ملاذ للتأمين',
 '8030.SR': 'ميدغلف للتأمين',
 '8040.SR': 'أليانز إس إف',
 '8050.SR': 'سلامة',
 '8060.SR': 'ولاء للتأمين',
 '8070.SR': 'الدرع العربي',
 '8100.SR': 'سايكو',
 '8120.SR': 'إتحاد الخليج الأهلية',
 '8150.SR': 'أسيج',
 '8160.SR': 'التأمين العربية',
 '8170.SR': 'الاتحاد للتأمين',
 '8180.SR': 'الصقر للتأمين *',
 '8190.SR': 'المتحدة للتأمين',
 '8200.SR': 'الإعادة السعودية',
 '8210.SR': 'بوبا العربية',
 '8230.SR': 'تكافل الراجحي',
 '8240.SR': 'تشب العربية',
 '8250.SR': 'جي آي جي',
 '8260.SR': 'الخليجية العامة',
 '8270.SR': 'بروج للتأمين',
 '8280.SR': 'العالمية',
 '8300.SR': 'الوطنية',
 '8310.SR': 'أمانة للتأمين',
 '8311.SR': 'عناية',
 '8313.SR': 'رسن'
            }

# Setup logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

def fetch_data_for_stock(stock):
    try:
        # Fetch data for a stock using yfinance
        data = yf.Ticker(stock).info
        # Convert the dictionary into a DataFrame
        df = pd.DataFrame([data])
        return df
    except Exception as e:
        logging.error(f"Error fetching data for stock {stock}: {e}")
        return pd.DataFrame()

def calculate_graham_number_and_eps_type(row, factor):
    try:
        # Use forward EPS if available, else use trailing EPS
        if not pd.isna(row['forwardEps']):
            eps = row['forwardEps']
            eps_type = 'Forward'
        else:
            eps = row['trailingEps']
            eps_type = 'Trailing'
        # Calculate Graham number and round to 2 decimal places
        graham_number = round(np.sqrt(factor * eps * row['bookValue']), 2)
        return graham_number, eps_type
    except Exception as e:
        logging.error(f"Error calculating Graham number for row {row['symbol']}: {e}")
        return np.nan, None

def get_data_for_sector(sector):
    try:
        stock_codes = tasi[sector]
        data = [fetch_data_for_stock(code) for code in stock_codes]
        df = pd.concat(data, ignore_index=True)
        columns_to_select = ['symbol','trailingEps','forwardEps','bookValue', 'currentPrice']
        df = df[[col for col in columns_to_select if col in df.columns]]
        # Add 'company' column
        df['company'] = df['symbol'].copy()
        # Replace symbols with company names
        df['symbol'] = df['symbol'].replace(companies)
        # Calculate Graham numbers and add new columns
        for factor in [22.5, 30, 50]:
            df[f'Graham_{factor}'], df['EPS_Type'] = zip(*df.apply(lambda row: calculate_graham_number_and_eps_type(row, factor), axis=1))
        # Drop rows with missing 'Graham_22.5' values
        df = df.dropna(subset=['Graham_22.5'])
        # Reorder columns
        df = df[['symbol', 'company', 'trailingEps', 'forwardEps', 'bookValue', 'currentPrice', 'Graham_22.5', 'Graham_30', 'Graham_50']]
        # Set 'symbol' as index
        df = df.set_index('symbol')
        # Rename index
        df.index.names = ['الشركة']
        # Rename columns
        column_names = {
            'company': 'الرمز',
            'trailingEps': 'ربحية السهم الحالية',
            'forwardEps': 'ربحية السهم المتوقعة',
            'bookValue': 'القيمة الدفترية',
            'currentPrice': 'السعر الحالي',
            'Graham_22.5': 'تقييم متشدد',
            'Graham_30': 'تقييم متساهل',
            'Graham_50': 'تقييم متساهل جدا'
        }
        df = df.rename(columns=column_names)
        # Round all floating-point numbers to two decimal places
        df = df.round({col: 2 for col in df.select_dtypes(float).columns})
        # Apply styling
        def color_cells(row):
            color = {}
            for col in ['تقييم متشدد', 'تقييم متساهل', 'تقييم متساهل جدا']:
                color[col] = 'background-color: LightGreen' if row['السعر الحالي'] < row[col] else 'background-color: LightCoral'
            return pd.Series(color)
        styled_df = df.style.apply(color_cells, axis=1)
        return styled_df
    except Exception as e:
        logging.error(f"Error getting data for sector {sector}: {e}")
        return pd.DataFrame()
     
     
# Streamlit code
st.title('حساب القيمة العادلة بأستخدام طريقة جراهام')
st.markdown(' @telmisany - برمجة يحيى التلمساني')


# User input
sector = st.selectbox('اختار القطاع المطلوب', options=[''] + list(tasi.keys()))

# Submit button
if st.button('Submit'):
    if sector:
        # Fetch and display data
        sector_data = get_data_for_sector(sector)
        st.dataframe(sector_data)
    else:
        st.write(":أختار القطاع المطلوب")

# Fetch and display data
sector_data = get_data_for_sector(sector)


st.markdown('[تطبيقات أخرى قد تعجبك](https://twitter.com/telmisany/status/1702641486792159334)')
# Add three empty lines for spacing
st.write('\n\n\n')
# Add a hyperlink to your Twitter account
st.markdown('[X تابعني في منصة](https://twitter.com/telmisany)')

# Buy me coffee AD
image_url = 'https://drive.google.com/file/d/1L7hg_kGgWZmbNJvDbWGWkfFcfDXawR_U/view?usp=sharing'
link_url = 'https://www.buymeacoffee.com/y7iia'
st.markdown(f'<a href="{link_url}"><img src="{image_url}" alt="Image" width="200"/></a>', unsafe_allow_html=True)
