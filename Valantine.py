import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. إعداد الصفحة
st.set_page_config(page_title="For Umm Al-Baraa", page_icon="❤️", layout="centered")

# 2. تخصيص الـ CSS (الجانب الجمالي)
st.markdown("""
    <style>
    /* استيراد خط عربي جميل */
    @import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@1,400;1,700&display=swap');
    
    /* خلفية التطبيق */
    .stApp {
        background-color: #0e1117;
    }
    
    /* تنسيق العنوان */
    h1 {
        font-family: 'Amiri', serif;
        color: #ff4b4b;
        text-align: center;
        font-size: 3rem !important;
        margin-bottom: 5px;
    }
    
    /* تنسيق الإهداء الخاص - تم التكبير والتحسين */
    .dedication {
        font-family: 'Amiri', serif;
        color: #D4AF37; /* ذهبي */
        text-align: center;
        font-size: 4rem !important; /* حجم ضخم */
        font-weight: bold;
        margin-top: -10px;
        margin-bottom: 30px;
        text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.5); /* توهج خفيف */
    }
    
    /* تنسيق صندوق المعادلة */
    .equation-container {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #333;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .katex { font-size: 1.5em !important; } /* تكبير رموز الرياضيات */
    </style>
""", unsafe_allow_html=True)

# 3. العناوين والإهداء
st.title("Happy Valentine's Day")
st.markdown('<div class="dedication">إهداء إلى أم البراء</div>', unsafe_allow_html=True)

# 4. الجانب التقني (عرض المعادلة بشكل صحيح داخل HTML)
# نستخدم $$ ... $$ داخل Markdown ليتم معالجتها كـ LaTeX
st.markdown(r"""
<div class="equation-container">
    <p style="color: #bbb; font-family: 'Amiri'; font-size: 1.2rem; margin-bottom: 10px;">
        السر الرياضي (The Mathematical Heart):
    </p>
    <div style="color: white;">
        $$
        y = x^{\frac{2}{3}} + 0.9 \sin(\textcolor{#ff4b4b}{k} x) \sqrt{3 - x^2}
        $$
    </div>
</div>
""", unsafe_allow_html=True)

# 5. التحكم (Slider)
k = st.slider("مستوى الحب (Frequency k)", 0.0, 200.0, 5.0, 0.5)

# 6. الحسابات الرياضية
x = np.linspace(-1.75, 1.75, 7000)
# معادلة القلب
y = np.cbrt(x**2) + 0.9 * np.sin(k * x) * np.sqrt(3 - x**2)

# 7. الرسم باستخدام Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x, y=y,
    mode='lines',
    line=dict(color='#ff1744', width=1.5),
    name='Heart Wave',
    hoverinfo='none'
))

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False, zeroline=False, visible=False, range=[-2.5, 2.5]),
    yaxis=dict(showgrid=False, zeroline=False, visible=False, range=[-1.5, 2.5]),
    margin=dict(l=0, r=0, t=0, b=0),
    height=450,
)

st.plotly_chart(fig, use_container_width=True)

# 8. رسالة الختام
if k > 150:
    st.balloons()
    st.markdown("""
    <div style='text-align: center; color: white; font-family: Amiri; font-size: 2rem;'>
    اكتملت المعادلة.. واكتمل القلب! ❤️
    </div>
    """, unsafe_allow_html=True)
