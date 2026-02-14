import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. إعداد الصفحة
st.set_page_config(page_title="For Umm Al-Baraa", page_icon="❤️", layout="centered")

# 2. تخصيص الـ CSS (الوضع الأبيض الأكاديمي)
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
        color: #b71c1c; /* أحمر غامق */
        text-align: center;
        margin-bottom: 5px;
    }
    
    /* تنسيق الإهداء */
    .dedication {
        font-family: 'Amiri', serif;
        color: #b8860b; /* ذهبي داكن */
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: bold;
        margin-bottom: 30px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* تنسيق المعادلة */
    .katex {
        font-size: 2rem !important;
        color: #000000 !important; /* أسود */
        font-family: 'Times New Roman', serif;
    }
    
    /* صندوق توضيحي للمعادلة */
    .math-label {
        color: #555;
        font-family: 'Amiri', serif;
        font-size: 1.2rem;
        text-align: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. العناوين والإهداء (تمت إضافة القلب هنا)
st.title("Happy Valentine's Day") 
st.markdown('<div class="dedication">❤️إهداء إلى أم البراء❤️</div>', unsafe_allow_html=True)

# 4. المعادلة (استخدام st.latex المباشر لحل مشكلة العرض)
st.markdown('<p class="math-label">السر الرياضي (The Equation):</p>', unsafe_allow_html=True)

# عرض المعادلة
st.latex(r"""
y = x^{\frac{2}{3}} + 0.9 \sin(\textcolor{#b71c1c}{k} x) \sqrt{3 - x^2}
""")

# 5. التحكم (Slider)
k = st.slider("اضبطي التردد (k) ليكتمل الرسم:", 0.0, 200.0, 5.0, 0.5)

# 6. الحسابات
x = np.linspace(-1.75, 1.75, 8000)
y = np.cbrt(x**2) + 0.9 * np.sin(k * x) * np.sqrt(3 - x**2)

# 7. الرسم (Plotly)
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x, y=y,
    mode='lines',
    line=dict(color='#d50000', width=2), # أحمر واضح
    name='Heart',
    hoverinfo='none'
))

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False, visible=False, range=[-2.5, 2.5]),
    yaxis=dict(showgrid=False, visible=False, range=[-1.5, 2.5]),
    margin=dict(l=0, r=0, t=0, b=0),
    height=450,
)

st.plotly_chart(fig, use_container_width=True)

# 8. مفاجأة الختام
if k > 150:
    st.balloons()
    st.markdown("""
    <div style='text-align: center; color: #333; font-family: Amiri; font-size: 1.8rem; margin-top: 10px;'>
    كل عام وأنتِ قلبي ومعادلتي الثابتة ❤️
    </div>
    """, unsafe_allow_html=True)
