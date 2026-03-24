import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. إعدادات الصفحة الفاخرة
st.set_page_config(page_title="YALLA SCALP PRO", layout="wide", initial_sidebar_state="collapsed")

# تصميم CSS مخصص لجعل الواجهة فاخرة والعناوين واضحة فوق المربعات
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ffcc; }
    div[data-testid="stMetricLabel"] { font-size: 18px; font-weight: bold; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; text-align: center; }
    h1, h2, h3 { text-align: center; color: #ffffff; font-family: 'Cairo', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("<h1>💎 YALLA SCALP PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>الإصدار 7.0 المستقر - تحليل السيولة اليومي</p>", unsafe_allow_html=True)

# 2. تقسيم الشاشة (يمين للتحكم - منتصف للبيانات)
col_main, col_right = st.columns([3, 1])

# --- القسم الأيمن: المراقبة والحاسبة ---
with col_right:
    st.markdown("### 🔍 البحث والمراقبة")
    search_query = st.text_input("ادخل اسم الشركة بالعربي:", "الراجحي")
    
    st.markdown("---")
    st.markdown("### 🧮 حاسبة الأرباح")
    capital = st.number_input("رأس المال ($)", value=1000, step=100)
    shares = st.number_input("عدد الأسهم", value=100)
    
    st.info(f"الربح المتوقع T1: {round((shares * 0.5), 2)}$")
    st.info(f"الربح المتوقع T2: {round((shares * 1.2), 2)}$")
    
    st.markdown("---")
    st.markdown("### 🔔 حالة التنبيهات")
    st.success("الجوال: متصل ✅")
    st.success("اللابتوب: متصل ✅")
    # محاكاة التنبيه الصوتي (سيظهر كإشعار برمجياً)
    if st.button("اختبار صوت التنبيه"):
        st.write('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>', unsafe_allow_html=True)

# --- القسم الأوسط: الأهداف والرسم البياني ---
with col_main:
    # أ. المربعات الثلاثة للأهداف (في المنتصف وبشكل أنيق)
    st.markdown("### أهداف العمليات اللحظية")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.metric(label="الهدف الاول", value="10.50")
    with t2:
        st.metric(label="الهدف الثاني", value="10.85")
    with t3:
        st.metric(label="الهدف الثالث", value="11.20")

    # ب. الرسم البياني (حجم متوسط وأنيق)
    st.markdown("#### حركة السعر والسيولة")
    # بيانات وهمية للرسم البياني
    df = pd.DataFrame({
        'time': pd.date_range(start='2026-03-24', periods=20, freq='H'),
        'price': [10.1, 10.15, 10.12, 10.2, 10.25, 10.31, 10.28, 10.35, 10.4, 10.45, 10.5, 10.48, 10.55, 10.6, 10.58, 10.65, 10.7, 10.75, 10.8, 10.85]
    })
    fig = go.Figure(data=[go.Scatter(x=df['time'], y=df['price'], line=dict(color='#00ffcc', width=3))])
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    # ج. مربعات البيانات الأساسية (تحت الرسم البياني)
    st.markdown("---")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric(label="سعر الافتتاح", value="10.25")
    with d2:
        st.metric(label="الإغلاق السابق", value="10.10")
    with d3:
        st.metric(label="تاريخ اليوم", value=datetime.now().strftime("%Y-%m-%d"))

# 3. شريط الأخبار السفلي
st.markdown("---")
st.markdown("<marquee style='color: #00ffcc; font-size: 18px;'>خبر عاجل: سيولة ضخمة تدخل قطاع التكنولوجيا الآن - نظام يلا سكالب يرصد إشارة دخول قوية - راقب الهدف الثالث لشركة سابك</marquee>", unsafe_allow_html=True)
