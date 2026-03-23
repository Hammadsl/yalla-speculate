import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- إعدادات الصفحة الفاخرة ---
st.set_page_config(page_title="Yalla Speculate Pro", layout="wide", initial_sidebar_state="expanded")

# --- تنسيق CSS مخصص للجمالية الفاخرة ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stSidebar { background-color: #161b22; border-right: 1px solid #30363d; }
    h1, h2, h3 { color: #e6edf3; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stMetric { background-color: #1c2128; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    .target-blue { background-color: #007bff; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin: 5px; }
    .target-yellow { background-color: #ffc107; color: black; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin: 5px; }
    .target-purple { background-color: #6f42c1; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية (اليمين) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2502/2502160.png", width=80)
    st.title("Yalla Speculate")
    
    # حسابة الأرباح
    st.subheader("💰 حسابة الأرباح")
    price_in = st.number_input("سعر الشراء", value=10.0)
    quantity = st.number_input("الكمية", value=100)
    current_price_calc = st.number_input("السعر المستهدف", value=11.0)
    profit = (current_price_calc - price_in) * quantity
    st.success(f"الربح المتوقع: ${profit:,.2f}")
    
    st.markdown("---")
    
    # الأخبار
    st.subheader("📰 آخر الأخبار")
    st.caption("• الفيدرالي يثبت أسعار الفائدة")
    st.caption("• سهم لوسيد يختبر مناطق دعم قوية")
    st.caption("• نمو متوقع في قطاع التكنولوجيا الصيني")

# --- المنطقة الوسطى (التحليل والفرص) ---
col_main = st.container()

with col_main:
    st.title("💎 رادار الفرص الذكي")
    symbol = st.text_input("🔍 ادخل رمز السهم (مثال: LCID, NVDA, AAPL)", "LCID").upper()
    
    try:
        data = yf.download(symbol, period="3mo", interval="1d")
        if not data.empty:
            curr_price = data['Close'].iloc[-1]
            
            # رسم الشموع اليابانية الفاخر
            fig = go.Figure(data=[go.Candlestick(x=data.index,
                            open=data['Open'], high=data['High'],
                            low=data['Low'], close=data['Close'],
                            increasing_line_color='#26a69a', decreasing_line_color='#ef5350')])
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # تحليل الفرص
            st.subheader("🚀 تحليل Predator للمستويات القادمة")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="target-blue">🔵 هدف أول: ${curr_price * 1.05:.2f}</div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="target-yellow">🟡 هدف ثاني: ${curr_price * 1.10:.2f}</div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="target-purple">🟣 هدف ثالث: ${curr_price * 1.15:.2f}</div>', unsafe_allow_html=True)
                
            # إشارة Predator
            st.info(f"💡 حالة السهم الحالية: السعر ${curr_price:.2f} - تجميع عند مستويات الدعم.")
            
    except:
        st.error("يرجى التأكد من رمز السهم الصحيح.")

st.markdown("---")
st.caption("Yalla Speculate Pro v11.0 | التصميم النهائي الفاخر 2026")
