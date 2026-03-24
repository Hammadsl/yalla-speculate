import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="منصة التحليل الفني", page_icon="📊",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<script>document.documentElement.lang='ar';document.documentElement.setAttribute('dir','rtl');</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
*,body,.stApp{font-family:'Tajawal',sans-serif!important;}
body,.stApp{background:#080d15!important;color:#e2e8f0!important;direction:rtl;}
/* Force English (Latin) numerals everywhere */
*{font-variant-numeric:tabular-nums;unicode-bidi:plaintext;}
.card-val,.m-val,.sig-box,.calc-result,.tgt-card,.calc-row,
[data-testid="stMetricValue"],
.stNumberInput input,.stTextInput input{
    font-feature-settings:"tnum";
    font-variant-numeric: tabular-nums;
    direction:ltr;
    unicode-bidi: embed;
}
.block-container{padding:1rem 1.5rem 2rem;max-width:1600px;}

/* search */
.search-box{background:#0d1422;border:1px solid #1e2d45;border-radius:16px;padding:24px 28px;margin-bottom:18px;}
.platform-title{font-size:34px;font-weight:800;color:#FFD700;text-align:center;margin-bottom:4px;letter-spacing:.5px;}
.platform-sub{text-align:center;color:#374151;font-size:13px;margin-bottom:16px;}

/* signal */
.sig-box{border-radius:14px;padding:20px 16px;text-align:center;}
.sig-enter-now  {background:#001800;border:2px solid #00C851;}
.sig-ready-enter{background:#0b1f0d;border:2px solid #5DBF6A;}
.sig-ready-exit {background:#1f0808;border:2px solid #E06060;}
.sig-exit-now   {background:#140000;border:2px solid #BB0000;}

/* cards */
.card{background:#0d1422;border:1px solid #1a2540;border-radius:10px;padding:12px 10px;text-align:center;}
.card-lbl{color:#374151;font-size:11px;margin-bottom:3px;}
.card-val{font-size:18px;font-weight:700;}
.cg{color:#00C851!important;}.cr{color:#FF4444!important;}
.cy{color:#FFD700!important;}.cb{color:#60A5FA!important;}.cw{color:#9ca3af!important;}

/* targets */
.tgt-card{background:#0d1422;border:1px solid #1a2540;border-radius:10px;padding:14px 10px;text-align:center;}

/* calculator */
.calc-box{background:#0d1422;border:1px solid #1a2540;border-radius:14px;padding:18px 16px;}
.calc-title{color:#FFD700;font-size:15px;font-weight:700;margin-bottom:14px;border-right:3px solid #FFD700;padding-right:8px;}
.calc-row{display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #111e30;font-size:13px;}
.calc-result{background:#060c14;border-radius:10px;padding:12px;margin-top:12px;text-align:center;}

/* section title */
.sec{color:#FFD700;font-size:15px;font-weight:700;margin:16px 0 8px;padding-right:8px;border-right:3px solid #FFD700;}

/* market/fear gauge */
.gauge-box{background:#0d1422;border:1px solid #1a2540;border-radius:10px;padding:12px;text-align:center;}

/* prog bar */
.pb{background:#1a2540;border-radius:99px;height:7px;margin-top:5px;overflow:hidden;}
.pf{height:7px;border-radius:99px;}

/* indicator breakdown */
.ind-row{display:flex;justify-content:space-between;padding:5px 8px;background:#060c14;border-radius:6px;margin-bottom:3px;font-size:12px;}

/* streamlit overrides */
.stButton>button{background:linear-gradient(90deg,#FFD700,#FFA500)!important;color:#000!important;
  font-weight:700!important;border:none!important;border-radius:10px!important;font-size:15px!important;}
.stTextInput>div>input{background:#0d1422!important;border:1px solid #1e2d45!important;
  color:#e2e8f0!important;border-radius:10px!important;font-size:15px!important;}
.stNumberInput>div>div>input{background:#0d1422!important;border:1px solid #1e2d45!important;
  color:#e2e8f0!important;border-radius:8px!important;}
.stSelectbox>div>div{background:#0d1422!important;border:1px solid #1e2d45!important;color:#e2e8f0!important;}
div[data-testid="stSidebar"]{background:#06090f!important;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# INDICATOR FUNCTIONS
# ═══════════════════════════════════════

def f(s): return float(s.dropna().iloc[-1]) if len(s.dropna()) else 0.0

def calc_rsi(c, n=14):
    d=c.diff(); g=d.clip(lower=0).rolling(n).mean(); l=(-d.clip(upper=0)).rolling(n).mean()
    return 100-100/(1+g/(l+1e-9))

def calc_macd(c, fast=12, slow=26, sig=9):
    ef=c.ewm(span=fast,adjust=False).mean(); es=c.ewm(span=slow,adjust=False).mean()
    m=ef-es; s=m.ewm(span=sig,adjust=False).mean()
    return m, s, m-s

def calc_bb(c, n=20, k=2):
    m=c.rolling(n).mean(); sd=c.rolling(n).std()
    return m+k*sd, m, m-k*sd

def calc_stoch(h, l, c, kp=14, dp=3):
    ll=l.rolling(kp).min(); hh=h.rolling(kp).max()
    k=100*(c-ll)/(hh-ll+1e-9)
    return k, k.rolling(dp).mean()

def calc_atr(h, l, c, n=14):
    tr=pd.concat([(h-l),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    return tr.rolling(n).mean()

def calc_adx(h, l, c, n=14):
    tr=pd.concat([(h-l),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    dmp=(h-h.shift()).clip(lower=0); dmm=(l.shift()-l).clip(lower=0)
    dmp=dmp.where(dmp>dmm,0); dmm=dmm.where(dmm>dmp,0)
    a=tr.ewm(span=n,adjust=False).mean()
    dip=100*dmp.ewm(span=n,adjust=False).mean()/(a+1e-9)
    dim=100*dmm.ewm(span=n,adjust=False).mean()/(a+1e-9)
    dx=100*(dip-dim).abs()/(dip+dim+1e-9)
    return dx.ewm(span=n,adjust=False).mean(), dip, dim

def calc_cci(h, l, c, n=20):
    tp=(h+l+c)/3
    return (tp-tp.rolling(n).mean())/(0.015*tp.rolling(n).std()+1e-9)

def calc_wr(h, l, c, n=14):
    hh=h.rolling(n).max(); ll=l.rolling(n).min()
    return -100*(hh-c)/(hh-ll+1e-9)

def calc_mfi(h, l, c, v, n=14):
    tp=(h+l+c)/3; mf=tp*v
    pos=mf.where(tp>tp.shift(),0).rolling(n).sum()
    neg=mf.where(tp<tp.shift(),0).rolling(n).sum()
    return 100-100/(1+pos/(neg+1e-9))

def calc_obv(c, v):
    return (np.sign(c.diff())*v).fillna(0).cumsum()

def calc_cmf(h, l, c, v, n=20):
    mfv=((c-l)-(h-c))/(h-l+1e-9)*v
    return mfv.rolling(n).sum()/(v.rolling(n).sum()+1e-9)

def calc_sar(h, l, af=0.02, af_max=0.2):
    sar=np.zeros(len(h)); trend=np.ones(len(h))
    sar[0]=float(l.iloc[0]); ep=float(h.iloc[0]); a=af
    for i in range(1,len(h)):
        ps=sar[i-1]
        if trend[i-1]==1:
            sar[i]=ps+a*(ep-ps)
            sar[i]=min(sar[i],float(l.iloc[max(0,i-1)]),float(l.iloc[max(0,i-2)]))
            if float(l.iloc[i])<sar[i]: trend[i]=-1; sar[i]=ep; ep=float(l.iloc[i]); a=af
            else:
                trend[i]=1
                if float(h.iloc[i])>ep: ep=float(h.iloc[i]); a=min(a+af,af_max)
        else:
            sar[i]=ps+a*(ep-ps)
            sar[i]=max(sar[i],float(h.iloc[max(0,i-1)]),float(h.iloc[max(0,i-2)]))
            if float(h.iloc[i])>sar[i]: trend[i]=1; sar[i]=ep; ep=float(h.iloc[i]); a=af
            else:
                trend[i]=-1
                if float(l.iloc[i])<ep: ep=float(l.iloc[i]); a=min(a+af,af_max)
    return pd.Series(sar,index=h.index), pd.Series(trend,index=h.index)

def calc_fibonacci(c):
    hi=float(c.tail(60).max()); lo=float(c.tail(60).min()); d=hi-lo
    return {"0%":hi,"23.6%":hi-0.236*d,"38.2%":hi-0.382*d,
            "50%":hi-0.5*d,"61.8%":hi-0.618*d,"100%":lo}

def calc_pivot(h, l, c):
    hv=float(h.tail(20).max()); lv=float(l.tail(20).min()); cv=float(c.iloc[-1])
    p=(hv+lv+cv)/3
    return {"P":p,"R1":2*p-lv,"R2":p+(hv-lv),"S1":2*p-hv,"S2":p-(hv-lv)}

def smart_targets(px, atr_v, sig_type, fibs, pivots):
    """Hybrid targets: Fibonacci + Pivot + ATR"""
    if sig_type in ("buy","watch_buy"):
        fib382 = fibs["38.2%"]; fib618 = fibs["61.8%"]
        r1=pivots["R1"]; r2=pivots["R2"]
        t1 = fib382 if fib382 > px else px + atr_v*1.5
        t2 = r1     if r1 > t1    else px + atr_v*3.0
        t3 = r2     if r2 > t2    else fib618 if fib618>t2 else px+atr_v*5.0
        sl = pivots["S1"] if pivots["S1"] < px else px - atr_v*2.0
        return [
            ("🎯 الهدف 1", round(t1,2), "#00C851"),
            ("🎯 الهدف 2", round(t2,2), "#00A040"),
            ("🎯 الهدف 3", round(t3,2), "#007030"),
            ("🛑 وقف الخسارة", round(sl,2), "#FF4444"),
        ]
    else:
        s1=pivots["S1"]; s2=pivots["S2"]
        fib382=fibs["38.2%"]; fib618=fibs["61.8%"]
        t1 = s1      if s1 < px else px - atr_v*1.5
        t2 = s2      if s2 < t1 else px - atr_v*3.0
        t3 = fib618  if fib618 < t2 else px - atr_v*5.0
        sl = pivots["R1"] if pivots["R1"] > px else px + atr_v*2.0
        return [
            ("📉 هدف هبوط 1", round(t1,2), "#FF6644"),
            ("📉 هدف هبوط 2", round(t2,2), "#CC3322"),
            ("📉 هدف هبوط 3", round(t3,2), "#AA1100"),
            ("↩️ إعادة دخول",  round(sl,2), "#FFD700"),
        ]

def market_detect(ticker):
    t=ticker.upper()
    if t.endswith(".SR"): return "SA","SAR","ر.س"
    return "US","USD","$"

def fmt(v, d=2):
    result = f"{v:,.{d}f}"
    ar_digits = '٠١٢٣٤٥٦٧٨٩'
    en_digits = '0123456789'
    for ar, en in zip(ar_digits, en_digits):
        result = result.replace(ar, en)
    return result

# ═══════════════════════════════════════
# MASTER SIGNAL SCORE  (all indicators)
# ═══════════════════════════════════════

def master_score(rsi, macd, macd_s, px, ema20, ema50, sma200,
                 stk, bbu, bbl, vol, vol_avg,
                 adx, dip, dim, cci, wr, mfi, cmf, sar_tr):
    sc = 50
    indicators = {}

    # RSI
    if rsi < 30:    sc+=8;  indicators["RSI"]="ذروة بيع 🟢"
    elif rsi < 45:  sc+=10; indicators["RSI"]="قوة صعودية 🟢"
    elif rsi < 60:  sc+=5;  indicators["RSI"]="محايد ⚪"
    elif rsi < 70:  sc+=0;  indicators["RSI"]="قريب الذروة 🟡"
    else:           sc-=20; indicators["RSI"]="ذروة شراء 🔴"

    # MACD
    if macd > macd_s: sc+=18; indicators["MACD"]="صاعد ✅"
    else:             sc-=18; indicators["MACD"]="هابط ❌"

    # Moving Averages
    ma_pts = 0
    if px > ema20:  ma_pts += 5
    if px > ema50:  ma_pts += 7
    if px > sma200: ma_pts += 8
    sc += ma_pts - 10
    indicators["MA"] = "فوق المتوسطات 🟢" if ma_pts >= 15 else "تحت المتوسطات 🔴" if ma_pts <= 5 else "مختلطة ⚪"

    # ADX
    if adx > 25:
        if dip > dim: sc+=10; indicators["ADX"]="اتجاه صاعد قوي 🟢"
        else:         sc-=10; indicators["ADX"]="اتجاه هابط قوي 🔴"
    else: sc+=0; indicators["ADX"]="تداول جانبي ⚪"

    # Stochastic
    if stk < 20:    sc+=8;  indicators["Stoch"]="ذروة بيع 🟢"
    elif stk > 80:  sc-=8;  indicators["Stoch"]="ذروة شراء 🔴"
    else:           sc+=2;  indicators["Stoch"]="محايد ⚪"

    # Bollinger
    if px < bbl:    sc+=6;  indicators["BB"]="تحت النطاق 🟢"
    elif px > bbu:  sc-=6;  indicators["BB"]="فوق النطاق 🔴"
    else:           sc+=1;  indicators["BB"]="داخل النطاق ⚪"

    # CCI
    if cci < -100:  sc+=5;  indicators["CCI"]="ذروة بيع 🟢"
    elif cci > 100: sc-=5;  indicators["CCI"]="ذروة شراء 🔴"
    else:           sc+=1;  indicators["CCI"]="محايد ⚪"

    # Williams %R
    if wr < -80:    sc+=5;  indicators["W%R"]="ذروة بيع 🟢"
    elif wr > -20:  sc-=5;  indicators["W%R"]="ذروة شراء 🔴"
    else:           sc+=1;  indicators["W%R"]="محايد ⚪"

    # MFI
    if mfi < 20:    sc+=4;  indicators["MFI"]="ضغط بيع 🟢"
    elif mfi > 80:  sc-=4;  indicators["MFI"]="ضغط شراء 🔴"
    else:           sc+=1;  indicators["MFI"]="طبيعي ⚪"

    # CMF
    if cmf > 0.1:   sc+=5;  indicators["CMF"]="تدفق شراء 🟢"
    elif cmf < -0.1:sc-=5;  indicators["CMF"]="تدفق بيع 🔴"
    else:           sc+=0;  indicators["CMF"]="محايد ⚪"

    # Volume
    vr = vol/(vol_avg+1e-9)
    if vr > 1.5:    sc+=5;  indicators["Volume"]="تأكيد حجم 🟢"
    elif vr < 0.5:  sc-=3;  indicators["Volume"]="حجم ضعيف 🔴"
    else:           sc+=1;  indicators["Volume"]="طبيعي ⚪"

    # SAR
    if sar_tr == 1: sc+=5;  indicators["SAR"]="اتجاه صاعد 🟢"
    else:           sc-=5;  indicators["SAR"]="اتجاه هابط 🔴"

    return max(0, min(100, int(sc))), indicators

def signal_from_score(score):
    if score >= 65:
        return {"label":"دخول الآن","en":"BUY NOW","icon":"▲",
                "cls":"sig-enter-now","color":"#00C851","type":"buy"}
    elif score >= 45:
        return {"label":"استعداد دخول","en":"READY TO BUY","icon":"◆",
                "cls":"sig-ready-enter","color":"#5DBF6A","type":"watch_buy"}
    elif score >= 28:
        return {"label":"استعداد خروج","en":"READY TO SELL","icon":"◆",
                "cls":"sig-ready-exit","color":"#E06060","type":"watch_sell"}
    else:
        return {"label":"خروج الآن","en":"SELL NOW","icon":"▼",
                "cls":"sig-exit-now","color":"#BB0000","type":"sell"}

def fear_greed(rsi, stk, bbu, bbl, px, vol, vol_avg):
    score = 50
    if rsi > 70: score += 25
    elif rsi < 30: score -= 25
    else: score += (rsi - 50) * 0.5
    if stk > 80: score += 15
    elif stk < 20: score -= 15
    bp = (px - bbl) / (bbu - bbl + 1e-9) * 100
    score += (bp - 50) * 0.2
    vr = vol / (vol_avg + 1e-9)
    if vr > 1.5: score += 10
    score = max(0, min(100, score))
    if score >= 75: return score, "جشع شديد 🤑", "#FF4444"
    elif score >= 55: return score, "جشع 😊", "#FF9800"
    elif score >= 45: return score, "محايد 😐", "#FFD700"
    elif score >= 25: return score, "خوف 😟", "#60A5FA"
    else: return score, "خوف شديد 😱", "#00C851"

def market_state(px, ema20, ema50, sma200, adx):
    if px > ema50 and px > sma200 and adx > 25:
        return "📈 اتجاه صاعد قوي", "#00C851"
    elif px < ema50 and px < sma200 and adx > 25:
        return "📉 اتجاه هابط قوي", "#FF4444"
    elif adx < 20:
        return "📊 تداول جانبي", "#FFD700"
    elif px > ema50:
        return "📈 صاعد معتدل", "#5DBF6A"
    else:
        return "📉 هابط معتدل", "#E06060"

# ═══════════════════════════════════════
# HEADER
# ═══════════════════════════════════════

st.markdown("""
<div class="search-box">
  <div class="platform-title">📊 منصة التحليل الفني المتقدم</div>
  <div class="platform-sub">أسعار مباشرة • تحليل احترافي • حاسبة الأرباح</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# SEARCH
# ═══════════════════════════════════════
col_s, col_b, col_p, col_i = st.columns([4, 1, 1.5, 1.5])
with col_s:
    ticker = st.text_input("", placeholder="رمز السهم — مثال: 2222.SR أو AAPL",
                           label_visibility="collapsed").upper().strip()
with col_b:
    analyze = st.button("🔍 تحليل", use_container_width=True)
with col_p:
    period = st.selectbox("", ["3mo","6mo","1y","2y"], index=1,
                          format_func=lambda x:{"3mo":"3 أشهر","6mo":"6 أشهر","1y":"سنة","2y":"سنتين"}[x],
                          label_visibility="collapsed")
with col_i:
    interval = st.selectbox("", ["1d","1wk"], index=0,
                            format_func=lambda x:{"1d":"يومي","1wk":"أسبوعي"}[x],
                            label_visibility="collapsed")

# ═══════════════════════════════════════
# MAIN ANALYSIS
# ═══════════════════════════════════════
if analyze and ticker:
    market, currency, sym = market_detect(ticker)

    with st.spinner("⏳ جاري تحميل البيانات وتحليل كل المؤشرات..."):
        try:
            data = yf.download(ticker, period=period, interval=interval,
                               progress=False, auto_adjust=True)
            try:
                info = yf.Ticker(ticker).info or {}
            except:
                info = {}
        except Exception as e:
            st.error(f"❌ خطأ: {e}"); st.stop()

    if data is None or data.empty or len(data) < 30:
        st.error("❌ بيانات غير كافية. تحقق من الرمز.")
        st.info("💡 السعودي: 2222.SR | الأمريكي: AAPL, TSLA, MSFT")
        st.stop()

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    C = data["Close"].astype(float)
    H = data["High"].astype(float)
    L = data["Low"].astype(float)
    V = data["Volume"].astype(float)
    O = data["Open"].astype(float)

    # ── All indicators (background) ──
    rsi_s             = calc_rsi(C)
    macd_l, macd_s, macd_h = calc_macd(C)
    bbu_s, bbm_s, bbl_s   = calc_bb(C)
    stk_s, std_s          = calc_stoch(H, L, C)
    atr_s                 = calc_atr(H, L, C)
    adx_s, dip_s, dim_s   = calc_adx(H, L, C)
    cci_s                 = calc_cci(H, L, C)
    wr_s                  = calc_wr(H, L, C)
    mfi_s                 = calc_mfi(H, L, C, V)
    obv_s                 = calc_obv(C, V)
    cmf_s                 = calc_cmf(H, L, C, V)
    sar_s, sar_tr_s       = calc_sar(H, L)
    ema20_s               = C.ewm(span=20, adjust=False).mean()
    ema50_s               = C.ewm(span=50, adjust=False).mean()
    sma200_s              = C.rolling(200).mean()
    vol_ma20              = V.rolling(20).mean()
    fibs                  = calc_fibonacci(C)
    pivots                = calc_pivot(H, L, C)

    # Latest values
    px       = float(C.iloc[-1])
    rsi_v    = f(rsi_s)
    macd_v   = f(macd_l); macd_sv = f(macd_s)
    bbu_v    = f(bbu_s);  bbl_v   = f(bbl_s); bbm_v = f(bbm_s)
    stk_v    = f(stk_s);  std_v   = f(std_s)
    atr_v    = f(atr_s)
    adx_v    = f(adx_s);  dip_v   = f(dip_s); dim_v = f(dim_s)
    cci_v    = f(cci_s)
    wr_v     = f(wr_s)
    mfi_v    = f(mfi_s)
    cmf_v    = f(cmf_s)
    sar_tr_v = float(sar_tr_s.iloc[-1])
    ema20_v  = f(ema20_s); ema50_v = f(ema50_s); sma200_v = f(sma200_s)
    vol_v    = float(V.iloc[-1]); vol_avg = f(vol_ma20)
    prev_px  = float(C.iloc[-2]) if len(C) > 1 else px
    chg_pct  = (px - prev_px) / prev_px * 100

    # Score + signal
    score, ind_breakdown = master_score(
        rsi_v, macd_v, macd_sv, px, ema20_v, ema50_v, sma200_v,
        stk_v, bbu_v, bbl_v, vol_v, vol_avg,
        adx_v, dip_v, dim_v, cci_v, wr_v, mfi_v, cmf_v, sar_tr_v)
    sig = signal_from_score(score)

    # Targets (hybrid: Fib + Pivot + ATR)
    targets = smart_targets(px, atr_v, sig["type"], fibs, pivots)

    # Fear & Greed
    fg_score, fg_label, fg_color = fear_greed(rsi_v, stk_v, bbu_v, bbl_v, px, vol_v, vol_avg)

    # Market state
    mkt_label, mkt_color = market_state(px, ema20_v, ema50_v, sma200_v, adx_v)

    # Risk/Reward
    stop_px = targets[3][1]
    risk    = abs(px - stop_px)
    rr_list = []
    for i in range(3):
        reward = abs(targets[i][1] - px)
        rr = reward / risk if risk > 0 else 0
        rr_list.append(rr)

    company = info.get("longName", ticker) or ticker

    # ═══════════════════════════════════════
    # LAYOUT: chart col + calculator col
    # ═══════════════════════════════════════
    chart_col, calc_col = st.columns([3, 1])

    # ── CALCULATOR (right column) ──────────
    with calc_col:
        st.markdown(f"<div style='color:#374151;font-size:12px;margin-bottom:8px'>{company} | {market} | {currency}</div>",
                    unsafe_allow_html=True)

        # Signal box
        st.markdown(f"""
        <div class="sig-box {sig['cls']}" style="margin-bottom:12px">
            <div style="color:{sig['color']};font-size:30px;font-weight:800">{sig['icon']} {sig['label']}</div>
            <div style="color:{sig['color']};font-size:11px;margin-top:2px">{sig['en']}</div>
            <div style="color:{sig['color']};font-size:13px;font-weight:600;margin-top:8px">قوة الإشارة: {score}/100</div>
            <div class="pb"><div class="pf" style="width:{score}%;background:{sig['color']}"></div></div>
        </div>""", unsafe_allow_html=True)

        # Market state + Fear/Greed
        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown(f"""<div class="gauge-box">
                <div style="color:#374151;font-size:10px">حالة السوق</div>
                <div style="color:{mkt_color};font-size:12px;font-weight:600;margin-top:3px">{mkt_label}</div>
            </div>""", unsafe_allow_html=True)
        with mc2:
            st.markdown(f"""<div class="gauge-box">
                <div style="color:#374151;font-size:10px">الخوف والجشع</div>
                <div style="color:{fg_color};font-size:12px;font-weight:600;margin-top:3px">{fg_label}</div>
                <div style="color:#374151;font-size:10px">{fg_score:.0f}/100</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # ── Calculator ──
        st.markdown("<div class='calc-box'>", unsafe_allow_html=True)
        st.markdown("<div class='calc-title'>💰 حاسبة الأرباح</div>", unsafe_allow_html=True)

        shares   = st.number_input("عدد الأسهم", min_value=1, value=100, step=1, key="sh")
        entry_px = st.number_input(f"سعر الدخول ({sym})", min_value=0.01,
                                   value=round(px, 2), step=0.01, key="ep",
                                   format="%.2f")
        tgt_options = {
            f"الهدف 1  {sym}{fmt(targets[0][1])}": targets[0][1],
            f"الهدف 2  {sym}{fmt(targets[1][1])}": targets[1][1],
            f"الهدف 3  {sym}{fmt(targets[2][1])}": targets[2][1],
            "سعر مخصص": None,
        }
        chosen = st.selectbox("السعر المستهدف", list(tgt_options.keys()), key="tgt")
        if tgt_options[chosen] is None:
            exit_px = st.number_input(f"أدخل السعر ({sym})", min_value=0.01,
                                      value=round(px*1.05,2), step=0.01, key="cust", format="%.2f")
        else:
            exit_px = tgt_options[chosen]

        comm_rate = 0.0015
        cost_in   = shares * entry_px
        cost_out  = shares * exit_px
        comm_in   = cost_in  * comm_rate
        comm_out  = cost_out * comm_rate
        gross_pnl = cost_out - cost_in
        net_pnl   = gross_pnl - comm_in - comm_out
        pct_pnl   = net_pnl / cost_in * 100 if cost_in > 0 else 0
        is_profit = net_pnl >= 0
        pnl_color = "#00C851" if is_profit else "#FF4444"
        pnl_icon  = "📈" if is_profit else "📉"

        usd_rate  = 3.75 if currency == "SAR" else 1.0
        net_usd   = net_pnl / usd_rate

        st.markdown(f"""
        <div class="calc-result">
            <div style="color:#374151;font-size:11px;margin-bottom:6px">النتيجة الصافية</div>
            <div style="color:{pnl_color};font-size:26px;font-weight:800">{pnl_icon} {sym}{fmt(abs(net_pnl))}</div>
            <div style="color:{pnl_color};font-size:14px;font-weight:600">{pct_pnl:+.2f}%</div>
            {'<div style="color:#374151;font-size:11px;margin-top:4px">≈ $' + fmt(abs(net_usd)) + ' USD</div>' if currency=='SAR' else ''}
        </div>
        <div style="margin-top:10px">
            <div class="calc-row"><span style="color:#374151">رأس المال</span><span style="color:#e2e8f0">{sym}{fmt(cost_in)}</span></div>
            <div class="calc-row"><span style="color:#374151">الربح الخام</span><span style="color:{pnl_color}">{sym}{fmt(gross_pnl):}</span></div>
            <div class="calc-row"><span style="color:#374151">العمولة (0.15%×2)</span><span style="color:#FF9800">-{sym}{fmt(comm_in+comm_out)}</span></div>
            <div class="calc-row"><span style="color:#374151">وقف الخسارة</span><span style="color:#FF4444">{sym}{fmt(stop_px)}</span></div>
        </div>
        """, unsafe_allow_html=True)

        # R/R comparison
        st.markdown("<div style='margin-top:12px;'>", unsafe_allow_html=True)
        for i, (rr, tgt) in enumerate(zip(rr_list, targets[:3])):
            rr_ok = rr >= 2.0
            rr_clr = "#00C851" if rr >= 2 else "#FF9800" if rr >= 1 else "#FF4444"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                 padding:5px 8px;background:#060c14;border-radius:6px;margin-bottom:3px;font-size:12px">
                <span style="color:#374151">{tgt[0]}</span>
                <span style="color:{tgt[2]}">{sym}{fmt(tgt[1])}</span>
                <span style="color:{rr_clr}">R/R {rr:.1f}x {"✅" if rr_ok else "⚠️"}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Indicator breakdown
        st.markdown("<div style='margin-top:12px;'>", unsafe_allow_html=True)
        st.markdown("<div style='color:#374151;font-size:11px;margin-bottom:4px'>تفصيل المؤشرات</div>", unsafe_allow_html=True)
        for k, v in ind_breakdown.items():
            clr = "#00C851" if "🟢" in v else "#FF4444" if "❌" in v or "🔴" in v else "#9ca3af"
            st.markdown(f"""<div class="ind-row">
                <span style="color:#374151">{k}</span>
                <span style="color:{clr}">{v}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── CHART (left column) ────────────────
    with chart_col:
        # Key metrics row
        mco = st.columns(6)
        mets = [
            ("السعر",   f"{sym}{fmt(px)}",        "cy"),
            ("التغيير", f"{chg_pct:+.2f}%",       "cg" if chg_pct>=0 else "cr"),
            ("RSI",     fmt(rsi_v,1),              "cr" if rsi_v>70 else "cg" if rsi_v<30 else "cw"),
            ("ADX",     fmt(adx_v,1),              "cb" if adx_v>25 else "cw"),
            ("ATR",     fmt(atr_v,2),              "cw"),
            ("Volume",  f"{vol_v/1e6:.1f}M" if vol_v>1e5 else fmt(vol_v,0),
                        "cg" if vol_v>vol_avg else "cw"),
        ]
        for i,(lbl,val,cls) in enumerate(mets):
            with mco[i]:
                st.markdown(f"""<div class="card">
                    <div class="card-lbl">{lbl}</div>
                    <div class="card-val {cls}">{val}</div>
                </div>""", unsafe_allow_html=True)

        # ── CHART ──
        fig = make_subplots(
            rows=5, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.018,
            row_heights=[0.46, 0.155, 0.135, 0.135, 0.115],
            subplot_titles=("", "RSI (14)", "MACD", "Stochastic (14,3)", "ADX")
        )

        # ── Candlestick ONLY (no indicators on candles) ──
        fig.add_trace(go.Candlestick(
            x=data.index, open=O, high=H, low=L, close=C,
            name="السعر",
            increasing=dict(fillcolor="#00C851", line=dict(color="#00C851", width=0.8)),
            decreasing=dict(fillcolor="#FF4444", line=dict(color="#FF4444", width=0.8))
        ), row=1, col=1)

        # ── Target lines ONLY on the candle chart ──
        tgt_styles = [
            dict(color="#00C851", dash="dash",  width=1.8),
            dict(color="#00A040", dash="dash",  width=1.5),
            dict(color="#007030", dash="dash",  width=1.5),
            dict(color="#FF4444", dash="dot",   width=2.0),
        ]
        for (name, tpx, clr), style in zip(targets, tgt_styles):
            pct = (tpx - px) / px * 100
            fig.add_hline(
                y=tpx, row=1, col=1,
                line=dict(color=style["color"], width=style["width"], dash=style["dash"]),
                annotation_text=f" {name}: {sym}{fmt(tpx)} ({pct:+.1f}%)",
                annotation_position="right",
                annotation_font=dict(size=11, color=style["color"]),
            )

        # ── RSI sub-chart ──
        fig.add_trace(go.Scatter(x=data.index, y=rsi_s, name="RSI",
                                  line=dict(color="#E91E63", width=1.8)), row=2, col=1)
        fig.add_hrect(y0=70, y1=100, fillcolor="rgba(255,68,68,0.05)", line_width=0, row=2, col=1)
        fig.add_hrect(y0=0,  y1=30,  fillcolor="rgba(0,200,81,0.05)",  line_width=0, row=2, col=1)
        for y, c in [(70,"#FF4444"),(50,"#333"),(30,"#00C851")]:
            fig.add_hline(y=y, line=dict(color=c, width=0.8, dash="dot"), row=2, col=1)

        # ── MACD sub-chart ──
        hcols = ["#00C851" if v >= 0 else "#FF4444" for v in macd_h.fillna(0)]
        fig.add_trace(go.Bar(x=data.index, y=macd_h, name="Hist",
                              marker_color=hcols, opacity=0.7), row=3, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=macd_l, name="MACD",
                                  line=dict(color="#FF9800", width=1.5)), row=3, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=macd_s, name="Signal",
                                  line=dict(color="#2196F3", width=1.5)), row=3, col=1)
        fig.add_hline(y=0, line=dict(color="#222", width=0.8), row=3, col=1)

        # ── Stochastic sub-chart ──
        fig.add_trace(go.Scatter(x=data.index, y=stk_s, name="%K",
                                  line=dict(color="#00BCD4", width=1.5)), row=4, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=std_s, name="%D",
                                  line=dict(color="#FF5722", width=1.5)), row=4, col=1)
        fig.add_hrect(y0=80, y1=100, fillcolor="rgba(255,68,68,0.05)", line_width=0, row=4, col=1)
        fig.add_hrect(y0=0,  y1=20,  fillcolor="rgba(0,200,81,0.05)",  line_width=0, row=4, col=1)
        for y, c in [(80,"#FF4444"),(20,"#00C851")]:
            fig.add_hline(y=y, line=dict(color=c, width=0.8, dash="dot"), row=4, col=1)

        # ── ADX sub-chart ──
        fig.add_trace(go.Scatter(x=data.index, y=adx_s, name="ADX",
                                  line=dict(color="#FFD700", width=1.8)), row=5, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=dip_s, name="DI+",
                                  line=dict(color="#00C851", width=1.2, dash="dot")), row=5, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=dim_s, name="DI-",
                                  line=dict(color="#FF4444", width=1.2, dash="dot")), row=5, col=1)
        fig.add_hline(y=25, line=dict(color="#333", width=0.8, dash="dot"), row=5, col=1)

        fig.update_layout(
            template="plotly_dark",
            height=820,
            showlegend=False,
            xaxis_rangeslider_visible=False,
            plot_bgcolor="#080d15",
            paper_bgcolor="#080d15",
            font=dict(family="Tajawal, sans-serif", color="#6b7280", size=11),
            margin=dict(l=4, r=120, t=16, b=4),
            separators=",.",
        )
        # Force English numerals on all axes
        for axis in ['xaxis','xaxis2','xaxis3','xaxis4','xaxis5',
                     'yaxis','yaxis2','yaxis3','yaxis4','yaxis5']:
            if hasattr(fig.layout, axis):
                getattr(fig.layout, axis).update(separators=",.")
        for ann in fig.layout.annotations:
            ann.font.size = 10; ann.font.color = "#6b7280"

        st.plotly_chart(fig, use_container_width=True)

        # ── Targets row ──
        st.markdown("<div class='sec'>🎯 الأهداف السعرية</div>", unsafe_allow_html=True)
        tc = st.columns(4)
        for i, (name, tpx, clr) in enumerate(targets):
            pct = (tpx - px) / px * 100
            with tc[i]:
                st.markdown(f"""<div class="tgt-card">
                    <div style="color:#374151;font-size:11px;margin-bottom:3px">{name}</div>
                    <div style="color:{clr};font-size:20px;font-weight:700">{sym}{fmt(tpx)}</div>
                    <div style="color:{clr};font-size:12px">{pct:+.1f}%</div>
                    <div style="color:#374151;font-size:10px;margin-top:2px">R/R {rr_list[i] if i<3 else 0:.1f}x</div>
                </div>""", unsafe_allow_html=True)

# ── Landing ──
elif not analyze:
    st.markdown("""
    <div style="text-align:center;padding:80px 20px">
        <div style="font-size:64px;margin-bottom:20px">📊</div>
        <div style="color:#e2e8f0;font-size:22px;font-weight:700;margin-bottom:10px">ابحث عن أي سهم للبدء</div>
        <div style="color:#374151;font-size:14px;line-height:2.2">
            السوق السعودي: 2222.SR &nbsp;•&nbsp; 1120.SR &nbsp;•&nbsp; 2010.SR &nbsp;•&nbsp; 7010.SR<br>
            السوق الأمريكي: AAPL &nbsp;•&nbsp; TSLA &nbsp;•&nbsp; MSFT &nbsp;•&nbsp; NVDA &nbsp;•&nbsp; AMZN
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<hr style="border:1px solid #0d1422;margin-top:30px">
<p style="text-align:center;color:#1f2937;font-size:11px">
للأغراض التعليمية فقط • ليست توصية استثمارية • استشر مختص مالي قبل أي قرار
</p>""", unsafe_allow_html=True)
