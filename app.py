import streamlit as st
import subprocess
import sys

# وظيفة لتثبيت المكتبات من داخل الكود إذا نقصت
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# محاولة تحميل المكتبات، وإذا فشلت يتم تثبيتها آلياً
try:
    import yfinance as yf
    import pandas_ta as ta
    import plotly.graph_objects as go
except ImportError:
    with st.spinner('يتم الآن تجهيز محرك "الوحش".. انتظر ثواني...'):
        install('yfinance')
        install('pandas_ta')
        install('plotly')
        st.rerun()

# --- واجهة المنصة ---
st.set_page_config(page_title="Yalla Scalp Pro", layout="wide")
st.markdown("<h1 style='text-align:center; color:#0ecb81;'>YALLA SCALP PRO 💎</h1>", unsafe_allow_html=True)

symbol = st.text_input("🔍 ابحث عن رمز السهم:", value="NVDA").upper()

if symbol:
    try:
        data = yf.Ticker(symbol).history(period="6mo")
        if not data.empty:
            curr_p = data['Close'].iloc[-1]
            st.metric(f"سعر {symbol} الحالي", f"${curr_p:.2f}")
            
            fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
            
            st.success(f"الهدف القادم: ${curr_p*1.05:.2f}")
        else:
            st.error("لم يتم العثور على بيانات.")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
