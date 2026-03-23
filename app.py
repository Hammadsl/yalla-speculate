import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- إعدادات المنصة ---
st.set_page_config(page_title="Sahm Copy - Yalla Scalp", layout="wide")

# --- تنسيق CSS لمحاكاة "سهم" بدقة ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Noto+Sans+Arabic:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', 'Noto Sans Arabic', sans-serif;
        direction: rtl;
        background-color: #F8F9FB;
    }

    /* شريط المؤشرات العلوي */
    .market-header {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 0 0 15px 15px;
        border-bottom: 1px solid #E0E4E9;
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    .market-box { text-align: center; min-width: 150px; }
    .m-title { font-size: 12px; color: #848E9C; margin-bottom: 5px; }
    .m-price { font-size: 14px; font-weight: bold; color: #1E2329; }
    .m-change { font-size: 12px; }
    .up { color: #0ECB81; } .down { color: #F6465D; }

    /* الحاويات الجانبية */
    .side-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E0E4E9;
        margin-bottom: 15px;
    }
    .card-title { font-size: 16px; font-weight: bold; color: #1E2329; border-bottom: 2px solid #0ECB81; display: inline-block; margin-bottom: 15px; }

    /* البحث */
    .stTextInput input {
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        text-align: left !important; /* الأرقام والرموز يسار */
    }

    /* كروت الأهداف */
    .target-grid { display: flex; gap: 10px; margin-top: 15px; }
    .target-item { flex: 1; padding: 15px; border-radius: 10px; text-align: center; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. شريط المؤشرات العلوي (واضح ومنظم) ---
st.markdown("""
    <div class="market-header">
        <div class="market-box">
            <div class="m-title">S&P 500</div>
            <div class="m-price">5,241.53</div>
            <div class="m-change down">▼ -1.51%</div>
        </div>
        <div class="market-box">
            <div class="m-title">NASDAQ</div>
            <div class="m-price">16,384.47</div>
            <div class="m-change down">▼ -2.01%</div>
        </div>
        <div class="market-box">
            <div class="m-title">Dow Jones</div>
            <div class="m-price">39,475.90</div>
            <div class="m-change down">▼ -0.96%</div>
        </div>
        <div class="market-box">
            <div class="m-title">TASI</div>
            <div class="m-price">12,634.20</div>
            <div class="m-change up">▲ +0.40%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. توزيع المحتوى (جانبي ويمين) ---
col_main, col_side = st.columns([3, 1])

with col_side:
    # قائمة المتابعة
    st.markdown('<div class="side-card"><div class="card-title">قائمة المتابعة</div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="display:flex; justify-content:space-between; padding:10px 0;">
            <span style="font-weight:bold;">LCID</span>
            <span class="down">10.06 $</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # حاسبة الأرباح
    st.markdown('<div class="side-card"><div class="card-title">حاسبة الأرباح</div>', unsafe_allow_html=True)
    buy_price = st.number_input("سعر الشراء", value=10.0, step=0.01)
    target_price = st.number_input("السعر المستهدف", value=11.5, step=0.01)
    shares = st.number_input("الكمية", value=100)
    total_profit = (target_price - buy_price) * shares
    st.markdown(f"<div style='background:#E8F9F3; padding:10px; border-radius:5px; color:#0ECB81; text-align:center;'>الربح المتوقع: {total_profit:,.2f} $</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    # محرك البحث
    symbol = st.text_input("", placeholder="Search Ticker (e.g. NVDA, AAPL, LCID)...").upper()
    
    if symbol:
        try:
            ticker_data = yf.Ticker(symbol)
            df = ticker_data.history(period="1d", interval="1m")
            
            if not df.empty:
                current_p = df['Close'].iloc[-1]
                
                # عرض السعر
                st.markdown(f"<h2>{symbol} <span style='color:#848E9C; font-size:16px;'>Global Market</span></h2>", unsafe_allow_html=True)
                st.markdown(f"<h1 style='color:#1E2329;'>{current_p:,.2f} <span style='font-size:18px; color:#F6465D;'>-2.33%</span></h1>", unsafe_allow_html=True)

                # الرسم البياني (خطوط ناعمة مثل سهم)
                fig = go.Figure(data=[go.Scatter(x=df.index, y=df['Close'], line=dict(color='#0ECB81', width=2), fill='tozeroy', fillcolor='rgba(14, 203, 129, 0.1)')])
                fig.update_layout(template="plotly_white", height=400, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)
                
                # الأهداف (تحت الرسم البياني)
                st.markdown("### مستويات الأهداف (Predator Targets)")
                st.markdown(f"""
                <div class="target-grid">
                    <div class="target-item" style="background-color: #007BFF;">هدف أول <br> {current_p*1.05:,.2f}</div>
                    <div class="target-item" style="background-color: #F1B100;">هدف ثاني <br> {current_p*1.10:,.2f}</div>
                    <div class="target-item" style="background-color: #6F42C1;">هدف ثالث <br> {current_p*1.15:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
        except:
            st.error("Please enter a valid symbol")

# تذييل
st.markdown("<center style='color:#848E9C; padding:20px;'>Yalla Scalp Pro | Powered by Global Data Feed</center>", unsafe_allow_html=True)
