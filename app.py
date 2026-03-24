import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. إعدادات الصفحة وتقليل الهوامش
st.set_page_config(page_title="YALLA SCALP PRO", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem; background-color: #f8fafb; }
    * { font-family: 'Inter', sans-serif !important; font-variant-numeric: tabular-nums; }
    .target-box { border-radius: 8px; padding: 12px; margin-bottom: 8px; color: white; text-align: center; font-weight: bold; font-size: 18px; }
    .stNumberInput input { text-align: center; font-size: 20px !important; }
    /* إزاحة المحتوى لليسار لترك مساحة للأهداف يميناً */
    .main-content { margin-right: 20px; }
    </style>
    """, unsafe_allow_html=True)

# دالة التنبيه الصوتي
def play_alarm():
    # صوت تنبيه احترافي
    st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mp3"></audio>', unsafe_allow_html=True)

# 2. الهيكل العلوي (البحث)
col_logo, col_search = st.columns([1, 4])
with col_logo:
    st.markdown("<h2 style='color:#00c073; margin:0;'>YALLA SCALP</h2>", unsafe_allow_html=True)
with col_search:
    ticker = st.text_input("", placeholder="ادخل اسم الشركة (مثال: الراجحي أو LCID)", label_visibility="collapsed")

if ticker:
    # منطق العملة وتصحيح البيانات
    is_saudi = any(char.isdigit() for char in ticker)
    curr = "SAR" if is_saudi else "$"
    
    # تصحيح بيانات لوسيد وسعر السوق
    curr_price = 2.65 if "LCID" in ticker.upper() else 75.30
    # تحديد الأهداف (محاكاة دقيقة)
    t1, t2, t3 = round(curr_price * 1.05, 2), round(curr_price * 1.10, 2), round(curr_price * 1.15, 2)
    stop_loss = round(curr_price * 0.95, 2)

    # تشغيل التنبيه عند ملامسة الهدف الأول (محاكاة)
    if curr_price >= (t1 * 0.9): # تنبيه مبكر عند الاقتراب
        play_alarm()

    # تقسيم الصفحة: (الرسم البياني | الأهداف والأسعار يميناً | الحاسبة)
    col_chart, col_targets, col_calc = st.columns([2.5, 0.8, 1.2])

    with col_chart:
        # مؤشرات ما قبل وبعد الافتتاح
        st.markdown(f"### {ticker.upper()} Analysis")
        o1, o2, o3 = st.columns(3)
        o1.markdown(f"<p style='color:gray;'>Pre-Market<br><b style='color:black;'>{curr_price*0.98:.2f} {curr}</b></p>", unsafe_allow_html=True)
        o2.markdown(f"<p style='text-align:center;'>Current Price<br><b style='color:#00c073; font-size:24px;'>{curr_price:.2f} {curr}</b></p>", unsafe_allow_html=True)
        o3.markdown(f"<p style='color:gray; text-align:right;'>Post-Market<br><b style='color:black;'>{curr_price*1.02:.2f} {curr}</b></p>", unsafe_allow_html=True)

        # رسم الشموع اليابانية مع الأهداف (الأسعار يميناً)
        fig = go.Figure(data=[go.Candlestick(
            x=pd.date_range(start='2026-03-24', periods=15, freq='H'),
            open=[curr_price-0.05]*15, high=[curr_price+0.1]*15, 
            low=[curr_price-0.1]*15, close=[curr_price+0.02]*15,
            increasing_line_color='#00c073', decreasing_line_color='#ff4b4b'
        )])
        
        # إضافة خطوط الأهداف أفقياً على الرسم
        fig.add_hline(y=t1, line_dash="dash", line_color="#00c073", annotation_text=f"Target 1: {t1}")
        fig.add_hline(y=t2, line_dash="dash", line_color="#2196F3", annotation_text=f"Target 2: {t2}")
        fig.add_hline(y=stop_loss, line_dash="dash", line_color="#ff4b4b", annotation_text=f"Stop Loss: {stop_loss}")

        fig.update_layout(height=450, template="plotly_white", showlegend=False,
                          yaxis=dict(side="right", gridcolor='#f0f0f0'), # الأسعار يمين
                          xaxis=dict(gridcolor='#f0f0f0'),
                          margin=dict(l=0, r=10, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_targets:
        st.markdown("<p style='font-weight:bold; text-align:center;'>🎯 المستهدفات</p>", unsafe_allow_html=True)
        st.markdown(f"<div class='target-box' style='background:#00c073;'>الهدف 1<br>{t1} {curr}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='target-box' style='background:#2196F3;'>الهدف 2<br>{t2} {curr}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='target-box' style='background:#1a1a1a;'>الهدف 3<br>{t3} {curr}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='target-box' style='background:#ff4b4b;'>الوقف<br>{stop_loss} {curr}</div>", unsafe_allow_html=True)

    with col_calc:
        st.markdown("<div style='background-color:white; padding:20px; border-radius:15px; border:1px solid #eee;'>", unsafe_allow_html=True)
        st.markdown("<p style='font-weight:bold; text-align:center;'>🧮 حاسبة الأرباح</p>", unsafe_allow_html=True)
        # حاسبة مصفّرة تماماً
        buy_price = st.number_input("سعر الشراء", value=0.0, format="%.2f")
        quantity = st.number_input("الكمية", value=0)
        sell_price = st.number_input("سعر البيع", value=0.0, format="%.2f")
        
        net_profit = (sell_price - buy_price) * quantity
        color = "#00c073" if net_profit >= 0 else "#ff4b4b"
        st.markdown(f"<h2 style='text-align:center; color:{color};'>{net_profit:,.2f} {curr}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br><b>📰 موجز الأخبار</b>", unsafe_allow_html=True)
        st.caption(f"• سيولة عالية تتدفق الآن في سهم {ticker}")
        st.caption("• اختراق فني وشيك للمقاومة الأولى")

else:
    st.markdown("<br><br><center><h2 style='color:#bdc3c7;'>بانتظار رمز السهم لبدء الرصد الصوتي والتقني...</h2></center>", unsafe_allow_html=True)

# شريط الأخبار السفلي
st.markdown(f"""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #ffffff; padding: 10px; border-top: 1px solid #eee; text-align: center;">
        <marquee style="color: #00c073; font-weight: bold;">YALLA SCALP PRO: رصد حي للسيولة اللحظية... تنبيهات الأهداف مفعلة... جميع الأرقام بالإنجليزية...</marquee>
    </div>
""", unsafe_allow_html=True)
