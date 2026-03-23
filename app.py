import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# 1. إعدادات الصفحة
st.set_page_config(page_title="Yalla Scalp Pro", layout="wide")

# 2. تصميم الواجهة (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: center; background-color: #0b0e11; color: white; }
    .stMetric { background-color: #1c2128; padding: 15px; border-radius: 10px; border: 1px solid #0ecb81; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 YALLA SCALP PRO")
st.write("---")

# 3. خانة البحث عن السهم
symbol = st.text_input("🔍 ادخل رمز السهم (مثال: NVDA أو TSLA):", value="NVDA").upper()

if symbol:
    try:
        # جلب البيانات من ياهو فاينانس
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1mo", interval="1d")
        
        if not data.empty:
            curr_p = data['Close'].iloc[-1]
            change = ((curr_p - data['Open'].iloc[-1]) / data['Open'].iloc[-1]) * 100
            
            # 4. عرض مؤشرات سريعة
            col1, col2, col3 = st.columns(3)
            col1.metric("السعر الحالي", f"${curr_p:.2f}")
            col2.metric("التغير اليومي", f"{change:.2f}%")
            col3.metric("حجم التداول", f"{data['Volume'].iloc[-1]:,}")

            # 5. رسم الشموع اليابانية
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
            
            # 6. أهداف ناصر المقترحة
            st.markdown("### 🎯 أهداف Predator")
            t1, t2, t3 = st.columns(3)
            t1.success(f"الهدف 1 (+5%): ${curr_p*1.05:.2f}")
            t2.warning(f"الهدف 2 (+10%): ${curr_p*1.10:.2f}")
            t3.error(f"وقف الخسارة (-5%): ${curr_p*0.95:.2f}")
            
        else:
            st.error("لم نجد بيانات لهذا الرمز.")
    except Exception as e:
        st.info("جاري تحميل البيانات.. يرجى الانتظار")

st.sidebar.info("الإصدار 1.0 - جاهز للاستخدام")
