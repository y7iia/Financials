import streamlit as st

# Custom CSS for visual enhancements
st.markdown("""
    <style>
        .title {
            font-size: 2.5em;
            color: red;
            text-align: center;
            margin-bottom: 10px;
        }
        .description {
            font-size: 1.25em;
            color: #666;
            text-align: center;
            margin-bottom: 20px;
        }
        .new-badge {
            background-color: #FFC107;
            color: white;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 0.75em;
            margin-left: 5px;
        }
        .button {
            width: 100%;
            padding: 15px;
            font-size: 1.1em;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .profile-pic {
            display: block;
            margin-left: auto;
            margin-right: auto;
            border-radius: 50%;
            width: 150px;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="title">تطبيقات بايثون لأسواق الأسهم</div>', unsafe_allow_html=True)
st.markdown('<div class="description">أدوات مالية متكاملة للمستثمرين في أسواق المال، تساعدك على اتخاذ قرارات استثمارية ذكية ومدروسة</div>', unsafe_allow_html=True)

# profile picture
profile_pic_url = "https://pbs.twimg.com/profile_images/1689517781669007360/oIga1frq_400x400.jpg"
st.markdown(f'<img src="{profile_pic_url}" alt="Profile Picture" class="profile-pic">', unsafe_allow_html=True)
st.markdown('برمجة يحيى التلمساني')
# Add a hyperlink to your Twitter account
st.markdown('[X تابعني في منصة](https://twitter.com/telmisany)')

# Button grid
app_links = [
    ("الأرباح المبقاة للشركات", "https://retainedincome.streamlit.app/"),
    ("حاسبة دعوم ومقاومات الأسهم", "https://support-resistance-levels.streamlit.app/"),
    ("توصيات المحللين", "https://tickerstargets.streamlit.app/#analyst-recommendations"),
    ("القيمة العادلة للأسهم بطريقة جراهام", "https://otherfinancials-z8jg3khd9ka2igdzqjvxbw.streamlit.app/"),
    ("القوائم المالية (غير معرب)", "https://tasi-financials.streamlit.app/"),
    ("النتائج المالية", "https://net-income.streamlit.app/"),
    ("التوزيعات النقدية", "https://tasi-dividents.streamlit.app/"),
    ("نسبة تغير أسعار الأسهم من قاع كورونا 2020", "https://corona-return.streamlit.app/"),
    ("تقييم توصيات المحللين", "https://corona-return.streamlit.app/"),
    ("المحلل الرقمي (قريبا)", ""),
]

# Indicate new apps (separated by ,)
new_apps = ["تقييم توصيات المحللين"]

# Create a 2x5 grid using Streamlit's columns
columns = st.columns(2)
for i, (app_name, link) in enumerate(app_links):
    col = columns[i % 2]  # Alternate between left and right columns
    with col:
        if app_name in new_apps:
            st.markdown(
                f'<a href="{link}" target="_blank">'
                f'<button class="button">{app_name} <span class="new-badge">NEW</span></button>'
                f'</a>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<a href="{link}" target="_blank">'
                f'<button class="button">{app_name}</button>'
                f'</a>',
                unsafe_allow_html=True,
            )

# Add three empty lines for spacing
st.write('\n\n\n')

# Buy me coffee AD:
image_url = 'https://i.ibb.co/dM0tT0f/buy-me-coffee.png'
link_url = 'https://www.buymeacoffee.com/y7iia'
st.markdown(f'<a href="{link_url}"><img src="{image_url}" alt="Image" width="200"/></a>', unsafe_allow_html=True)
