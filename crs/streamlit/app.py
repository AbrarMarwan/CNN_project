import streamlit as st

st.set_page_config(page_title="تحليل مشاعر الأطفال", layout="centered")

import requests
from PIL import Image
import base64

# إعداد خلفية بصورة
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .glass-box {{
        background-color: rgba(0, 0, 0, 0.5);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        margin-top: 30px;
    }}
    .glass-box h1, .glass-box p, .glass-box label {{
        color: white !important;
        font-weight: bold;
    }}

    /* تكبير زر اختيار الملف */
    .stFileUploader label {{
        color: white !important;
        font-size: 18px !important;
        font-weight: bold;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# خلفية
set_background("background.webp")


# عنوان
st.markdown("""
<div class="glass-box">
    <h1 style="text-align: center;">🎈 تحليل مشاعر الأطفال من الرسومات</h1>
    <p style="text-align: center; font-size: 18px;">
        ارفع رسمة لطفل وسنقوم بتحليل المشاعر المعبّرة فيها باستخدام الذكاء الاصطناعي.
    </p>
</div>
""", unsafe_allow_html=True)

# رفع الصورة
st.markdown("### 🎨 اختر رسمة الطفل")

uploaded_file = st.file_uploader("اختر ملف", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

# زر التحليل
analyze_button = st.button("🔍 تحليل المشاعر")
st.markdown('</div>', unsafe_allow_html=True)

# عند الضغط
if analyze_button and uploaded_file is not None:
    st.image(uploaded_file, caption="📸 الرسمة المختارة", use_column_width=True)

    # إرسال API
    files = {'image': uploaded_file.getvalue()}
    response = requests.post("http://127.0.0.1:5000/predict", files={'image': uploaded_file})

    if response.status_code == 200:
        result = response.json()
        emotion = result['predicted_class']
        confidence = result['confidence']

         
        st.markdown("### 🎯 النتيجة المتوقعة:")

        if emotion == "Happy":
            st.success(f"😊 الطفل يبدو سعيدًا بنسبة ثقة {confidence:.2f}%")
        elif emotion == "Sad":
            st.warning(f"😢 الطفل يبدو حزينًا بنسبة ثقة {confidence:.2f}%")
        elif emotion == "Angry":
            st.error(f"😠 الطفل يبدو غاضبًا بنسبة ثقة {confidence:.2f}%")
        else:
            st.warning(f"😢 الطفل يبدو خائفًا بنسبة ثقة {confidence:.2f}%")

         
        st.progress(confidence / 100)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("❌ حدث خطأ أثناء الاتصال بالـ API.")
elif analyze_button and uploaded_file is None:
    st.warning("📌 الرجاء رفع رسمة قبل الضغط على زر التحليل.")
