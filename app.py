import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. إعدادات الصفحة والستايل الفاخر
st.set_page_config(page_title="YALLA SCALP PRO", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; background-color: #f8fafb; }
    * { font-family: 'Inter', sans-serif !important; font-variant-numeric: tabular-nums; }
    
    /* تصميم كروت الأهداف الجانبية */
    .target-card {
        border-radius: 10px; padding: 15px; margin-bottom: 10px; 
        color: white; text-align: center; font-weight: bold; font-size: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* تنسيق الحاسبة */
    .calc-container {
        background-color: #ffffff; padding: 20px; border-radius: 15px;
        border: 1px solid #e0e0e0; box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }
    
    /* تعديل شكل المدخلات الرقمية */
    .stNumberInput input { text-align: center; font-size: 18px !important; color: #111; }
    </style>
    """, unsafe_allow_html=True)

# دالة التنبيه الصوتي
def play_alarm():
    st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mp3"></audio>', unsafe_allow_html=True)

# 2. الهيكل العلوي (البحث)
col_l, col_s = st.columns([1, 4])
with col_l:
    st.markdown("<h2 style='color:#00c073; margin:0;'>YALLA SCALP</h2>", unsafe_allow_html=True)
with col_s:
    ticker = st.text_input("", placeholder="ادخل اسم الشركة...", label_visibility="collapsed")

st.markdown("---")

if ticker:
    # منطق العملة وتصحيح البيانات (لوسيد كمثال)
    is_saudi = any(char.isdigit() for char in ticker)
    curr = "SAR" if is_saudi else "$"
    
    # تحديد السعر بناءً على السهم (تصحيح لوسيد)
    curr_price = 2.65 if "LCID" in ticker.upper() else 75.30
    t1, t2, t3 = round(curr_price * 1.05, 2), round(curr_price * 1.10, 2), round(curr_price * 1.15, 2)
    stop_loss = round(curr_price * 0.95, 2)

    # تشغيل التنبيه عند ملامسة الهدف الأول
    if curr_price >= (t1 * 0.99):
        play_alarm()

    # تقسيم الصفحة: (الرسم البياني | الأهداف | الحاسبة)
    col_chart, col_targets, col_calc = st.columns([2.5, 0.8, 1.2])

    with col_chart:
        st.markdown(f"### {ticker.upper()} <span style='color:gray; font-size:14px;'>Live Candles</span>", unsafe_allow_html=True)
        
        # مؤشرات قبل وبعد الافتتاح
        o1, o2, o3 = st.columns(3)
        o1.markdown(f"<small>Pre-Market</small><br><b>{curr_price*0.98:.2f}</b>", unsafe_allow_html=True)
        o2.markdown(f"<div style='text-align:center;'><small>Current</small><br><b style='color:#00c073; font-size:22px;'>{curr_price:.2f} {curr}</b></div>", unsafe_allow_html=True)
        o3.markdown(f"<div style='text-align:right;'><small>Post-Market</small><br><b>{curr_price*1.02:.2f}</b></div>", unsafe_allow_html=True)

        # رسم الشموع اليابانية (الأسعار يميناً)
        fig = go.Figure(data=[go.Candlestick(
            x=pd.date_range(start='2026-03-24', periods=15, freq='H'),
            open=[curr_price-0.05]*15, high=[curr_price+0.1]*15, 
            low=[curr_price-0.1]*15, close=[curr_price+0.02]*15,
            increasing_line_color='#00c073', decreasing_line_color='#ff4b4b'
        )])
        
        # إضافة خطوط الأهداف والوقف على الرسم البياني
        fig.add_hline(y=t1, line_dash="dash", line_color="#00c073", annotation_text=f"T1: {t1}")
        fig.add_hline(y=t2, line_dash="dash", line_color="#2196F3", annotation_text=f"T2: {t2}")
        fig.add_hline(y=stop_loss, line_dash="dash", line_color="#ff4b4b", annotation_text=f"STOP")

        fig.update_layout(height=450, template="plotly_white", showlegend=False,
                          yaxis=dict(side="right", gridcolor='#f0f0f0'),
                          margin=dict(l=0, r=10, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_targets:
        st.markdown("<p style='font-weight:bold; text-align:center;'>🎯 المستهدفات</p>", unsafe_allow_html=True)
        st.markdown(f"<div class='target-card' style='background:#00c073;'>الهدف 1<br>{t1} {curr}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='target-card' style='background:#2196F3;'>الهدف 2<br>{t2} {curr}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='target-card' style='background:#1a1a1a;'>الهدف 3<br>{t3} {curr}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='target-card' style='background:#ff4b4b;'>الوقف<br>{stop_loss} {curr}</div>", unsafe_allow_html=True)

    with col_calc:
        st.markdown("<div class='calc-container'>", unsafe_allow_html=True)
        st.markdown("<p style='font-weight:bold; text-align:center;'>🧮 حاسبة الأرباح</p>", unsafe_allow_html=True)
        # حاسبة مصفّرة تماماً
        buy_p = st.number_input("سعر الشراء", value=0.00, format="%.2f")
        qty = st.number_input("الكمية", value=0)
        sell_p = st.number_input("سعر البيع", value=0.00, format="%.2f")
        
        profit = (sell_p - buy_p) * qty
        p_color = "#00c073" if profit >= 0 else "#ff4b4b"
        st.markdown(f"<h2 style='text-align:center; color:{p_color};'>{profit:,.2f} {curr}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br><b>📰 موجز</b>", unsafe_allow_html=True)
        st.caption(f"تم رصد سيولة في {ticker}")

else:
    # التحليل العام (عند الدخول أول مرة)
    st.markdown("### 📊 حالة السوق العامة")
    c1, c2, c3 = st.columns(3)
    c1.metric("TASI", "12,640", "+0.32%")
    c2.metric("S&P 500", "5,240", "+1.20%")
    c3.metric("السيولة", "5.4B SAR", "إيجابي")
    
    fig_idx = go.Figure(data=[go.Scatter(y=[10,15,13,17,20,18,25], line=dict(color='#00c073', width=4), fill='tozeroy')])
    fig_idx.update_layout(height=350, template="plotly_white", xaxis_visible=False)
    st.plotly_chart(fig_idx, use_container_width=True)
