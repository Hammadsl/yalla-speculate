import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. إعدادات الصفحة الفاخرة
st.set_page_config(page_title="YALLA SCALP PRO", layout="wide")

# تصميم CSS لضبط الألوان والتنسيق (أبيض ورمادي فاتح مع أخضر سهم)
st.markdown("""
    <style>
    .main { background-color: #f8fafb; }
    * { font-family: 'Inter', sans-serif !important; font-variant-numeric: tabular-nums; }
    .stMetric { background-color: #ffffff; border-radius: 10px; padding: 10px; border: 1px solid #eee; }
    .target-card { background-color: #ffffff; border-radius: 8px; padding: 15px; margin-bottom: 10px; border-right: 4px solid #00c073; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .calc-sidebar { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #eef0f2; height: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. الهيكل العلوي الثابت (Header)
col_head1, col_head2 = st.columns([1, 4])
with col_head1:
    st.markdown("<h2 style='color:#00c073; margin:0;'>YALLA SCALP</h2>", unsafe_allow_html=True)
with col_head2:
    ticker = st.text_input("", placeholder="ادخل اسم الشركة أو الرمز (مثال: الراجحي أو AAPL)...", label_visibility="collapsed")

st.markdown("---")

# 3. المنطق التفاعلي (التبديل بين العام والخاص)
if not ticker:
    # --- الحالة الأولى: التحليل العام (عند فتح الموقع) ---
    st.markdown("### 📊 نظرة عامة على السوق")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("المؤشر العام (TASI)", "12,450.20", "+0.45%")
    m2.metric("مؤشر S&P 500", "5,230.10", "+1.10%")
    m3.metric("السيولة الداخلة", "6.2B SAR", "إيجابي")
    m4.metric("الشركات الرابحة", "145", "نشط")

    # رسم بياني عام لاتجاه السوق
    fig_gen = go.Figure(data=[go.Scatter(x=list(range(10)), y=[10, 12, 11, 14, 15, 14, 16, 18, 17, 20], fill='tozeroy', line=dict(color='#00c073'))])
    fig_gen.update_layout(height=400, title="أداء المؤشرات الرئيسية (لحظي)", template="plotly_white")
    st.plotly_chart(fig_gen, use_container_width=True)

else:
    # --- الحالة الثانية: تحليل السهم المختار (عند البحث) ---
    curr = "SAR" if any(char.isdigit() for char in ticker) else "$"
    
    # تقسيم الواجهة (تصميم سهم الاحترافي)
    col_main_chart, col_side_targets, col_side_calc = st.columns([2.5, 0.8, 1])

    with col_main_chart:
        st.markdown(f"## {ticker.upper()} <span style='font-size:18px; color:gray;'>{curr}</span>", unsafe_allow_html=True)
        # بيانات السهم المختارة
        d1, d2, d3 = st.columns(3)
        d1.metric("السعر الحالي", f"75.30 {curr}", "1.50%")
        d2.metric("الافتتاح", f"76.10 {curr}")
        d3.metric("أعلى سعر اليوم", f"77.00 {curr}")

        # الرسم البياني للسهم المختار
        fig_stock = go.Figure(data=[go.Candlestick(x=pd.date_range(start='2026-03-01', periods=15),
                                open=[70,71,72,71,73,74,75,74,76,77,78,77,79,80,81],
                                high=[72,73,73,72,75,76,77,75,78,79,80,78,81,82,83],
                                low=[69,70,71,70,72,73,74,73,75,76,77,76,78,79,80],
                                close=[71,72,71,73,74,75,74,76,77,78,77,79,80,81,80])])
        fig_stock.update_layout(height=400, template="plotly_white", margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_stock, use_container_width=True)

    with col_side_targets:
        st.markdown("<p style='font-weight:bold;'>🎯 الأهداف والوقف</p>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="target-card"><div style="color:gray; font-size:12px;">الهدف الاول</div><b>80.00 {curr}</b></div>
            <div class="target-card"><div style="color:gray; font-size:12px;">الهدف الثاني</div><b>85.50 {curr}</b></div>
            <div class="target-card"><div style="color:gray; font-size:12px;">الهدف الثالث</div><b>90.15 {curr}</b></div>
            <div class="target-card" style="border-right-color:#ff4b4b;"><div style="color:gray; font-size:12px;">وقف الخسارة</div><b style="color:#ff4b4b;">68.00 {curr}</b></div>
        """, unsafe_allow_html=True)

    with col_side_calc:
        st.markdown("<div class='calc-sidebar'>", unsafe_allow_html=True)
        st.markdown("<p style='font-weight:bold; text-align:center;'>🧮 حاسبة الأرباح</p>", unsafe_allow_html=True)
        buy_p = st.number_input("سعر الشراء", value=70.0)
        qty = st.number_input("الكمية", value=100)
        sell_p = st.number_input("سعر البيع", value=85.0)
        profit = (sell_p - buy_p) * qty
        st.markdown(f"<h3 style='color:#00c073; text-align:center;'>+{profit:,.2f} {curr}</h3>", unsafe_allow_html=True)
        st.button("تحديث الحساب", use_container_width=True)
        st.markdown("---")
        st.markdown("<b>📰 أخبار السهم</b>", unsafe_allow_html=True)
        st.caption("• رصد دخول سيولة مؤسساتية")
        st.caption("• السهم يحافظ على المسار الصاعد")
        st.markdown("</div>", unsafe_allow_html=True)

# 4. شريط الأخبار السفلي (ثابت)
st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #ffffff; padding: 10px; border-top: 1px solid #eee; text-align: center; z-index: 1000;">
        <marquee style="color: #00c073; font-weight: bold; font-size: 14px;">
            YALLA SCALP PRO: رصد سيولة ذكية... يتم الآن تحليل السوق السعودي والأمريكي... جميع الأرقام باللغة الإنجليزية...
        </marquee>
    </div>
""", unsafe_allow_html=True)
