import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta 

# Create a dictionary of ticker symbols to company names
companies = {
 '1010.SR': 'الرياض',
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
 '1201.SR': 'تكوين ',
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
 '2090.SR': 'جبسكو',
 '2100.SR': 'وفرة',
 '2110.SR': 'الكابلات',
 '2120.SR': 'المتطورة',
 '2130.SR': 'صدق',
 '2140.SR': 'أيان للاستثمار',
 '2150.SR': 'زجاج',
 '2160.SR': 'أميانتيت ',
 '2170.SR': 'اللجين القابضة',
 '2180.SR': 'فيبكو',
 '2190.SR': 'سيسكو القابضة',
 '2200.SR': 'أنابيب *',
 '2210.SR': 'نماء للكيماويات',
 '2220.SR': 'معدنية ',
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
 '2300.SR': 'صناعة الورق ',
 '2310.SR': 'سبكيم العالمية',
 '2320.SR': 'البابطين',
 '2330.SR': 'المتقدمة',
 '2340.SR': 'العبداللطيف',
 '2350.SR': 'كيان السعودية',
 '2360.SR': 'الفخارية',
 '2370.SR': 'مسك',
 '2380.SR': 'بترو رابغ ',
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
 '4014.SR': 'دار المعدات ',
 '4015.SR': 'جمجوم فارما',
 '4016.SR': 'أفالون فارما',
 '4020.SR': 'العقارية',
 '4030.SR': 'البحري',
 '4031.SR': 'الخدمات الأرضية',
 '4040.SR': 'سابتكو ',
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
 '4130.SR': 'الباحة ',
 '4140.SR': 'صادرات',
 '4141.SR': 'العمران',
 '4142.SR': 'كابلات الرياض',
 '4150.SR': 'التعمير',
 '4160.SR': 'ثمار ',
 '4161.SR': 'بن داود',
 '4162.SR': 'المنجم للأغذية',
 '4163.SR': 'الدواء',
 '4164.SR': 'النهدي',
 '4170.SR': 'شمس ',
 '4180.SR': 'مجموعة فتيحي',
 '4190.SR': 'جرير',
 '4191.SR': 'أبو معطي',
 '4192.SR': 'السيف غاليري',
 '4200.SR': 'الدريس',
 '4210.SR': 'الأبحاث و الإعلام',
 '4220.SR': 'إعمار ',
 '4230.SR': 'البحر الأحمر ',
 '4240.SR': 'الحكير',
 '4250.SR': 'جبل عمر',
 '4260.SR': 'بدجت السعودية',
 '4261.SR': 'ذيب',
 '4262.SR': 'لومي',
 '4263.SR': 'سال',
 '4270.SR': 'طباعة وتغليف',
 '4280.SR': 'المملكة ',
 '4290.SR': 'الخليج للتدريب',
 '4291.SR': 'الوطنية للتربية والتعليم',
 '4292.SR': 'عطاء التعليمية',
 '4300.SR': 'دار الأركان',
 '4310.SR': 'مدينة المعرفة',
 '4320.SR': 'الأندلس العقارية',
 '4321.SR': 'المراكز العربية',
 '4322.SR': 'رتال',
 '4323.SR': 'سمو ',
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
 '6040.SR': 'تبوك الزراعية ',
 '6050.SR': 'الأسماك ',
 '6060.SR': 'الشرقية للتنمية',
 '6070.SR': 'الجوف',
 '6090.SR': 'جازادكو',
 '7010.SR': 'اس تي سي',
 '7020.SR': 'إتحاد إتصالات',
 '7030.SR': 'زين السعودية ',
 '7040.SR': 'عذيب للاتصالات',
 '7200.SR': 'ام آي اس',
 '7201.SR': 'بحر العرب',
 '7202.SR': 'سلوشنز',
 '7203.SR': 'عِلم',
 '7204.SR': 'توبي',
 '8010.SR': 'التعاونية',
 '8012.SR': 'جزيرة تكافل',
 '8020.SR': 'ملاذ للتأمين',
 '8030.SR': 'ميدغلف للتأمين ',
 '8040.SR': 'أليانز إس إف',
 '8050.SR': 'سلامة',
 '8060.SR': 'ولاء للتأمين',
 '8070.SR': 'الدرع العربي',
 '8100.SR': 'سايكو ',
 '8120.SR': 'إتحاد الخليج الأهلية ',
 '8150.SR': 'أسيج ',
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
 '8310.SR': 'أمانة للتأمين ',
 '8311.SR': 'عناية'}

# Function to fetch stock data and evaluate the analyst's recommendation
def evaluate_analyst_recommendation(ticker, target_date, target_price, analyst_name, company_name):
    try:
        # Define the end date as one year from the target date
        end_date = target_date + timedelta(days=365)

        # Fetch historical stock data from target date to end date
        stock_data = yf.download(ticker, start=target_date, end=end_date)

        if not stock_data.empty:
            # Calculate highest and lowest price and the return since the target date
            highest_price = stock_data['High'].max()
            lowest_price = stock_data['Low'].min()
            highest_date = stock_data['High'].idxmax()
            lowest_date = stock_data['Low'].idxmin()
            initial_price = stock_data.iloc[0]['Open']
            highest_return = ((highest_price - initial_price) / initial_price) * 100
            lowest_return = ((lowest_price - initial_price) / initial_price) * 100

            # Check if and when the target was achieved within the year
            target_achieved = stock_data['High'] >= target_price
            if target_achieved.any():
                target_achieved_date = stock_data[target_achieved].index[0]
                days_to_target = (target_achieved_date - target_date).days
                target_reached = 'نعم'
            else:
                target_achieved_date = None
                days_to_target = None
                target_reached = 'لا'

            # Create a results DataFrame
            result_data = {
                'اسم المحلل': analyst_name,
                'اسم الشركة': company_name,
                'السعر المستهدف': target_price,
                'تحقق الهدف ؟': target_reached,
                'أعلى سعر تم الوصول إليه': highest_price,
                'تاريخ الأعلى سعر': highest_date.strftime('%Y-%m-%d'),
                'العائد إلى الأعلى سعر %': highest_return,
                'أدنى سعر تم الوصول إليه': lowest_price,
                'تاريخ الأدنى سعر': lowest_date.strftime('%Y-%m-%d'),
                'العائد إلى الأدنى سعر %': lowest_return,
                'عدد الأيام لتحقيق الهدف': days_to_target if days_to_target is not None else "لم يتحقق الهدف خلال السنة"
            }
            return pd.DataFrame([result_data])
        else:
            return "No data available for the selected stock and date range."
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit interface code
st.title('تقييم توصيات المحللين الفنية')
st.sidebar.header('مدخلات المستخدم')

# User inputs
ticker = st.text_input('رمز السهم', value='1010.SR')
target_date = st.date_input('تاريخ التوصية', datetime.now())
target_price = st.number_input('السعر المستهدف', value=100.0)
analyst_name = st.text_input('اسم المحلل')
company_name = companies.get(ticker, 'Unknown Company')



if st.sidebar.button('تقييم التوصية'):
    result = evaluate_analyst_recommendation(ticker, target_date, target_price, analyst_name, company_name)
    if isinstance(result, pd.DataFrame):
        st.write(result)
    else:
        st.error(result)

# Links and advertisements
st.markdown('[تطبيقات أخرى قد تعجبك](https://twitter.com/telmisany/status/1702641486792159334)')
# Add three empty lines for spacing
st.write('\n\n\n')
# Add a hyperlink to your Twitter account
st.markdown('[X تابعني في منصة](https://twitter.com/telmisany)')

# Buy me coffee AD:
image_url = 'https://i.ibb.co/dM0tT0f/buy-me-coffee.png'
link_url = 'https://www.buymeacoffee.com/y7iia'
st.markdown(f'<a href="{link_url}"><img src="{image_url}" alt="Image" width="200"/></a>', unsafe_allow_html=True)
