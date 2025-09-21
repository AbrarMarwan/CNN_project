import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="تحليل مشاعر الأطفال", layout="centered")
st.title("🎈 تحليل مشاعر الأطفال من الصور")
st.write("ارفع صورة وسيتم إرسالها إلى النموذج لتحليل المشاعر.")

uploaded_file = st.file_uploader("📷 اختر صورة", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="الصورة الأصلية", use_column_width=True)

    # إرسال الصورة إلى API
    files = {'image': uploaded_file.getvalue()}
    response = requests.post("http://127.0.0.1:5000/predict", files={'image': uploaded_file})

    if response.status_code == 200:
        result = response.json()
        st.markdown(f"### 🎯 المشاعر المتوقعة: `{result['predicted_class']}`")
        st.progress(result['confidence'] / 100)
        st.write(f"نسبة الثقة: **{result['confidence']:.2f}%**")
    else:
        st.error("حدث خطأ أثناء الاتصال بالـ API.")
