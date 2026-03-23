import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- إعدادات الصفحة (ثيم سهم الفاتح) ---
st.set_page_config(page_title="Yalla Scalp Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; background-color: #f4f9f7; }
    
    /* شريط المؤشرات العلوي */
    .ticker-bar { background: #e8f4f0; padding: 10px; border-radius: 10px; display: flex; justify-content: space-around; font-size: 12px; margin-bottom: 20px; border: 1px solid #d1e7dd; }
    .ticker-item { text-align: center; }
    .down { color: #ef5350; } .up { color: #26a69a; }

    /* بطاقات البيانات */
    .info-card { background: white; padding: 15px; border-radius: 12px; border: 1px solid #e0e0e0; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .price-large { font-size: 32px; font-weight: bold; color: #333; }
    
    /* عمق السوق */
    .depth-bar { height: 10px; display: flex; border-radius: 5px; overflow: hidden; margin: 10px 0; }
    .bid { background: #26a69a; } .ask { background: #ef5350; }

    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 20px; padding: 10px 25px; }
    .stTabs [aria-selected="true"] { background-color: #26a69a !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. شريط المؤشرات العلوي (محاكاة) ---
st.markdown("""
    <div class="ticker-bar">
        <div class="ticker-item">مؤشر إس آند بي 500 <br> <span class="down">▼ 1.51%</span></div>
        <div class="ticker-item">نازداك <br> <span class="down">▼ 2.01%</span></div>
        <div class="ticker-item">داو جونز <br> <span class="down">▼ 0.96%</span></div>
        <div class="ticker-item">تداول (TASI) <br> <span class="up">▲ 0.40%</span></div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. الهيكل الرئيسي (جانبي + منتصف) ---
col_main, col_side = st.columns([3, 1])

with col_side:
    st.markdown("### 📋 قائمة المتابعة")
    st.info("LCID لوسيد موتورز \n $10.06")
    st.markdown("---")
    st.markdown("### 💰 حاسبة الأرباح")
    buy_p = st.number_input("سعر الشراء", value=10.0)
    target_p = st.number_input("السعر المستهدف", value=11.5)
    st.success(f"الربح المتوقع: {target_p - buy_p:,.2f}$")

with col_main:
    # البحث
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        symbol = st.text_input("", placeholder="ابحث عن رمز السهم (مثل LCID)...").upper()
    
    if symbol:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")
        
        if not data.empty:
            curr_price = data['Close'].iloc[-1]
            change = curr_price - data['Open'].iloc[0]
            pct_change = (change / data['Open'].iloc[0]) * 100
            
            # عرض رأس الصفحة للسهم
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.markdown(f"<h1>{symbol} <small style='font-size:15px; color:grey;'>لوسيد موتورز</small></h1>", unsafe_allow_html=True)
                st.markdown(f"<div class='price-large'>${curr_price:,.2f} <span style='font-size:18px;' class='{'up' if change > 0 else 'down'}'>{change:+.2f} ({pct_change:+.2f}%)</span></div>", unsafe_allow_html=True)
            
            # بطاقات تفصيلية
            st.markdown("<br>", unsafe_allow_html=True)
            i1, i2, i3, i4 = st.columns(4)
            i1.markdown(f"<div class='info-card'><small>القيمة السوقية</small><br><b>3.30B</b></div>", unsafe_allow_html=True)
            i2.markdown(f"<div class='info-card'><small>الحجم</small><br><b>5.82M</b></div>", unsafe_allow_html=True)
            i3.markdown(f"<div class='info-card'><small>الافتتاح</small><br><b>10.30</b></div>", unsafe_allow_html=True)
            i4.markdown(f"<div class='info-card'><small>نطاق اليوم</small><br><b>9.98 - 10.44</b></div>", unsafe_allow_html=True)

            # الرسم البياني والتبويبات
            tab1, tab2, tab3 = st.tabs(["📊 الرسم البياني", "📰 الأخبار", "💧 السيولة"])
            
            with tab1:
                fig = go.Figure(data=[go.Scatter(x=data.index, y=data['Close'], fill='tozeroy', line=dict(color='#26a69a'))])
                fig.update_layout(template="plotly_white", height=400, margin=dict(l=0,r=0,t=0,b=0))
                st.plotly_chart(fig, use_container_width=True)
                
                # عمق السوق (محاكاة)
                st.markdown("### ⚖️ عمق السوق")
                st.markdown("""
                    <div style="display:flex; justify-content:space-between;"><small>طلب 19.61%</small><small>عرض 80.39%</small></div>
                    <div class="depth-bar"><div class="bid" style="width:20%"></div><div class="ask" style="width:80%"></div></div>
                """, unsafe_allow_html=True)
            
            with tab2:
                st.write("• هل ينبغي أن تتطلب منصة السيارات الجديدة من لوسيد...")
                st.write("• لوسيد تعلن عن نتائج الربع الأول القوية...")

            # أهداف يلا سكالب
            st.markdown("### 🎯 أهداف Predator")
            t1, t2, t3 = st.columns(3)
            t1.markdown(f'<div style="background:#e3f2fd; padding:10px; border-radius:10px; border-right:5px solid #2196f3; text-align:center;"><b>هدف أول</b><br>${curr_price*1.05:,.2f}</div>', unsafe_allow_html=True)
            t2.markdown(f'<div style="background:#fffde7; padding:10px; border-radius:10px; border-right:5px solid #fbc02d; text-align:center;"><b>هدف ثاني</b><br>${curr_price*1.10:,.2f}</div>', unsafe_allow_html=True)
            t3.markdown(f'<div style="background:#f3e5f5; padding:10px; border-radius:10px; border-right:5px solid #9c27b0; text-align:center;"><b>هدف ثالث</b><br>${curr_price*1.15:,.2f}</div>', unsafe_allow_html=True)
