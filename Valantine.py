import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. إعداد الصفحة وتصميمها
st.set_page_config(page_title="For Umm Al-Baraa", page_icon="🌹", layout="centered")

# 2. حقن كود CSS لتخصيص التصميم (Custom Styling)
# هذا الجزء يجعل النصوص تظهر في المنتصف ويغير نوع الخط
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@1,700&display=swap');
    
    .main {
        background-color: #0e1117;
    }
    h1 {
        font-family: 'Amiri', serif;
        color: #ff4b4b;
        text-align: center;
        font-size: 3.5rem !important;
        text-shadow: 2px 2px 4px #000000;
    }
    .subtitle {
        font-family: 'Amiri', serif;
        color: #d4af37; /* Gold Color */
        text-align: center;
        font-size: 2.2rem;
        margin-bottom: 20px;
    }
    .stSlider {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. العناوين المخصصة
st.title("❤️ Happy Valentine's Day ❤️")
st.markdown('<p class="subtitle">إهداء إلى أم البراء</p>', unsafe_allow_html=True)

# 4. شريط التحكم (Slider)
k = st.slider("مستوى الحب (Frequency k)", 0.0, 150.0, 5.0, 0.5)

# 5. الحسابات الرياضية (NumPy Vectorization)
x = np.linspace(-1.8, 1.8, 5000) # تقليل النقاط قليلاً لزيادة سلاسة الحركة في المتصفح
# معادلة القلب: استخدام np.cbrt للجذر التكعيبي لتجنب الأخطاء مع الأرقام السالبة
y = np.cbrt(x**2) + 0.9 * np.sin(k * x) * np.sqrt(3 - x**2)

# 6. الرسم باستخدام Plotly (أفضل بصرياً)
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x, y=y,
    mode='lines',
    line=dict(color='#ff0055', width=2), # لون أحمر وردي
    name='Heart'
))

# إخفاء المحاور والخلفية لتركيز النظر على القلب فقط
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False, zeroline=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, visible=False),
    margin=dict(l=0, r=0, t=0, b=0),
    height=500,
    shapes=[
        # إضافة إطار خفيف أو توهج (اختياري)
    ]
)

st.plotly_chart(fig, use_container_width=True)

# مفاجأة عند اكتمال القلب
if k > 140:
    st.balloons()
    st.markdown("<h3 style='text-align: center; color: white;'>اكتمل القلب! ❤️</h3>", unsafe_allow_html=True)
