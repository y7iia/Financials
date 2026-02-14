import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="Valentine Heart", page_icon="❤️")

# العنوان والمعادلة
st.title("Happy Valentine's Day! ❤️")
st.latex(r"y = x^{\frac{2}{3}} + 0.9 \sin(kx) \sqrt{3 - x^2}")

# شريط التمرير لقيمة k
# المدى من 0 إلى 200 لمحاكاة تأثير التعبئة
k = st.slider("قيمة التردد (k)", min_value=0.0, max_value=200.0, value=10.0, step=0.5)

# الحسابات الرياضية
# المجال من -جذر(3) إلى +جذر(3)
x = np.linspace(-np.sqrt(3), np.sqrt(3), 10000)

# حساب الدالة: استخدام الجذر التكعيبي لتربيع x لتفادي مشاكل الأعداد السالبة
y = np.cbrt(x**2) + 0.9 * np.sin(k * x) * np.sqrt(3 - x**2)

# الرسم البياني
fig, ax = plt.subplots(figsize=(8, 8))

# تطبيق الثيم المظلم لمحاكاة الصورة الأصلية
plt.style.use('dark_background')
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# رسم الخط
ax.plot(x, y, color='#ff3333', linewidth=0.8)

# تنسيق المحاور
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-1.5, 2.5)
ax.grid(True, alpha=0.3, linestyle='--') # شبكة خفيفة
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# عرض الرسم في ستريم ليت
st.pyplot(fig)
