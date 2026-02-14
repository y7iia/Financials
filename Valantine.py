import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. إعداد الصفحة
st.set_page_config(page_title="For Umm Al-Baraa", page_icon="❤️", layout="centered")

# 2. تخصيص الـ CSS (الوضع الفاتح - Light Mode)
st.markdown("""
    <style>
    /* استيراد الخط العربي */
    @import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@1,400;1,700&display=swap');
    
    /* خلفية بيضاء */
    .stApp {
        background-color: #ffffff;
    }
    
    /* تنسيق العنوان الرئيسي */
    h1 {
        font-family: 'Amiri', serif;
        color: #d32f2f; /* أحمر داكن قليلاً للوضوح */
        text-align: center;
        margin-bottom: 5px;
    }
    
    /* تنسيق الإهداء - ذهبي داكن ليناسب الأبيض */
    .dedication {
        font-family: 'Amiri', serif;
        color: #b8860b; /* Dark Goldenrod */
        text-align: center;
        font-size: 3.8rem !important;
        font-weight: bold;
        margin-top: -15px;
        margin-bottom: 20px;
        /* ظل خفيف للنص بدلاً من التوهج */
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    /* صندوق المعادلة - خلفية رمادية فاتحة جداً */
    .equation-box {
        background-color: #f8f9fa; /* رمادي فاتح جداً */
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .equation-label {
        color: #555; /* رمادي داكن */
        font-family: 'Amiri', serif;
        font-size: 1.4rem;
        margin-bottom: 10px;
        text-align: center;
    }
    
    /* إجبار رموز الرياضيات على اللون الأسود */
    .katex {
        font-size: 2.2rem !important;
        color: #000000 !important; /* أسود */
        font-family: 'Times New Roman', serif;
    }
    
    /* تحسين لون السلايدر */
    .stSlider > div > div > div > div {
        color: #d32f2f;
    }
    </style>
""", unsafe_allow_html=True)

# 3. العناوين والإهداء
st.title("Happy Valentine'
