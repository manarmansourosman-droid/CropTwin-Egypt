import streamlit as st
import pandas as pd
import joblib
import time

# 1. إعدادات واجهة المستخدم والعناوين الجمالية
st.set_page_config(
    page_title="CropTwin Egypt", 
    page_icon="🌾", 
    layout="wide"  # جعل التصميم عريض ومريح للعين
)

# تصميم العنوان الرئيسي في منتصف الصفحة
st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🌾 نظام التؤامة الرقمية للتنبؤ بإنتاجية المحاصيل في مصر</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555;'>CropTwin-Egypt: AI-Powered Yield Prediction</h3>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

# 2. تحميل الموديل وعواميد البيانات في الخلفية
@st.cache_resource
def load_model():
    model = joblib.load('crop_yield_model.pkl')
    columns = joblib.load('model_columns.pkl')
    return model, columns

try:
    model, model_columns = load_model()

    # ==================== الفكرة رقم 1: الشريطة الجانبية (Sidebar) ====================
    with st.sidebar:
        st.markdown("<h2 style='color: #2E7D32;'>⚙️ لوحة التحكم والمدخلات</h2>", unsafe_allow_html=True)
        st.write("قم بتعديل المؤشرات البيئية والمناخية لمحاكاة سيناريوهات الطقس:")
        
        # المدخلات جوه الـ Sidebar
        temp = st.slider("🌡️ متوسط درجة الحرارة (°C)", min_value=10.0, max_value=40.0, value=22.0, step=0.5)
        rain = st.slider("🌧️ معدل الأمطار السنوي (mm/year)", min_value=0.0, max_value=300.0, value=51.0, step=1.0)
        pesticides = st.number_input("🧪 كمية المبيدات المستخدمة (tonnes)", min_value=0.0, value=13214.0, step=100.0)
        crop_type = st.selectbox("🌱 اختر المحصول الاستراتيجي", ["Potatoes", "Wheat", "Maize"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        # زر الحساب بشكل بارز في الجنب
        predict_btn = st.button("🚀 احسب الإنتاجية المتوقعة الآن", use_container_width=True)

    # ==================== الفكرة رقم 3: المخرجات داخل كروت منظمة ====================
    # الشاشة الرئيسية (اليمين) هتعرض النتائج
    if predict_btn:
        # لمسة احترافية: تحميل ذكي يوحي بالمعالجة الحقيقية
        with st.spinner('🔄 يقوم الذكاء الاصطناعي الآن بتحليل البيانات ومحاكاة السيناريو...'):
            time.sleep(1) # تأخير ثانية واحدة للحركة الجمالية
        
        # بناء قاموس البيانات المستلمة بنفس الترتيب
        input_data = {col: 0 for col in model_columns}
        input_data['avg_temp'] = temp
        input_data['average_rain_fall_mm_per_year'] = rain
        input_data['pesticides_tonnes'] = pesticides
        
        # تفعيل الـ One-Hot Encoding للمحصول المختارات
        crop_column = f"Item_{crop_type}"
        if crop_column in input_data:
            input_data[crop_column] = 1
            
        # تحويل القاموس إلى DataFrame بنفس ترتيب الأعمدة الأصلي
        sample_df = pd.DataFrame([input_data])[model_columns]
        
        # تنفيذ التنبؤ
        prediction = model.predict(sample_df)[0]
        
        # عرض النتيجة جوه كرت كبير ومنظم (Card Design)
        st.markdown(f"""
            <div style="background-color: #f0f7f4; padding: 25px; border-radius: 15px; border-left: 8px solid #2E7D32; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);">
                <h4 style="color: #2E7D32; margin: 0;">📊 النتيجة والإنتاجية المتوقعة لمحصول <b>{crop_type}</b>:</h4>
                <p style="font-size: 42px; font-weight: bold; color: #1B5E20; margin: 15px 0 5px 0;">{prediction:,.2f} <span style="font-size: 20px; color: #555;">hg/ha</span></p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # لمسة توجيهية زراعية ذكية حسب النتيجة بتغيير ألوان الكروت التنبيهية
        if prediction < 150000:
            st.warning(f"⚠️ **تحذير هندسي:** المؤشرات البيئية والمناخية الحالية قد تؤدي لانخفاض ملحوظ في الإنتاجية متأثرة بظروف الطقس (الحرارة: {temp}°C، الأمطار: {rain}mm). يُرجى مراجعة وتعديل استراتيجيات الري والتسميد فوراً لحماية المحصول.")
        else:
            st.success(f"✨ **تقرير إيجابي:** المؤشرات المناخية والبيئية المدخلة ممتازة ومثالية جداً لتحقيق أعلى كفاءة إنتاجية مستهدفة للمحصول في المشاريع القومية لجمهورية مصر العربية.")

    else:
        # الرسالة الترحيبية المبدئية قبل الضغط على الزر
        st.info("💡 **مرحباً بك في نظام CropTwin:** من فضلك قم بضبط المؤشرات المناخية والبيئية من **القائمة الجانبية على اليسار**، ثم اضغط على زر **احسب الإنتاجية المتوقعة** لعرض التوأمة الرقمية الفورية.")

except FileNotFoundError:
    st.error("❌ **خطأ في النظام:** لم يتم العثور على ملفات الموديل المحفوظة (`crop_yield_model.pkl` أو `model_columns.pkl`). يرجى التأكد من تشغيل سطر الحفظ في الـ Jupyter Notebook أولاً!")