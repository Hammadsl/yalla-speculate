import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# إعدادات الصفحة
st.set_page_config(page_title="Yalla Scalp Pro", layout="wide")

# تصميم CSS احترافي وهادئ
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; background-color: #0b0e11; color: white; }
    .stApp { background-color: #0b0e11; }
    .metric-card { background: #1c2128; padding: 15px; border-radius: 10px; border: 1px solid #30363d; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# شريط جانبي للبحث
st.sidebar.header("📊 رادار يلا سكالب")
symbol = st.sidebar.text_input("اكتب رمز السهم (مثل NVDA أو LCID):", value="NVDA").upper()

if symbol:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1y", interval="1d")
        info = ticker.info
        
        if not data.empty:
            # حساب المؤشرات
            data['SMA20'] = ta.sma(data['Close'], length=20)
            data['RSI'] = ta.rsi(data['Close'], length=14)
            
            # العناوين والسعر
            st.title(f"{symbol} - {info.get('longName', 'Market')}")
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"<div class='metric-card'>السعر الحالي<br><h2>${data['Close'].iloc[-1]:.2f}</h2></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'>RSI (14)<br><h2>{data['RSI'].iloc[-1]:.1f}</h2></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='metric-card'>الحجم اليومي<br><h2>{info.get('volume', 0):,}</h2></div>", unsafe_allow_html=True)
            c4.markdown(f"<div class='metric-card'>مكرر الأرباح P/E<br><h2>{info.get('trailingPE', 'N/A')}</h2></div>", unsafe_allow_html=True)

            # الرسم البياني
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name="السعر"))
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'], line=dict(color='yellow', width=1.5), name="متوسط 20"))
            fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # قسم الأهداف الذكية
            st.markdown("### 🎯 أهداف Predator المقترحة")
            curr_p = data['Close'].iloc[-1]
            t1, t2, t3 = st.columns(3)
            t1.success(f"الهدف 1: ${curr_p*1.05:.2f}")
            t2.warning(f"الهدف 2: ${curr_p*1.10:.2f}")
            t3.error(f"وقف الخسارة: ${curr_p*0.95:.2f}")
            
    except Exception as e:
        st.error(f"تأكد من رمز السهم أو جودة الاتصال")

st.sidebar.markdown("---")
st.sidebar.info("تم تحديث النظام للنسخة v5.1 المستقرة")
