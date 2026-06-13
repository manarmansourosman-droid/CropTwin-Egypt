import streamlit as st
import pandas as pd
import joblib

# 1. إعدادات واجهة المستخدم والعناوين
st.set_page_config(page_title="CropTwin Egypt", page_icon="🌾", layout="centered")

st.title("🌾 نظام التؤامة الرقمية للتنبؤ بإنتاجية المحاصيل في مصر")
st.markdown("### CropTwin-Egypt: AI-Powered Yield Prediction")
st.write("قم بتعديل المؤشرات المناخية ونوع المحصول في الأسفل لمشاهدة التنبؤ الفوري للإنتاجية.")

# 2. تحميل الموديل وعواميد البيانات المحفوظة
@st.cache_resource
def load_model():
    model = joblib.load('crop_yield_model.pkl')
    columns = joblib.load('model_columns.pkl')
    return model, columns

try:
    model, model_columns = load_model()
    
    # 3. مدخلات المستخدم من خلال أزرار وسلايدرز تفاعلية
    st.subheader("📊 المؤشرات البيئية والمناخية")
    
    col1, col2 = st.columns(2)
    with col1:
        temp = st.slider("🌡️ متوسط درجة الحرارة (°C)", min_value=10.0, max_value=40.0, value=22.0, step=0.5)
        rain = st.slider("🌧️ معدل الأمطار السنوي (mm/year)", min_value=0.0, max_value=300.0, value=51.0, step=1.0)
    with col2:
        pesticides = st.number_input("🧪 كمية المبيدات المستخدمة (tonnes)", min_value=0.0, value=13214.0, step=100.0)
        crop_type = st.selectbox("🌱 اختر المحصول الاستراتيجي", ["Potatoes", "Wheat", "Maize"])

    # 4. زر التنبؤ ومعالجة البيانات المستلمة
    if st.button("🔮 احسب الإنتاجية المتوقعة الآن"):
        # بناء قاموس بيانات مساوٍ لعدد العواميد الأصلية
        input_data = {col: 0 for col in model_columns}
        
        # تعبئة القيم المستمرة المتغيرة
        input_data['avg_temp'] = temp
        input_data['average_rain_fall_mm_per_year'] = rain
        input_data['pesticides_tonnes'] = pesticides
        
        # تفعيل المحصول المختار بناءً على الـ One-Hot Encoding
        crop_column = f"Item_{crop_type}"
        if crop_column in input_data:
            input_data[crop_column] = 1
            
        # تحويل القاموس إلى DataFrame بنفس الترتيب الذي تدرب عليه الموديل
        sample_df = pd.DataFrame([input_data])[model_columns]
        
        # تنفيذ التنبؤ
        prediction = model.predict(sample_df)[0]
        
        # عرض النتائج بشكل تفاعلي مبهر
        st.success(f"🎯 الإنتاجية المتوقعة لـمحصول **{crop_type}** هي:")
        st.metric(label="Expected Yield (hg/ha)", value=f"{prediction:,.2f}")
        
        # لمسة توجيهية زراعية للمستخدم
        if prediction < 150000:
            st.warning("⚠️ تحذير: المؤشرات البيئية الحالية قد تؤدي لانخفاض الإنتاجية. يُرجى مراجعة نظم الري والتسميد.")
        else:
            st.info("🚀 مؤشرات مناخية ممتازة ومثالية لتحقيق الإنتاجية المستهدفة في المشاريع القومية.")

except FileNotFoundError:
    st.error("❌ لم يتم العثور على ملفات الموديل المحفوظة. يرجى تشغيل سطر الحفظ (joblib) من النوت بوك أولاً لتصدير الموديل!")
    