import pandas as pd
import yfinance as yf
import streamlit as st
from datetime import timedelta

# Create a dictionary of sector to ticker symbols

tasi = {
'الطاقة': ['4200.SR', '2382.SR', '4030.SR', '2381.SR', '2222.SR', '2030.SR'],
'البتروكيماويات': ['2380.SR', '2290.SR', '2250.SR', '2020.SR', '2170.SR', '2210.SR', '2001.SR', '2310.SR', '2010.SR', '2060.SR', '2330.SR', '2350.SR'],
'التأمين': ['8313.SR', '8250.SR', '8012.SR', '8020.SR', '8210.SR', '8010.SR', '8150.SR', '8230.SR', '8200.SR', '8180.SR', '8070.SR', '8311.SR', '8040.SR', '8270.SR', '8160.SR', '8300.SR', '8280.SR', '8120.SR', '8060.SR', '8050.SR', '8260.SR', '8310.SR', '8240.SR', '8190.SR', '8170.SR', '8100.SR', '8030.SR'],
'البنوك': ['1030.SR', '1020.SR', '1180.SR', '1150.SR', '1010.SR', '1120.SR', '1050.SR', '1080.SR', '1060.SR', '1140.SR'],
'المرافق العامة': ['2082.SR', '2080.SR', '2081.SR', '2083.SR', '5110.SR', '2084.SR'],
'الاتصالات': ['7030.SR', '7040.SR', '7010.SR', '7020.SR'],
'إدارة وتطوير العقارات': ['4322.SR', '4300.SR', '4310.SR', '4323.SR', '4320.SR', '4250.SR', '4090.SR', '4100.SR', '4020.SR', '4230.SR', '4150.SR', '4321.SR', '4220.SR'],
'الادوية': ['4015.SR', '4016.SR', '2070.SR'],
'الاعلام والترفيه': ['4070.SR', '4072.SR', '4071.SR', '4210.SR'],
'التطبيقات وخدمات التقنية': ['7202.SR', '7200.SR', '7204.SR', '7203.SR', '7201.SR'],
'الخدمات الاستهلاكية': ['4292.SR', '4290.SR', '1830.SR', '6012.SR', '4291.SR', '6015.SR', '1810.SR', '6013.SR', '4170.SR', '1820.SR', '6002.SR', '6014.SR'],
'الخدمات التجارية والمهنية': ['1831.SR', '1832.SR', '6004.SR', '1833.SR', '4270.SR', '1834.SR'],
'الخدمات المالية': ['1111.SR', '4280.SR', '1182.SR', '4082.SR', '1183.SR', '2120.SR', '4081.SR', '4130.SR'],
'الرعاية الصحية': ['2230.SR', '4004.SR', '4017.SR', '4014.SR', '4009.SR', '4013.SR', '4002.SR', '2140.SR', '4005.SR', '4007.SR'],
'السلع طويلة الاجل': ['4012.SR', '2340.SR', '4011.SR', '1213.SR', '4180.SR', '2130.SR'],
'الصناديق العقارية المتداولة': ['4344.SR', '4345.SR', '4335.SR', '4339.SR', '4337.SR', '4338.SR', '4348.SR', '4336.SR', '4349.SR', '4340.SR', '4330.SR', '4350.SR', '4333.SR', '4331.SR', '4346.SR', '4334.SR', '4332.SR', '4342.SR', '4347.SR'],
'المواد الاساسية': ['3080.SR', '1321.SR', '3092.SR', '3003.SR', '3060.SR', '1320.SR', '2150.SR', '2240.SR', '3040.SR', '2300.SR', '3005.SR', '3010.SR', '3002.SR', '2360.SR', '2200.SR', '1211.SR', '3090.SR', '1202.SR', '3020.SR', '1210.SR', '3007.SR', '1301.SR', '1322.SR', '2223.SR', '3091.SR', '3004.SR', '1201.SR', '3050.SR', '3030.SR', '2090.SR', '1304.SR', '2220.SR', '2180.SR', '3008.SR'],
'المواد الرأسمالية': ['2160.SR', '1214.SR', '1212.SR', '1302.SR', '2040.SR', '4142.SR', '4143.SR', '2320.SR', '2370.SR', '4140.SR', '4141.SR', '1303.SR', '2110.SR', '4110.SR'],
'النقل': ['4031.SR', '2190.SR', '4260.SR', '4262.SR', '4263.SR', '4261.SR', '4040.SR'],
'إنتاج الأغذية': ['2283.SR', '6070.SR', '2284.SR', '2282.SR', '2050.SR', '2281.SR', '6090.SR', '2285.SR', '2100.SR', '6010.SR', '2286.SR', '2270.SR', '6040.SR', '6020.SR', '6001.SR', '6060.SR', '4080.SR', '6050.SR', '2280.SR'],
'تجزئة وتوزيع السلع الاستهلاكية': ['4001.SR', '4164.SR', '4162.SR', '4161.SR', '4163.SR', '4006.SR', '4160.SR', '4061.SR'],
'تجزئة وتوزيع السلع الكمالية': ['4240.SR', '4050.SR', '4190.SR', '4192.SR', '4003.SR', '4191.SR', '4008.SR', '4051.SR'],
'المنتجات المنزلية و الشخصية': ['4165.SR'],
'تاسي' : ['^TASI.SR']}



# Create a dictionary of ticker symbols to company names
companies = {'1010.SR': 'الرياض',
 '1020.SR': 'الجزيرة',
 '1030.SR': 'الإستثمار',
 '1050.SR': 'بي اس اف',
 '1060.SR': 'الأول',
 '1080.SR': 'العربي',
 '1111.SR': 'مجموعة تداول',
 '1120.SR': 'الراجحي',
 '1140.SR': 'البلاد',
 '1150.SR': 'الإنماء',
 '1180.SR': 'الأهلي',
 '1182.SR': 'أملاك',
 '1183.SR': 'سهل',
 '1201.SR': 'تكوين',
 '1202.SR': 'مبكو',
 '1210.SR': 'بي سي آي',
 '1211.SR': 'معادن',
 '1212.SR': 'أسترا الصناعية',
 '1213.SR': 'نسيج',
 '1214.SR': 'شاكر',
 '1301.SR': 'أسلاك',
 '1302.SR': 'بوان',
 '1303.SR': 'الصناعات الكهربائية',
 '1304.SR': 'اليمامة للحديد',
 '1320.SR': 'أنابيب السعودية',
 '1321.SR': 'أنابيب الشرق',
 '1322.SR': 'أماك',
 '1810.SR': 'سيرا',
 '1820.SR': 'مجموعة الحكير',
 '1830.SR': 'لجام للرياضة',
 '1831.SR': 'مهارة',
 '1832.SR': 'صدر',
 '1833.SR': 'الموارد',
 '1834.SR': 'سماسكو',
 '2001.SR': 'كيمانول',
 '2010.SR': 'سابك',
 '2020.SR': 'سابك للمغذيات الزراعية',
 '2030.SR': 'المصافي',
 '2040.SR': 'الخزف السعودي',
 '2050.SR': 'مجموعة صافولا',
 '2060.SR': 'التصنيع',
 '2070.SR': 'الدوائية',
 '2080.SR': 'الغاز',
 '2081.SR': 'الخريف',
 '2082.SR': 'أكوا باور',
 '2083.SR': 'مرافق',
 '2084.SR': 'مياهنا',
 '2090.SR': 'جبسكو',
 '2100.SR': 'وفرة',
 '2110.SR': 'الكابلات السعودية',
 '2120.SR': 'متطورة',
 '2130.SR': 'صدق',
 '2140.SR': 'أيان',
 '2150.SR': 'زجاج',
 '2160.SR': 'أميانتيت',
 '2170.SR': 'اللجين',
 '2180.SR': 'فيبكو',
 '2190.SR': 'سيسكو القابضة',
 '2200.SR': 'أنابيب',
 '2210.SR': 'نماء للكيماويات',
 '2220.SR': 'معدنية',
 '2222.SR': 'أرامكو السعودية',
 '2223.SR': 'لوبريف',
 '2230.SR': 'الكيميائية',
 '2240.SR': 'الزامل للصناعة',
 '2250.SR': 'المجموعة السعودية',
 '2270.SR': 'سدافكو',
 '2280.SR': 'المراعي',
 '2281.SR': 'تنمية',
 '2282.SR': 'نقي',
 '2283.SR': 'المطاحن الأولى',
 '2284.SR': 'المطاحن الحديثة',
 '2285.SR': 'المطاحن العربية',
 '2286.SR': 'المطاحن الرابعة',
 '2290.SR': 'ينساب',
 '2300.SR': 'صناعة الورق',
 '2310.SR': 'سبكيم العالمية',
 '2320.SR': 'البابطين',
 '2330.SR': 'المتقدمة',
 '2340.SR': 'ارتيكس',
 '2350.SR': 'كيان السعودية',
 '2360.SR': 'الفخارية',
 '2370.SR': 'مسك',
 '2380.SR': 'بترو رابغ',
 '2381.SR': 'الحفر العربية',
 '2382.SR': 'أديس',
 '3002.SR': 'أسمنت نجران',
 '3003.SR': 'أسمنت المدينة',
 '3004.SR': 'أسمنت الشمالية',
 '3005.SR': 'أسمنت ام القرى',
 '3007.SR': 'الواحة',
 '3008.SR': 'الكثيري',
 '3010.SR': 'أسمنت العربية',
 '3020.SR': 'أسمنت اليمامة',
 '3030.SR': 'أسمنت السعودية',
 '3040.SR': 'أسمنت القصيم',
 '3050.SR': 'أسمنت الجنوب',
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
 '4009.SR': 'السعودي الألماني الصحية',
 '4011.SR': 'لازوردي',
 '4012.SR': 'الأصيل',
 '4013.SR': 'سليمان الحبيب',
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
 '4070.SR': 'تهامة',
 '4071.SR': 'العربية',
 '4072.SR': 'مجموعة إم بي سي',
 '4080.SR': 'سناد القابضة',
 '4081.SR': 'النايفات',
 '4082.SR': 'مرنة',
 '4090.SR': 'طيبة',
 '4100.SR': 'مكة',
 '4110.SR': 'باتك',
 '4130.SR': 'الباحة',
 '4140.SR': 'صادرات',
 '4141.SR': 'العمران',
 '4142.SR': 'كابلات الرياض',
 '4143.SR': 'تالكو',
 '4150.SR': 'التعمير',
 '4160.SR': 'ثمار',
 '4161.SR': 'بن داود',
 '4162.SR': 'المنجم',
 '4163.SR': 'الدواء',
 '4164.SR': 'النهدي',
 '4165.SR': 'الماجد للعود',
 '4170.SR': 'شمس',
 '4180.SR': 'مجموعة فتيحي',
 '4190.SR': 'جرير',
 '4191.SR': 'أبو معطي',
 '4192.SR': 'السيف غاليري',
 '4200.SR': 'الدريس',
 '4210.SR': 'الأبحاث والإعلام',
 '4220.SR': 'إعمار',
 '4230.SR': 'البحر الأحمر',
 '4240.SR': 'سينومي ريتيل',
 '4250.SR': 'جبل عمر',
 '4260.SR': 'بدجت السعودية',
 '4261.SR': 'ذيب',
 '4262.SR': 'لومي',
 '4263.SR': 'سال',
 '4270.SR': 'طباعة وتغليف',
 '4280.SR': 'المملكة',
 '4290.SR': 'الخليج للتدريب',
 '4291.SR': 'الوطنية للتعليم',
 '4292.SR': 'عطاء',
 '4300.SR': 'دار الأركان',
 '4310.SR': 'مدينة المعرفة',
 '4320.SR': 'الأندلس',
 '4321.SR': 'سينومي سنترز',
 '4322.SR': 'رتال',
 '4323.SR': 'سمو',
 '4330.SR': 'الرياض ريت',
 '4331.SR': 'الجزيرة ريت',
 '4332.SR': 'جدوى ريت الحرمين',
 '4333.SR': 'تعليم ريت',
 '4334.SR': 'المعذر ريت',
 '4335.SR': 'مشاركة ريت',
 '4336.SR': 'ملكية ريت',
 '4337.SR': 'سيكو السعودية ريت',
 '4338.SR': 'الأهلي ريت 1',
 '4339.SR': 'دراية ريت',
 '4340.SR': 'الراجحي ريت',
 '4342.SR': 'جدوى ريت السعودية',
 '4344.SR': 'سدكو كابيتال ريت',
 '4345.SR': 'الإنماء ريت للتجزئة',
 '4346.SR': 'ميفك ريت',
 '4347.SR': 'بنيان ريت',
 '4348.SR': 'الخبير ريت',
 '4349.SR': 'الإنماء ريت الفندقي',
 '4350.SR': 'الاستثمار ريت',
 '5110.SR': 'كهرباء السعودية',
 '6001.SR': 'حلواني إخوان',
 '6002.SR': 'هرفي للأغذية',
 '6004.SR': 'كاتريون',
 '6010.SR': 'نادك',
 '6012.SR': 'ريدان',
 '6013.SR': 'التطويرية الغذائية',
 '6014.SR': 'الآمار',
 '6015.SR': 'أمريكانا (شركة أجنبية)',
 '6020.SR': 'جاكو',
 '6040.SR': 'تبوك الزراعية',
 '6050.SR': 'الأسماك',
 '6060.SR': 'الشرقية للتنمية',
 '6070.SR': 'الجوف',
 '6090.SR': 'جازادكو',
 '7010.SR': 'اس تي سي',
 '7020.SR': 'إتحاد إتصالات',
 '7030.SR': 'زين السعودية',
 '7040.SR': 'عذيب للإتصالات',
 '7200.SR': 'إم آي إس',
 '7201.SR': 'بحر العرب',
 '7202.SR': 'سلوشنز',
 '7203.SR': 'علم',
 '7204.SR': 'توبي',
 '8010.SR': 'التعاونية',
 '8012.SR': 'جزيرة تكافل',
 '8020.SR': 'ملاذ للتأمين',
 '8030.SR': 'ميدغلف للتأمين',
 '8040.SR': 'أليانز إس إف',
 '8050.SR': 'سلامة',
 '8060.SR': 'ولاء',
 '8070.SR': 'الدرع العربي',
 '8100.SR': 'سايكو',
 '8120.SR': 'إتحاد الخليج الأهلية',
 '8150.SR': 'أسيج',
 '8160.SR': 'التأمين العربية',
 '8170.SR': 'الاتحاد',
 '8180.SR': 'الصقر للتأمين',
 '8190.SR': 'المتحدة للتأمين',
 '8200.SR': 'الإعادة السعودية',
 '8210.SR': 'بوبا العربية',
 '8230.SR': 'تكافل الراجحي',
 '8240.SR': 'تْشب',
 '8250.SR': 'جي آي جي',
 '8260.SR': 'الخليجية العامة',
 '8270.SR': 'بروج للتأمين',
 '8280.SR': 'ليفا',
 '8300.SR': 'الوطنية',
 '8310.SR': 'أمانة للتأمين',
 '8311.SR': 'عناية',
 '8313.SR': 'رسن',
'^TASI.SR': 'تاسي' }

import yfinance as yf
import pandas as pd
import streamlit as st


import yfinance as yf
import pandas as pd
import streamlit as st

def fetch_ticker_data(sector_tickers, ticker_names, sector, start_date, end_date):
    result_rows = []
    tickers = sector_tickers.get(sector, [])

    for ticker in tickers:
        try:
            # Fetch historical data using the download method
            historical_data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)

            # Flatten MultiIndex columns if they exist
            if isinstance(historical_data.columns, pd.MultiIndex):
                historical_data.columns = historical_data.columns.get_level_values(0)

            if historical_data.empty:
                st.write(f"No data available for ticker {ticker} for the selected period. The stock may have been enlisted after this date.")
                continue

            # Find the lowest closing price and its date
            min_close_date = historical_data['Low'].idxmin()
            min_close = historical_data.loc[min_close_date, 'Low']

            # Fetch the latest available data using the download method
            latest_data = yf.download(ticker, period="1d", auto_adjust=False)

            # Flatten MultiIndex for the latest data
            if isinstance(latest_data.columns, pd.MultiIndex):
                latest_data.columns = latest_data.columns.get_level_values(0)

            if latest_data.empty:
                st.write(f"No latest data available for ticker {ticker}.")
                continue

            latest_close = latest_data['Close'].iloc[-1]

            # Calculate percentage increase
            perc_increase = ((latest_close - min_close) / min_close) * 100

            # Append data to the results list
            result_rows.append({
                'القطاع': sector,
                'الرمز': ticker,
                'الشركة': ticker_names.get(ticker, "غير معروف"),
                'التاريخ': min_close_date.date(),
                'قاع الفترة المحددة': round(min_close, 2),
                'آخر اغلاق': round(latest_close, 2),
                'التغيير%': f"{perc_increase:.2f}%",
                'chg%': perc_increase  # For sorting
            })
        except Exception as e:
            st.write(f"An error occurred while fetching data for ticker {ticker}. Error: {e}")
            continue

    # Convert the results list to a Pandas DataFrame
    result_df = pd.DataFrame(result_rows)

    # Sort the DataFrame by the numeric percentage increase in descending order
    result_df = result_df.sort_values(by='chg%', ascending=False).reset_index(drop=True)

    # Drop the 'chg%' column (numeric percentage) from the user-facing output
    if not result_df.empty:
        result_df = result_df.drop(columns=['chg%'])

    return result_df

# Streamlit app interface
st.title("نسب ارتفاع وانخفاض الأسهم من تاريخ محدد")
st.markdown(' @telmisany - برمجة يحيى التلمساني')

# Select a sector
sector = st.selectbox("أختار قطاع", [''] + list(tasi.keys()))

# Select a date range
date_option = st.selectbox("اختر الفترة", ["قاع كورونا", "تاريخ آخر"])

if date_option == "تاريخ آخر":
    entered_date = st.date_input("اختر التاريخ")
    start_date = entered_date.strftime('%Y-%m-%d')
    end_date = start_date
else:
    start_date = "2020-03-01"
    end_date = "2020-04-01"

# Submit button
if st.button('Submit'):
    if sector:
        df = fetch_ticker_data(tasi, companies, sector, start_date, end_date)
        if not df.empty:
            st.dataframe(df)
        else:
            st.write("No data found for the selected sector and time period.")
    else:
        st.write("Please select a sector.")

st.write('\n')
st.markdown('[تطبيقات أخرى قد تعجبك](https://twitter.com/telmisany/status/1702641486792159334)')
# Add three empty lines for spacing
st.write('\n\n\n')
# Add a hyperlink to your Twitter account
st.markdown('[X تابعني في منصة](https://twitter.com/telmisany)')

# Buy me coffee AD:
image_url = 'https://i.ibb.co/WkHT8HP/buy-me-coffee_2.png'
link_url = 'https://www.buymeacoffee.com/y7iia'
st.markdown(f'<a href="{link_url}"><img src="{image_url}" alt="Image" width="200"/></a>', unsafe_allow_html=True)
