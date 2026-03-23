import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

st.set_page_config(page_title="Yalla Scalp Pro", layout="wide")

st.title("YALLA SCALP PRO 💎")
symbol = st.text_input("🔍 ادخل رمز السهم (مثال: NVDA):", value="NVDA").upper()

if symbol:
    data = yf.Ticker(symbol).history(period="6mo")
    if not data.empty:
        st.metric("السعر الحالي", f"${data['Close'].iloc[-1]:.2f}")
        fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
