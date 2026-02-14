import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. إعداد الصفحة
st.set_page_config(page_title="For Umm Al-Baraa", page_icon="❤️", layout="centered")

# 2. تخصيص الـ CSS (الجماليات والخطوط)
st.markdown("""
    <style>
    /* استيراد الخط العربي */
    @import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@1,400;1,700&display=swap');
    
    .stApp {
        background-color: #0e1117;
    }
    
    h1 {
        font-family: 'Amiri', serif;
        color: #ff4b4b;
        text-align: center;
        margin-bottom: 5px;
    }
    
    /* تنسيق الإهداء الفاخر */
    .dedication {
        font-family: 'Amiri', serif;
        color: #D4AF37; /* Gold */
        text-align: center;
        font-size: 3.8rem !important;
        font-weight: bold;
        margin-top: -15px;
        margin-bottom: 20px;
        text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.6);
    }
    
    /* تنسيق صندوق المعادلة ليظهر بشكل احترافي */
    .equation-box {
        background-color: #1a1c24;
        border: 1px solid #444;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .equation-label {
        color: #aaa;
        font-family: 'Amiri', serif;
        font-size: 1.4rem;
        margin-bottom: 5px;
        text-align: center;
    }
    
    /* إجبار رموز الرياضيات على اللون الأبيض والحجم الكبير */
    .katex {
        font-size: 2.2rem !important;
        color: white !important;
        font-family: 'Times New Roman', serif;
    }
    
    /* تحسين شكل السلايدر */
    .stSlider > div > div > div > div {
        color: #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

# 3. العناوين والإهداء
st.title("Happy Valentine's Day")
st.markdown('<div class="dedication">إهداء إلى أم البراء</div>', unsafe_allow_html=True)

# 4. المعادلة (الآن مفصولة لتظهر بشكل صحيح)
st.markdown('<p class="equation-label">السر الرياضي (The Math):</p>', unsafe_allow_html=True)

# استخدام st.latex مباشرة يضمن ظهورها بشكل صحيح
# \color{color_name} تستخدم لتلوين أجزاء من المعادلة
st.latex(r"""
y = \underbrace{x^{\frac{2}{3}}}_{\text{Shape}} + 0.9 \sin(\textcolor{#ff4b4b}{k} x) \sqrt{3 - x^2}
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
    line=dict(color='#ff1744', width=1.5),
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
    <div style='text-align: center; color: white; font-family: Amiri; font-size: 1.8rem; margin-top: 10px;'>
    كل عام وأنتِ قلبي ومعادلتي الثابتة ❤️
    </div>
    """, unsafe_allow_html=True)
