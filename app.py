import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. إعدادات الصفحة والستايل العام (ألوان منصة سهم - أخضر فاتح وأبيض)
st.set_page_config(page_title="YALLA SCALP PRO", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafb; }
    * { font-variant-numeric: tabular-nums; font-family: 'Inter', sans-serif !important; }
    
    /* تنسيق كروت الأهداف الجانبية (يمين) */
    .target-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        border-right: 4px solid #00c073;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .target-label { color: #666; font-size: 14px; }
    .target-price { color: #111; font-size: 20px; font-weight: bold; }

    /* تنسيق الحاسبة والقوائم الجانبية */
    .sidebar-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #eef0f2;
    }
    .block-container { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# دالة التنبيه الصوتي
def play_sound(url):
    st.markdown(f'<audio autoplay><source src="{url}" type="audio/mp3"></audio>', unsafe_allow_html=True)

# 2. منطق تحديد العملة
def get_currency(ticker):
    if any(char.isdigit() for char in ticker): return "SAR"
    return "$"

# 3. الهيكل الرأسي
col_logo, col_search = st.columns([1, 4])
with col_logo:
    st.markdown("<h3 style='color:#00c073;'>YALLA SCALP</h3>", unsafe_allow_html=True)
with col_search:
    ticker = st.text_input("", placeholder="ادخل اسم الشركة او الرمز...", label_visibility="collapsed")

if ticker:
    curr = get_currency(ticker)
    current_price = 75.30 # سعر افتراضي للمحاكاة
    target_1, target_2, target_3 = 80.00, 85.50, 90.15
    stop_loss = 68.00

    # تفعيل التنبيهات الصوتية تلقائياً عند الوصول للأهداف
    if current_price >= target_1:
        play_sound("https://www.soundjay.com/buttons/beep-01a.mp3")

    # تقسيم الصفحة (توزيع سهم الاحترافي)
    col_chart, col_targets, col_calc = st.columns([2.5, 0.8, 1])

    with col_chart:
        st.markdown(f"## {ticker.upper()} <span style='font-size:18px; color:gray;'>{curr}</span>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Price", f"{current_price} {curr}", "1.45%")
        m2.metric("Open", f"{76.10} {curr}")
        m3.metric("Volume", "5.2M")

        fig = go.Figure(data=[go.Scatter(x=list(range(20)), y=[70,71,72,75,74,76,78,77,79,81,80,82,83,85,84,86,88,87,89,90], 
                         fill='tozeroy', line=dict(color='#00c073', width=2))])
        fig.update_layout(height=400, template="plotly_white", margin=dict(l=0,r=0,t=20,b=0),
                          xaxis_visible=False, yaxis_gridcolor='#f0f0f0')
        st.plotly_chart(fig, use_container_width=True)

    with col_targets:
        st.markdown("<p style='font-weight:bold; color:#333;'>الأهداف اللحظية</p>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="target-card"><div class="target-label">الهدف الاول</div><div class="target-price">{target_1} {curr}</div></div>
            <div class="target-card"><div class="target-label">الهدف الثاني</div><div class="target-price">{target_2} {curr}</div></div>
            <div class="target-card"><div class="target-label">الهدف الثالث</div><div class="target-price">{target_3} {curr}</div></div>
            <div class="target-card" style="border-right-color:#ff4b4b;"><div class="target-label">وقف الخسارة</div><div class="target-price">{stop_loss} {curr}</div></div>
        """, unsafe_allow_html=True)

    with col_calc:
        st.markdown("<div class='sidebar-box'>", unsafe_allow_html=True)
        st.markdown("<p style='font-weight:bold;'>🧮 حاسبة الأرباح</p>", unsafe_allow_html=True)
        buy_p = st.number_input("Entry Price", value=70.0)
        qty = st.number_input("Qty", value=100)
        sell_p = st.number_input("Exit Price", value=85.0)
        total_profit = (sell_p - buy_p) * qty
        st.markdown(f"<h3 style='color:#00c073;'>+{total_profit:,.2f} {curr}</h3>", unsafe_allow_html=True)
        st.button("احسب الآن", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>### 📰 أخبار")
        st.caption("• تحسن ملحوظ في سيولة السهم اليوم")
        st.caption("• السهم يقترب من منطقة عرض قوية")

else:
    st.markdown("<br><br><center><h3>بانتظار إدخال رمز السهم لبدء المراقبة...</h3></center>", unsafe_allow_html=True)

# شريط الأخبار السفلي
st.markdown(f"""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #ffffff; padding: 10px; border-top: 1px solid #eee; text-align: center;">
        <marquee style="color: #00c073; font-weight: bold;">YALLA SCALP PRO: Monitoring Market Liquidity... All Targets calculated by Daily Volume...</marquee>
    </div>
""", unsafe_allow_html=True)
