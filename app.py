import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# إعدادات المنصة الاحترافية
st.set_page_config(page_title="Yalla Scalp Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: center; background-color: #0b0e11; color: white; }
    .stMetric { background-color: #1c2128; padding: 15px; border-radius: 10px; border: 1px solid #0ecb81; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 YALLA SCALP PRO")
st.write("---")

# البحث عن السهم
symbol = st.text_input("🔍 ادخل رمز السهم (مثال: NVDA أو AAPL):", value="NVDA").upper()

if symbol:
    try:
        # جلب البيانات
        with st.spinner('جاري تحليل البيانات...'):
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="6mo", interval="1d")
            
            if not data.empty:
                curr_p = data['Close'].iloc[-1]
                change = ((curr_p - data['Open'].iloc[-1]) / data['Open'].iloc[-1]) * 100
                
                # عرض السعر بشكل فخم
                col1, col2, col3 = st.columns(3)
                col1.metric("السعر الحالي", f"${curr_p:.2f}")
                col2.metric("التغير اليومي", f"{change:.2f}%")
                col3.metric("حجم التداول", f"{ticker.info.get('volume', 0):,}")

                # رسم الشموع اليابانية
                fig = go.Figure(data=[go.Candlestick(
                    x=data.index,
                    open=data['Open'], high=data['High'],
                    low=data['Low'], close=data['Close'],
                    name="السعر"
                )])
                
                fig.update_layout(
                    template="plotly_dark",
                    height=500,
                    xaxis_rangeslider_visible=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # أهداف Predator
                st.markdown("### 🎯 أهداف Predator")
                t1, t2, t3 = st.columns(3)
                t1.success(f"الهدف 1: ${curr_p*1.05:.2f}")
                t2.warning(f"الهدف 2: ${curr_p*1.10:.2f}")
                t3.error(f"وقف الخسارة: ${curr_p*0.95:.2f}")
            else:
                st.error("لم يتم العثور على بيانات. تأكد من الرمز.")
    except Exception as e:
        st.info("جاري تحديث المحرك.. انتظر لحظات")

st.sidebar.markdown("### ⚙️ إعدادات الرادار")
st.sidebar.write("الإصدار 6.0 المستقر")
