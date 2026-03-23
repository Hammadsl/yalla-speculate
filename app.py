import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# إعدادات المنصة
st.set_page_config(page_title="Yalla Scalp Pro", layout="wide")

# تصميم الواجهة (CSS) - مظهر احترافي داكن
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: center; background-color: #0b0e11; color: white; }
    .stApp { background-color: #0b0e11; }
    .main-box { background: #1c2128; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 10px; }
    .metric-value { font-size: 26px; font-weight: bold; color: #0ecb81; }
    input { background-color: #1c2128 !important; color: white !important; border: 1px solid #0ecb81 !important; border-radius: 10px !important; text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي وبحث السهم
st.markdown("<h1 style='color:#0ecb81;'>YALLA SCALP PRO 💎</h1>", unsafe_allow_html=True)
symbol = st.text_input("", placeholder="🔍 ابحث عن رمز السهم (مثال: NVDA, LCID, AAPL)").upper()

if symbol:
    try:
        ticker = yf.Ticker(symbol)
        # جلب بيانات 6 أشهر بفاصل يومي
        data = ticker.history(period="6mo", interval="1d")
        
        if not data.empty:
            # حساب المؤشرات الفنية
            data['SMA20'] = ta.sma(data['Close'], length=20)
            data['RSI'] = ta.rsi(data['Close'], length=14)
            curr_p = data['Close'].iloc[-1]
            rsi_val = data['RSI'].iloc[-1]

            # عرض البيانات العلوية
            st.markdown(f"## {symbol} - {ticker.info.get('longName', '')}")
            
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.markdown(f"<div class='main-box'>السعر<br><span class='metric-value'>${curr_p:.2f}</span></div>", unsafe_allow_html=True)
            with c2: st.markdown(f"<div class='main-box'>RSI<br><span class='metric-value' style='color:#fbc02d;'>{rsi_val:.1f}</span></div>", unsafe_allow_html=True)
            with c3: st.markdown(f"<div class='main-box'>التغير اليومي<br><span class='metric-value' style='color:white;'>{ticker.info.get('regularMarketChangePercent', 0):.2f}%</span></div>", unsafe_allow_html=True)
            with c4: st.markdown(f"<div class='main-box'>حجم التداول<br><span class='metric-value' style='color:white;'>{ticker.info.get('volume', 0):,}</span></div>", unsafe_allow_html=True)

            # الرسم البياني الاحترافي
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name="Price"))
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'], line=dict(color='#0ecb81', width=1.5), name="SMA 20"))
            fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
            # أهداف Predator
            st.markdown("### 🎯 أهداف Predator المقترحة")
            t1, t2, t3 = st.columns(3)
            t1.success(f"الهدف 1 (5%): ${curr_p*1.05:.2f}")
            t2.warning(f"الهدف 2 (10%): ${curr_p*1.10:.2f}")
            t3.error(f"وقف الخسارة: ${curr_p*0.95:.2f}")
            
        else:
            st.warning("لم يتم العثور على بيانات. يرجى التأكد من الرمز.")
    except Exception as e:
        st.error("خطأ في جلب البيانات. يرجى المحاولة لاحقاً.")

st.markdown("<br><hr><small>Yalla Scalp Pro v5.2 | 2026</small>", unsafe_allow_html=True)
