import streamlit as st
import yfinance as yf
import smtplib
from email.mime.text import MIMEText
import random
from datetime import datetime, timedelta
import pytz

# --- 🛠️ إعدادات الإرسال (سرية للغاية) ---
GMAIL_USER = 'hammadgmi9@gmail.com'
# استبدل النجوم بالـ 16 حرفاً التي حصلت عليها من جوجل (بدون مسافات)
GMAIL_PASSWORD = 'ydesiqhcvnbxspmj' 

# --- 1. تصميم الواجهة الاحترافية ---
st.set_page_config(page_title="Yalla Speculate Pro", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-header { color: #1e4d2b; text-align: center; font-size: 40px; font-weight: bold; margin-bottom: 20px; }
    .status-card { background: white; padding: 20px; border-radius: 15px; border-right: 5px solid #2E8B57; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .signal-box { padding: 25px; border-radius: 15px; text-align: center; font-size: 20px; font-weight: bold; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك التوقيت (الرياض & نيويورك) ---
saudi_tz = pytz.timezone('Asia/Riyadh')
ny_tz = pytz.timezone('America/New_York')

def get_now_sa(): return datetime.now(saudi_tz)

# --- 3. وظيفة إرسال الإيميل الآلية ---
def send_otp_email(target_email, code):
    msg = MIMEText(f"أهلاً بك في منصة يلا مضاربة.\n\nكود الدخول الخاص بك هو: {code}\n\nهذا الكود يمنحك دخولاً فورياً لمدة 24 ساعة.")
    msg['Subject'] = 'كود دخول Yalla Speculate'
    msg['From'] = f"Yalla Speculate <{GMAIL_USER}>"
    msg['To'] = target_email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, target_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False

# --- 4. نظام الدخول التلقائي وحفظ الجلسة ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<div class='main-header'>YALLA SPECULATE PRO 🚀</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>نظام الدخول الذكي عبر البريد الإلكتروني</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user_mail = st.text_input("أدخل بريدك الإلكتروني:")
        
        if st.button("الحصول على كود الدخول"):
            if "@" in user_mail:
                generated_otp = random.randint(100000, 999999)
                if send_otp_email(user_mail, generated_otp):
                    st.session_state["current_otp"] = str(generated_otp)
                    st.session_state["temp_mail"] = user_mail
                    st.success("📩 تم إرسال كود التحقق لإيميلك بنجاح!")
                else:
                    st.error("❌ فشل الإرسال. تأكد من إعدادات 'كلمة مرور التطبيق' في جوجل.")
            else:
                st.warning("يرجى إدخال إيميل صحيح.")

        if "current_otp" in st.session_state:
            otp_input = st.text_input("أدخل الكود المستلم من الإيميل:")
            if st.button("تفعيل الدخول المجاني"):
                if otp_input == st.session_state["current_otp"]:
                    st.session_state["authenticated"] = True
                    st.session_state["start_time"] = get_now_sa()
                    st.rerun()
                else:
                    st.error("الكود المدخل غير صحيح!")
    st.stop()

# --- 5. فحص فترة الـ 24 ساعة (الأمان الذكي) ---
time_left = st.session_state["start_time"] + timedelta(hours=24) - get_now_sa()

if time_left.total_seconds() <= 0:
    st.markdown("<div class='main-header'>⌛ انتهت الفترة التجريبية</div>", unsafe_allow_html=True)
    st.error("عذراً، انتهت صلاحية الدخول (24 ساعة). يرجى التواصل مع المدير للتفعيل الدائم.")
    if st.button("خروج"):
        st.session_state.clear()
        st.rerun()
    st.stop()

# --- 6. واجهة رادار المضاربة المحترفة ---
st.sidebar.markdown(f"🟢 **متصل الآن**\n\n{st.session_state['temp_mail']}")
st.sidebar.info(f"⏳ المتبقي لجلستك: {str(time_left).split('.')[0]}")

st.sidebar.divider()
st.sidebar.write(f"🇸🇦 الرياض: {get_now_sa().strftime('%I:%M %p')}")
st.sidebar.write(f"🇺🇸 نيويورك: {datetime.now(ny_tz).strftime('%I:%M %p')}")

# حاسبة الأرباح اللحظية
with st.sidebar.expander("💰 حاسبة الأرباح"):
    b_p = st.number_input("سعر الدخول", value=10.0)
    s_p = st.number_input("سعر الهدف", value=10.5)
    qty = st.number_input("الكمية", value=1000)
    st.success(f"الربح: ${(s_p - b_p) * qty:,.2f}")

if st.sidebar.button("تسجيل الخروج"):
    st.session_state.clear()
    st.rerun()

# --- 7. محرك تحليل Predator اللحظي ---
st.markdown("## 📈 رادار تحليل الفرص")
symbol = st.text_input("🔍 ادخل رمز السهم (مثل NVDA, TSLA, AAPL):").upper()

if symbol:
    try:
        with st.spinner('جاري تحليل سيولة الحيتان والمؤشرات...'):
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="5m")
            if not data.empty:
                current_p = data['Close'].iloc[-1]
                
                # حساب RSI مبسط للتحليل
                delta = data['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean().iloc[-1]
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean().iloc[-1]
                rsi = 100 - (100 / (1 + (gain/loss))) if loss != 0 else 50
                
                st.markdown(f"### {symbol} : <span style='color:#2E8B57'>${current_p:.2f}</span>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns(3)
                c1.metric("مؤشر RSI", f"{rsi:.1f}")
                c2.metric("حجم التداول", f"{data['Volume'].iloc[-1]:,.0f}")
                c3.metric("EMA 21", f"${data['Close'].rolling(21).mean().iloc[-1]:.2f}")

                # إشارات قرار Predator
                if rsi < 35:
                    st.markdown("<div class='signal-box' style='background-color:#2E8B57; color:white;'>إشارة Predator: دخول مضاربي - منطقة تجميع 🐋</div>", unsafe_allow_html=True)
                elif rsi > 65:
                    st.markdown("<div class='signal-box' style='background-color:#FF4B4B; color:white;'>إشارة Predator: تضخم سعري - استعداد للخروج ⚠️</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='signal-box' style='background-color:#FFA500; color:white;'>إشارة Predator: انتظار - ابحث عن اختراق ⚖️</div>", unsafe_allow_html=True)

                st.info(f"🎯 الأهداف المقترحة: هدف أول ${current_p*1.03:.2f} | هدف ثاني ${current_p*1.07:.2f} | وقف خسارة ${current_p*0.96:.2f}")
    except:
        st.error("تعذر العثور على بيانات للسهم المذكور.")

st.markdown("<br><hr><center>Yalla Speculate Pro v10.0 | All Rights Reserved 2026</center>", unsafe_allow_html=True)
