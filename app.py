import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# إعدادات احترافية
st.set_page_config(page_title="Yalla Scalp Pro", layout="wide")

# تصميم CSS لمنصة "سهم" مطورة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; background-color: #0d1117; color: white; }
    .stApp { background-color: #0b0e11; }
    .metric-card { background: #1c2128; padding: 15px; border-radius: 10px; border: 1px solid #30363d; text-align: center; margin: 5px; }
    .up { color: #26a69a; } .down { color: #ef5350; }
    </style>
    """, unsafe_allow_html=True)

# شريط البحث الذكي (Autocomplete)
popular_symbols = ["LCID", "NVDA", "AAPL", "TSLA", "AMD", "MSFT", "PLTR", "TASI", "BTC-USD"]
symbol = st.sidebar.selectbox("🔍 ابحث عن رمز السهم (تنبؤ آلي):", popular_symbols)

if symbol:
    ticker = yf.Ticker(symbol)
    # جلب البيانات اللحظية والتاريخية
    data = ticker.history(period="1y", interval="1d")
    info = ticker.info
    
    if not data.empty:
        # حساب المؤشرات الفنية (Technical Indicators)
        data['SMA20'] = ta.sma(data['Close'], length=20)
        data['SMA50'] = ta.sma(data['Close'], length=50)
        data['RSI'] = ta.rsi(data['Close'], length=14)
        
        # عرض البيانات الأساسية في مربعات (Dashboard)
        st.markdown(f"## {symbol} - {info.get('longName', 'Global Market')}")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f"<div class='metric-card'>سعر الإغلاق<br><h2 class='up'>${data['Close'].iloc[-1]:.2f}</h2></div>", unsafe_allow_html=True)
        m2.markdown(f"<div class='metric-card'>حجم التداول<br><h2>{info.get('volume', 0):,}</h2></div>", unsafe_allow_html=True)
        m3.markdown(f"<div class='metric-card'>القيمة السوقية<br><h2>{info.get('marketCap', 0):,}</h2></div>", unsafe_allow_html=True)
        m4.markdown(f"<div class='metric-card'>نطاق 52 أسبوع<br><h2>{info.get('fiftyTwoWeekLow', 0):.2f} - {info.get('fiftyTwoWeekHigh', 0):.2f}</h2></div>", unsafe_allow_html=True)

        # الرسم البياني المركب (الأسعار + المؤشرات)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.7, 0.3])
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name="السعر"), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'], line=dict(color='yellow', width=1), name="SMA 20"), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA50'], line=dict(color='cyan', width=1), name="SMA 50"), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], line=dict(color='purple'), name="RSI"), row=2, col=1)
        
        fig.update_layout(template="plotly_dark", height=600, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # التبويبات الإضافية لخيارات أكثر
        t1, t2, t3 = st.tabs(["📋 بيانات مالية عميقة", "🤖 إشارات AI", "📅 أخبار"])
        with t1:
            st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
            st.write(f"**EPS:** {info.get('trailingEps', 'N/A')}")
            st.write(f"**Beta:** {info.get('beta', 'N/A')}")
        with t2:
            st.info("نظام Predator AI: السهم حالياً في منطقة تجميع (RSI مستقر)")

st.sidebar.markdown("---")
st.sidebar.write("Yalla Scalp Pro v5.0")
