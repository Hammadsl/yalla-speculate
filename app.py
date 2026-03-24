import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. إعداد الصفحة والنمط البصري الفاخر (Dark UI)
st.set_page_config(page_title="YALLA SCALP PRO", layout="wide")

st.markdown("""
    <style>
    /* خلفية المنصة باللون الداكن العميق */
    .main { background-color: #0b0e14; color: #e1e1e1; }
    /* تنسيق الحاويات (المربعات) */
    .stMetric, .css-1r6slb0, .stButton>button {
        background-color: #1a1f29 !important;
        border: 1px solid #2d343f !important;
        border-radius: 10px !important;
        color: white !important;
    }
    /* شريط البحث */
    .stTextInput>div>div>input {
        background-color: #1a1f29;
        color: #00ffcc;
        border: 1px solid #00ffcc;
        text-align: center;
    }
    h1 { color: #ffffff; text-shadow: 2px 2px #000000; text-align: center; }
    .target-box { background: linear-gradient(90deg, #1a1f29, #252b36); padding: 20px; border-radius: 15px; border-left: 5px solid #00ffcc; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. رأس المنصة
st.markdown("<h1>💎 YALLA SCALP PRO</h1>", unsafe_allow_html=True)

# 3. محرك البحث الذكي (يميناً في الأعلى)
col_search_1, col_search_2, col_search_3 = st.columns([1, 2, 1])
with col_search_2:
    ticker = st.text_input("🔍 ابحث عن الشركة (بالعربي أو الرمز الإنجليزي):", placeholder="مثال: الراجحي أو 1120")

# محاكاة لبيانات الأسهم (هنا يتم ربط البحث بالنتائج)
if ticker:
    # تخصيص الصفحة للسهم المبحوث عنه فقط
    st.markdown(f"<h2 style='text-align:center; color:#00ffcc;'>تحليل سهم: {ticker}</h2>", unsafe_allow_html=True)
    
    # تقسيم الواجهة: يسار (بيانات وأهداف) - يمين (حاسبة وأخبار)
    col_left, col_mid, col_right = st.columns([1.5, 3, 1.5])

    # --- العمود الأيمن: حاسبة الأرباح والأخبار ---
    with col_right:
        st.markdown("### 🧮 حاسبة الأرباح")
        price_in = st.number_input("سعر الشراء", value=70.00)
        amount = st.number_input("عدد الأسهم", value=1000)
        target_val = st.number_input("سعر البيع المتوقع", value=85.00)
        profit = (target_val - price_in) * amount
        st.success(f"الربح الإجمالي: {profit:,.2f} $")
        
        st.markdown("---")
        st.markdown("### 📰 أخبار السوق")
        st.caption("📈 تدفق سيولة ضخمة في قطاع السهم")
        st.caption("💡 توقعات بارتفاع العائد على السهم")
        st.caption("📂 إعلان نتائج مالية إيجابية")

    # --- العمود الأوسط: الرسم البياني والأهداف (نفس تصميم الصورة) ---
    with col_mid:
        # الرسم البياني بشكل مصغر وأنيق
        fig = go.Figure(data=[go.Candlestick(x=pd.date_range(start='2026-01-01', periods=20),
                open=[70,71,72,71,73,74,75,74,76,77,78,77,79,80,81,80,82,83,84,85],
                high=[72,73,73,72,75,76,77,75,78,79,80,78,81,82,83,82,84,85,86,87],
                low=[69,70,71,70,72,73,74,73,75,76,77,76,78,79,80,79,81,82,83,84],
                close=[71,72,71,73,74,75,74,76,77,78,77,79,80,81,80,82,83,84,85,86])])
        fig.update_layout(height=350, template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض الأهداف بشكل فاخر (مربعات تحت الرسم)
        t1, t2, t3 = st.columns(3)
        t1.markdown("<div class='target-box'><b>الهدف 1</b><br><h2>80.00</h2></div>", unsafe_allow_html=True)
        t2.markdown("<div class='target-box'><b>الهدف 2</b><br><h2>85.00</h2></div>", unsafe_allow_html=True)
        t3.markdown("<div class='target-box'><b>الهدف 3</b><br><h2>90.00</h2></div>", unsafe_allow_html=True)

    # --- العمود الأيسر: بيانات الإغلاق والوقف ---
    with col_left:
        st.markdown("### 📊 بيانات حيوية")
        st.metric("السعر الحالي", "75.30", "1.50 (2.05%)")
        st.metric("سعر الافتتاح", "76.00")
        st.metric("الإغلاق السابق", "73.20")
        st.error("وقف الخسارة: 68.50")
        
        # تنبيهات صوتية (محاكاة)
        st.markdown("---")
        if st.button("🔊 تفعيل تنبيهات الأهداف"):
            st.toast("تم تفعيل التنبيهات الصوتية لجوالك ولابتوبك")

else:
    # الصفحة الترحيبية في حال عدم البحث
    st.info("يرجى كتابة اسم الشركة في خانة البحث أعلاه لبدء التحليل الفني واستخراج الأهداف.")
    st.image("https://images.unsplash.com/photo-1611974717482-58fce0001565?auto=format&fit=crop&w=1350&q=80", caption="بانتظار اختيار سهمك المفضل")

# شريط الأخبار السفلي
st.markdown("<br><marquee style='color: #00ffcc; font-size: 20px;'>نظام يلا سكالب: جاري مراقبة السيولة اللحظية لجميع أسهم السوق السعودي والأسواق العالمية.. استعد للدخول</marquee>", unsafe_allow_html=True)
