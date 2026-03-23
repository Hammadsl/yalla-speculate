import streamlit as st
import yfinance as yf

# إعدادات بسيطة جداً لضمان التشغيل
st.set_page_config(page_title="Yalla Scalp")

st.write("# 💎 YALLA SCALP PRO")
st.write("ناصر، إذا رأيت هذه الرسالة فالموقع يعمل!")

# خانة البحث
symbol = st.text_input("اكتب رمز السهم هنا (مثلاً NVDA):", value="AAPL")

if symbol:
    try:
        # جلب البيانات
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        
        if not data.empty:
            price = data['Close'].iloc[-1]
            st.success(f"سعر {symbol} الآن هو: ${price:.2f}")
            st.balloons() # احتفال بالتشغيل!
        else:
            st.error("لم نجد بيانات لهذا السهم، تأكد من الرمز.")
    except Exception as e:
        st.error("انتظر ثواني حتى يتم تحميل المحرك...")
