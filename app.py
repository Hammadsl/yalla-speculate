import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- إعدادات المنصة الاحترافية ---
st.set_page_config(page_title="Yalla Speculate Pro", layout="wide")

# --- تنسيق CSS لمحاكاة منصة "سهم" الفاخرة ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .main { background-color: #0b0e11; color: #ffffff; }
    
    /* ستايل شعار يلا سكالب */
    .logo-container {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #1e222d 0%, #0b0e11 100%);
        border-radius: 15px;
        margin-bottom: 25px;
        border: 1px solid #2d3339;
    }
    .logo-text { font-size: 32px; font-weight: bold; color: #2ecc71; letter-spacing: 1px; }
    .logo-sub { color: #848e9c; font-size: 14px; }

    /* تنسيق كروت الأهداف */
    .target-card {
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        font-weight: bold;
        text-align: center;
        border-right: 8px solid;
    }
    .blue-card { background-color: rgba(0, 123, 255, 0.1); border-color: #007bff; color: #007bff; }
    .yellow-card { background-color: rgba(255, 193, 7, 0.1); border-color: #ffc107; color: #ffc107; }
    .purple-card { background-color: rgba(111, 66, 193, 0.1); border-color: #6f42c1; color: #6f42c1; }
    
    /* تعديل مدخلات البحث */
    .stTextInput input {
        background-color: #1e222d !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        height: 50px !important;
        font-size: 18px !important;
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الهوية العلوية (Header) ---
st.markdown("""
    <div class="logo-container">
        <div class="logo-text">YALLA SCALP <span style="color:white">| يلا سكالب</span></div>
        <div class="logo-sub">منصة تحليل الأسهم الذكية - الإصدار الاحترافي</div>
    </div>
    """, unsafe_allow_html=True)

# --- تقسيم الصفحة (اليمين والمنتصف) ---
col_sidebar, col_main = st.columns([1, 3])

# --- الجانب الأيمن (حاسبة وأخبار) ---
with col_sidebar:
    st.markdown("### 💰 حاسبة الأرباح")
    with st.container():
        s_price = st.number_input("سعر الشراء", value=10.0, format="%.2f")
        qty = st.number_input("الكمية", value=100)
        t_price = st.number_input("السعر المستهدف", value=11.0, format="%.2f")
        res = (t_price - s_price) * qty
        st.info(f"الربح المتوقع: {res:,.2f} $")
    
    st.markdown("---")
    st.markdown("### 📰 نبض السوق")
    st.caption("• تحركات قوية في قطاع أشباه الموصلات.")
    st.caption("• أسهم التكنولوجيا تقود الارتفاع الصباحي.")
    st.caption("• لوسيد (LCID) تقترب من مناطق تجميع.")

# --- المنطقة الوسطى (البحث والتحليل) ---
with col_main:
    # خانة البحث المركزية
    symbol = st.text_input("", placeholder="🔍 ابحث عن رمز السهم (مثال: NVDA, LCID, AAPL)").upper()
    
    if symbol:
        try:
            data = yf.download(symbol, period="1mo", interval="1d")
            if not data.empty:
                last_price = data['Close'].iloc[-1]
                
                # عرض السعر الحالي بشكل كبير
                st.markdown(f"<h2 style='text-align:center;'>{symbol} : <span style='color:#2ecc71;'>${last_price:,.2f}</span></h2>", unsafe_allow_html=True)
                
                # الرسم البياني (شموع يابانية)
                fig = go.Figure(data=[go.Candlestick(x=data.index,
                                open=data['Open'], high=data['High'],
                                low=data['Low'], close=data['Close'],
                                increasing_line_color='#26a69a', decreasing_line_color='#ef5350')])
                fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=350, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig, use_container_width=True)
                
                # قسم الأهداف
                st.markdown("### 🎯 أهداف رادار يلا سكالب")
                t1, t2, t3 = st.columns(3)
                with t1:
                    st.markdown(f'<div class="target-card blue-card">🔵 هدف أول<br>${last_price*1.05:,.2f}</div>', unsafe_allow_html=True)
                with t2:
                    st.markdown(f'<div class="target-card yellow-card">🟡 هدف ثاني<br>${last_price*1.10:,.2f}</div>', unsafe_allow_html=True)
                with t3:
                    st.markdown(f'<div class="target-card purple-card">🟣 هدف ثالث<br>${last_price*1.15:,.2f}</div>', unsafe_allow_html=True)
            else:
                st.warning("لم يتم العثور على بيانات لهذا الرمز.")
        except Exception as e:
            st.error("حدث خطأ أثناء جلب البيانات.")

# --- تذييل الصفحة ---
st.markdown("<br><hr><center style='color:#848e9c;'>جميع الحقوق محفوظة لمنصة يلا سكالب 2026 ©</center>", unsafe_allow_html=True)
