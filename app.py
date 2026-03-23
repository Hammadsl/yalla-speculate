import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# --- إعدادات المنصة الاحترافية القصوى ---
st.set_page_config(page_title="Yalla Scalp - Ultra Terminal", layout="wide", initial_sidebar_state="expanded")

# --- تنسيق CSS فاخر (Dark Blue Terminal) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .metric-card { background: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; text-align: center; }
    .buy-signal { color: #39d353; font-weight: bold; border: 1px solid #39d353; padding: 10px; border-radius: 5px; }
    .sell-signal { color: #f85149; font-weight: bold; border: 1px solid #f85149; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك البحث الذكي في الأعلى ---
popular_stocks = ["NVDA", "AAPL", "TSLA", "LCID", "MSFT", "AMD", "PLTR", "TASI", "BTC-USD"]
symbol = st.sidebar.selectbox("🔍 اختر سهم أو ابحث عن رمز:", popular_stocks)

# --- جلب البيانات ---
ticker = yf.Ticker(symbol)
data = ticker.history(period="1y", interval="1d")
info = ticker.info

# --- حساب المؤشرات الفنية (Technical Engine) ---
data['SMA20'] = ta.sma(data['Close'], length=20)
data['SMA50'] = ta.sma(data['Close'], length=50)
data['EMA9'] = ta.ema(data['Close'], length=9)
data['RSI'] = ta.rsi(data['Close'], length=14)
bbands = ta.bbands(data['Close'], length=20, std=2)
data = pd.concat([data, bbands], axis=1)
macd = ta.macd(data['Close'])
data = pd.concat([data, macd], axis=1)

# --- توزيع التبويبات (Tabs) ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 التحليل الفني", "📑 البيانات المالية", "🔍 الماسح الذكي", "🤖 إشارات AI", "🛡️ إدارة المخاطر"])

with tab1: # صفحة الشارت والمؤشرات
    st.markdown(f"### {info.get('longName', symbol)} | {symbol}")
    
    # بطاقات سريعة
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("السعر الحالي", f"${data['Close'].iloc[-1]:.2f}")
    c2.metric("التغير", f"{info.get('regularMarketChangePercent', 0):.2f}%")
    c3.metric("RSI (14)", f"{data['RSI'].iloc[-1]:.1f}")
    c4.metric("حجم التداول", f"{info.get('volume', 0):,}")
    c5.metric("المتوسط (10d)", f"{info.get('averageVolume', 0):,}")

    # الرسم البياني المركب
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.6, 0.2, 0.2])
    
    # 1. الشموع والبولينجر
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name="Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['BBU_20_2.0'], line=dict(color='gray', width=1, dash='dot'), name="Upper BB"), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['BBL_20_2.0'], line=dict(color='gray', width=1, dash='dot'), name="Lower BB"), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA50'], line=dict(color='orange'), name="SMA 50"), row=1, col=1)
    
    # 2. RSI
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], line=dict(color='purple'), name="RSI"), row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    # 3. MACD
    fig.add_trace(go.Bar(x=data.index, y=data['MACDh_12_26_9'], name="MACD Hist"), row=3, col=1)

    fig.update_layout(template="plotly_dark", height=800, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with tab2: # البيانات المالية العميقة
    st.header("📊 ميزانية الشركة وبياناتها")
    f1, f2 = st.columns(2)
    with f1:
        st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
        st.write(f"**EPS:** {info.get('trailingEps', 'N/A')}")
        st.write(f"**Market Cap:** {info.get('marketCap', 'N/A'):,}")
        st.write(f"**Dividend Yield:** {info.get('dividendYield', 0)*100:.2f}%")
    with f2:
        st.write(f"**52 Week High:** ${info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.write(f"**52 Week Low:** ${info.get('fiftyTwoWeekLow', 'N/A')}")
        st.write(f"**Short Ratio:** {info.get('shortRatio', 'N/A')}")
        st.write(f"**Shares Outstanding:** {info.get('sharesOutstanding', 'N/A'):,}")

with tab4: # إشارات الذكاء الاصطناعي (Logic Based)
    st.header("🤖 تحليل Predator الذكي")
    last_price = data['Close'].iloc[-1]
    rsi_val = data['RSI'].iloc[-1]
    sma50_val = data['SMA50'].iloc[-1]
    
    if last_price > sma50_val and rsi_val < 70:
        st.markdown('<div class="buy-signal">✅ إشارة شراء: السهم فوق المتوسط RSI في منطقة آمنة</div>', unsafe_allow_html=True)
    elif rsi_val > 70:
        st.markdown('<div class="sell-signal">⚠️ إشارة بيع: تشبع شرائي عالٍ (RSI > 70)</div>', unsafe_allow_html=True)
    else:
        st.info("حالة الانتظار: لا توجد إشارة قوية حالياً.")

with tab5: # حاسبة المخاطر
    st.header("🛡️ إدارة المخاطر")
    balance = st.number_input("رأس مال المحفظة ($)", value=10000)
    risk_pct = st.slider("نسبة المخاطرة لكل صفقة (%)", 1, 5, 2)
    stop_loss = st.number_input("سعر وقف الخسارة ($)", value=last_price*0.95)
    
    risk_amt = balance * (risk_pct/100)
    pos_size = risk_amt / (last_price - stop_loss)
    st.write(f"**الكمية المقترحة للشراء:** {int(pos_size)} سهم")
    st.write(f"**أقصى خسارة مسموح بها:** ${risk_amt}")

st.sidebar.markdown("---")
st.sidebar.caption("Yalla Scalp Pro | النسخة الكاملة v4.0")
