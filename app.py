import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json, time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="منصة التحليل الفني المتقدم",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');
* { font-family: 'Tajawal', sans-serif !important; }
body, .stApp { background-color: #060b16 !important; color: #e2e8f0 !important; direction: rtl; }
.block-container { padding: 0.5rem 1rem 2rem; max-width: 1600px; }

/* Search bar */
.search-wrap {
    background: #0d1320;
    border: 1.5px solid #1e2d45;
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 24px;
    box-shadow: 0 4px 32px rgba(0,0,0,0.5);
}
.search-title {
    font-size: 42px; font-weight: 800;
    background: linear-gradient(90deg, #FFD700, #FFA500, #FF6B35);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin-bottom: 4px;
}
.search-sub { text-align:center; color:#4a5568; font-size:14px; margin-bottom:20px; }

/* Signal boxes */
.sig-enter-now   { background:#001a00; border:2.5px solid #00C851; border-radius:16px; padding:22px; text-align:center; }
.sig-ready-enter { background:#0a2010; border:2.5px solid #7FD68A; border-radius:16px; padding:22px; text-align:center; }
.sig-ready-exit  { background:#200808; border:2.5px solid #FF7070; border-radius:16px; padding:22px; text-align:center; }
.sig-exit-now    { background:#180000; border:2.5px solid #CC0000; border-radius:16px; padding:22px; text-align:center; }

/* Metric cards */
.m-card { background:#0d1320; border:1px solid #1e2d45; border-radius:12px; padding:14px 10px; text-align:center; margin-bottom:8px; }
.m-label { color:#4a5568; font-size:11px; margin-bottom:4px; }
.m-val { font-size:19px; font-weight:700; font-variant-numeric: tabular-nums; }
.c-green { color:#00C851 !important; }
.c-red   { color:#FF4444 !important; }
.c-gold  { color:#FFD700 !important; }
.c-gray  { color:#6b7280 !important; }
.c-blue  { color:#60A5FA !important; }
.c-orange{ color:#FB923C !important; }

/* Target cards */
.t-card { background:#0d1320; border:1px solid #1e2d45; border-radius:12px; padding:14px 10px; text-align:center; }

/* Section titles */
.sec-title {
    color:#FFD700; font-size:17px; font-weight:700;
    margin:22px 0 10px; padding-right:10px;
    border-right:4px solid #FFD700;
}

/* Notification badge */
.notif-badge {
    background:#1e2d45; border:1px solid #2d4060; border-radius:10px;
    padding:10px 14px; margin-bottom:6px; font-size:13px;
    display:flex; align-items:center; gap:10px;
}

/* Progress bar */
.prog-bg { background:#1e2d45; border-radius:99px; height:8px; margin-top:6px; overflow:hidden; }
.prog-fill { height:8px; border-radius:99px; transition:width 1s; }

/* Table rows */
.t-row {
    display:grid; grid-template-columns: 140px 110px 1fr 30px;
    padding:9px 12px; border-bottom:1px solid #0f1824;
    align-items:center; font-size:13px;
}
.t-row:hover { background:#0d1a2a; }

/* Score ring */
.score-ring { position:relative; display:inline-block; }

/* Alerts panel */
.alert-item {
    background:#0d1320; border-left:4px solid #FFD700;
    border-radius:8px; padding:10px 14px; margin-bottom:6px; font-size:13px;
}

/* Streamlit overrides */
.stButton>button {
    background:linear-gradient(90deg,#FFD700,#FFA500) !important;
    color:#000 !important; font-weight:700 !important;
    border:none !important; border-radius:12px !important;
    font-size:15px !important; padding:10px 20px !important;
}
.stTextInput>div>input {
    background:#0d1320 !important; border:1.5px solid #1e2d45 !important;
    color:#e2e8f0 !important; border-radius:10px !important;
    font-size:16px !important; font-family:'Tajawal' !important;
}
.stSelectbox>div>div {
    background:#0d1320 !important; border:1px solid #1e2d45 !important;
    color:#e2e8f0 !important;
}
div[data-testid="stSidebar"] { background:#06090f !important; border-right:1px solid #1e2d45; }
.stCheckbox label { color:#9ca3af !important; }
hr { border-color:#1e2d45 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Browser Notification JS ──────────────────────────────────────────────────
def inject_notification_js():
    st.components.v1.html("""
    <script>
    window.addEventListener('message', function(e) {
        if (e.data && e.data.type === 'STOCK_ALERT') {
            const d = e.data;
            if (Notification.permission === 'granted') {
                new Notification(d.title, {body: d.body, icon: d.icon || ''});
            } else if (Notification.permission !== 'denied') {
                Notification.requestPermission().then(p => {
                    if (p === 'granted')
                        new Notification(d.title, {body: d.body});
                });
            }
        }
        if (e.data && e.data.type === 'REQUEST_NOTIF') {
            Notification.requestPermission().then(p => {
                window.parent.postMessage({type:'NOTIF_RESULT', permission: p}, '*');
            });
        }
    });
    </script>
    """, height=0)

def send_browser_notification(title, body):
    escaped_title = title.replace("'", "\\'")
    escaped_body  = body.replace("'", "\\'")
    st.components.v1.html(f"""
    <script>
    (function() {{
        function tryNotify() {{
            if (typeof Notification !== 'undefined') {{
                if (Notification.permission === 'granted') {{
                    new Notification('{escaped_title}', {{body: '{escaped_body}'}});
                }} else if (Notification.permission !== 'denied') {{
                    Notification.requestPermission().then(p => {{
                        if (p === 'granted')
                            new Notification('{escaped_title}', {{body: '{escaped_body}'}});
                    }});
                }}
            }}
        }}
        tryNotify();
    }})();
    </script>
    """, height=0)

# ─── Helper: detect market & currency ────────────────────────────────────────
def detect_market(ticker: str):
    t = ticker.upper()
    if t.endswith(".SR"):
        return "SA", "SAR", "ر.س"
    elif t.endswith(".L"):
        return "UK", "GBP", "£"
    elif t.endswith(".PA") or t.endswith(".DE") or t.endswith(".MC"):
        return "EU", "EUR", "€"
    else:
        return "US", "USD", "$"

def fmt_price(val, sym):
    return f"{sym}{val:,.2f}"

def fmt_num_en(val, decimals=2):
    """Always return English numerals"""
    return f"{val:,.{decimals}f}"

# ─── Technical Indicators ─────────────────────────────────────────────────────

def rsi(s, n=14):
    d = s.diff(); g = d.clip(lower=0).rolling(n).mean(); l = (-d.clip(upper=0)).rolling(n).mean()
    return 100 - 100/(1+g/(l+1e-10))

def macd(s, f=12, sl=26, sig=9):
    ef = s.ewm(span=f,adjust=False).mean(); es = s.ewm(span=sl,adjust=False).mean()
    m = ef-es; sg = m.ewm(span=sig,adjust=False).mean()
    return m, sg, m-sg

def bb(s, n=20, k=2):
    m = s.rolling(n).mean(); sd = s.rolling(n).std()
    return m+k*sd, m, m-k*sd

def stoch(h,l,c,kp=14,dp=3):
    ll=l.rolling(kp).min(); hh=h.rolling(kp).max()
    k=100*(c-ll)/(hh-ll+1e-10); return k, k.rolling(dp).mean()

def atr(h,l,c,n=14):
    tr=pd.concat([(h-l),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    return tr.rolling(n).mean()

def adx(h,l,c,n=14):
    tr = pd.concat([(h-l),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    dmp = (h-h.shift()).clip(lower=0); dmm = (l.shift()-l).clip(lower=0)
    dmp = dmp.where(dmp>dmm, 0); dmm = dmm.where(dmm>dmp, 0)
    atr14 = tr.ewm(span=n,adjust=False).mean()
    dip = 100*(dmp.ewm(span=n,adjust=False).mean()/(atr14+1e-10))
    dim = 100*(dmm.ewm(span=n,adjust=False).mean()/(atr14+1e-10))
    dx  = 100*(dip-dim).abs()/(dip+dim+1e-10)
    return dx.ewm(span=n,adjust=False).mean(), dip, dim

def cci(h,l,c,n=20):
    tp=(h+l+c)/3; return (tp-tp.rolling(n).mean())/(0.015*tp.rolling(n).std()+1e-10)

def williams_r(h,l,c,n=14):
    hh=h.rolling(n).max(); ll=l.rolling(n).min()
    return -100*(hh-c)/(hh-ll+1e-10)

def mfi(h,l,c,vol,n=14):
    tp=(h+l+c)/3; mf=tp*vol
    pos=mf.where(tp>tp.shift(),0).rolling(n).sum()
    neg=mf.where(tp<tp.shift(),0).rolling(n).sum()
    return 100-100/(1+pos/(neg+1e-10))

def obv(c,vol):
    return (np.sign(c.diff())*vol).fillna(0).cumsum()

def vwap(h,l,c,vol):
    tp=(h+l+c)/3; return (tp*vol).cumsum()/(vol.cumsum()+1e-10)

def cmf(h,l,c,vol,n=20):
    mfv=((c-l)-(h-c))/(h-l+1e-10)*vol
    return mfv.rolling(n).sum()/(vol.rolling(n).sum()+1e-10)

def parabolic_sar(h,l,af_step=0.02,af_max=0.2):
    sar=np.zeros(len(h)); trend=np.ones(len(h))
    sar[0]=l.iloc[0]; ep=h.iloc[0]; af=af_step
    for i in range(1,len(h)):
        prev_sar=sar[i-1]
        if trend[i-1]==1:
            sar[i]=prev_sar+af*(ep-prev_sar)
            sar[i]=min(sar[i],l.iloc[max(0,i-1)],l.iloc[max(0,i-2)])
            if l.iloc[i]<sar[i]:
                trend[i]=-1; sar[i]=ep; ep=l.iloc[i]; af=af_step
            else:
                trend[i]=1
                if h.iloc[i]>ep: ep=h.iloc[i]; af=min(af+af_step,af_max)
        else:
            sar[i]=prev_sar+af*(ep-prev_sar)
            sar[i]=max(sar[i],h.iloc[max(0,i-1)],h.iloc[max(0,i-2)])
            if h.iloc[i]>sar[i]:
                trend[i]=1; sar[i]=ep; ep=h.iloc[i]; af=af_step
            else:
                trend[i]=-1
                if l.iloc[i]<ep: ep=l.iloc[i]; af=min(af+af_step,af_max)
    return pd.Series(sar, index=h.index), pd.Series(trend, index=h.index)

def pivot_points(h,l,c):
    p=(h+l+c)/3
    return {"P":p,"R1":2*p-l,"R2":p+(h-l),"R3":h+2*(p-l),
            "S1":2*p-h,"S2":p-(h-l),"S3":l-2*(h-p)}

def fibonacci_levels(h,l):
    diff=h-l
    return {
        "0%":h,"23.6%":h-0.236*diff,"38.2%":h-0.382*diff,
        "50%":h-0.5*diff,"61.8%":h-0.618*diff,"78.6%":h-0.786*diff,"100%":l
    }

def aroon(h,l,n=25):
    ai=(h.rolling(n+1).apply(lambda x:x.argmax())/n)*100
    ad=(l.rolling(n+1).apply(lambda x:x.argmin())/n)*100
    return ai,ad

def keltner(h,l,c,n=20,mult=2):
    mid=c.ewm(span=n,adjust=False).mean(); a=atr(h,l,c,n)
    return mid+mult*a, mid, mid-mult*a

def ultimate_oscillator(h,l,c,p1=7,p2=14,p3=28):
    bp=c-pd.concat([l,c.shift()],axis=1).min(axis=1)
    tr_=pd.concat([(h-l),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    avg1=bp.rolling(p1).sum()/(tr_.rolling(p1).sum()+1e-10)
    avg2=bp.rolling(p2).sum()/(tr_.rolling(p2).sum()+1e-10)
    avg3=bp.rolling(p3).sum()/(tr_.rolling(p3).sum()+1e-10)
    return 100*(4*avg1+2*avg2+avg3)/7

def volume_profile(close, volume, bins=20):
    mn,mx=close.min(),close.max()
    edges=np.linspace(mn,mx,bins+1)
    vols=[]
    for i in range(bins):
        mask=(close>=edges[i])&(close<edges[i+1])
        vols.append(volume[mask].sum())
    poc_idx=np.argmax(vols)
    return edges, np.array(vols), (edges[poc_idx]+edges[poc_idx+1])/2

# ─── Master Scoring ───────────────────────────────────────────────────────────
def master_score(rsi_v,macd_v,macd_sv,price,sma20,sma50,sma200,
                 stk,bb_u,bb_l,vol,avg_vol,adx_v,dip,dim,
                 cci_v,wr_v,mfi_v,cmf_v,sar_trend):
    sc=50
    # RSI (15pts)
    if 30<rsi_v<50: sc+=10
    elif 50<=rsi_v<65: sc+=15
    elif 65<=rsi_v<70: sc+=5
    elif rsi_v>=70: sc-=20
    elif rsi_v<=30: sc+=8
    # MACD (18pts)
    if macd_v>macd_sv: sc+=18
    else: sc-=18
    # MAs (20pts)
    if price>sma20: sc+=5
    if price>sma50: sc+=7
    if price>sma200: sc+=8
    # ADX (10pts)
    if adx_v>25:
        if dip>dim: sc+=10
        else: sc-=10
    # Stochastic (8pts)
    if stk<20: sc+=8
    elif stk>80: sc-=8
    elif stk<40: sc+=4
    # Bollinger (6pts)
    if price<bb_l: sc+=6
    elif price>bb_u: sc-=6
    # CCI (6pts)
    if cci_v<-100: sc+=6
    elif cci_v>100: sc-=6
    elif -50<cci_v<50: sc+=3
    # Williams %R (5pts)
    if wr_v<-80: sc+=5
    elif wr_v>-20: sc-=5
    # MFI (5pts)
    if mfi_v<20: sc+=5
    elif mfi_v>80: sc-=5
    # CMF (5pts)
    if cmf_v>0.1: sc+=5
    elif cmf_v<-0.1: sc-=5
    # Volume (5pts)
    if vol>avg_vol*1.8: sc+=5
    elif vol<avg_vol*0.4: sc-=3
    # Parabolic SAR (5pts)
    if sar_trend==1: sc+=5
    else: sc-=5
    return max(0,min(100,int(sc)))

def signal_info(score):
    if score>=65:
        return {"label":"دخول الآن","icon":"▲","cls":"sig-enter-now",
                "color":"#00C851","type":"buy","en":"BUY NOW"}
    elif score>=45:
        return {"label":"استعداد دخول","icon":"◆","cls":"sig-ready-enter",
                "color":"#7FD68A","type":"watch_buy","en":"READY TO BUY"}
    elif score>=28:
        return {"label":"استعداد خروج","icon":"◆","cls":"sig-ready-exit",
                "color":"#FF7070","type":"watch_sell","en":"READY TO SELL"}
    else:
        return {"label":"خروج الآن","icon":"▼","cls":"sig-exit-now",
                "color":"#CC0000","type":"sell","en":"SELL NOW"}

def calc_targets(price, atr_v, sig_type, sym):
    if sig_type in ("buy","watch_buy"):
        return [
            ("🎯 الهدف 1",  round(price+atr_v*1.5,2),  "#00C851"),
            ("🎯 الهدف 2",  round(price+atr_v*3.0,2),  "#00A040"),
            ("🎯 الهدف 3",  round(price+atr_v*5.0,2),  "#007030"),
            ("🛑 وقف الخسارة",round(price-atr_v*2.0,2),"#FF4444"),
        ]
    else:
        return [
            ("📉 هدف هبوط 1",round(price-atr_v*1.5,2),"#FF4444"),
            ("📉 هدف هبوط 2",round(price-atr_v*3.0,2),"#CC2222"),
            ("📉 هدف هبوط 3",round(price-atr_v*5.0,2),"#990000"),
            ("↩️ إعادة دخول",round(price-atr_v*5.5,2),"#FFD700"),
        ]

def interp(val, lo, hi, lo_lbl, hi_lbl, ok_lbl):
    if val<=lo: return lo_lbl,"#00C851"
    if val>=hi: return hi_lbl,"#FF4444"
    return ok_lbl,"#FFD700"

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#FFD700;text-align:center'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)

    period   = st.selectbox("📅 الفترة",   ["1mo","3mo","6mo","1y","2y"], index=2)
    interval = st.selectbox("⏱️ الإطار",   ["1d","1wk","1mo"], index=0,
                             format_func=lambda x:{"1d":"يومي","1wk":"أسبوعي","1mo":"شهري"}[x])
    st.markdown("---")
    st.markdown("<div style='color:#FFD700;font-weight:700;margin-bottom:8px'>📊 المؤشرات</div>", unsafe_allow_html=True)
    show_bb    = st.checkbox("بولينجر باند",    value=True)
    show_kc    = st.checkbox("Keltner Channel", value=True)
    show_sar   = st.checkbox("Parabolic SAR",   value=True)
    show_ema   = st.checkbox("EMA 9/20/50",     value=True)
    show_vwap  = st.checkbox("VWAP",            value=True)
    st.markdown("---")
    st.markdown("<div style='color:#FFD700;font-weight:700;margin-bottom:8px'>🔔 التنبيهات</div>", unsafe_allow_html=True)
    alert_rsi_hi = st.number_input("تنبيه RSI فوق", min_value=60, max_value=95, value=70, step=1)
    alert_rsi_lo = st.number_input("تنبيه RSI تحت", min_value=10, max_value=40, value=30, step=1)
    enable_notif = st.checkbox("تفعيل تنبيهات المتصفح", value=True)
    st.markdown("---")
    st.markdown("<p style='color:#374151;font-size:11px;text-align:center'>للأغراض التعليمية فقط. ليست توصية استثمارية.</p>", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
inject_notification_js()

st.markdown("""
<div class="search-wrap">
  <div class="search-title">📊 منصة التحليل الفني المتقدم</div>
  <div class="search-sub">RSI • MACD • Bollinger • Stochastic • ADX • CCI • Williams %R • MFI • VWAP • Parabolic SAR • Aroon • CMF • Fibonacci • Pivot Points</div>
</div>
""", unsafe_allow_html=True)

# ─── Search Bar ───────────────────────────────────────────────────────────────
col_inp, col_btn = st.columns([5,1])
with col_inp:
    ticker = st.text_input(
        "", placeholder="ابحث عن السهم — مثال: AAPL  •  2222.SR  •  TSLA  •  1120.SR  •  MSFT",
        label_visibility="collapsed"
    ).upper().strip()
with col_btn:
    analyze = st.button("🔍 تحليل", use_container_width=True)

# Quick picks
st.markdown("""
<div style="display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 20px;direction:rtl">
<span style="color:#4a5568;font-size:13px;padding-top:2px">أسهم سريعة:</span>
</div>
""", unsafe_allow_html=True)
qcols = st.columns(10)
quick = ["AAPL","MSFT","TSLA","NVDA","AMZN","2222.SR","1120.SR","2010.SR","7010.SR","1150.SR"]
for i, q in enumerate(quick):
    with qcols[i]:
        if st.button(q, key=f"q_{q}"):
            ticker = q
            analyze = True

# ─── MAIN ANALYSIS ────────────────────────────────────────────────────────────
if analyze and ticker:
    market, currency, sym = detect_market(ticker)

    with st.spinner(f"⏳ جاري تحليل {ticker} ..."):
        try:
            data = yf.download(ticker, period=period, interval=interval,
                               progress=False, auto_adjust=True)
            info = {}
            try:
                tk_obj = yf.Ticker(ticker)
                info   = tk_obj.info or {}
            except: pass
        except Exception as e:
            st.error(f"❌ خطأ: {e}"); st.stop()

    if data is None or data.empty or len(data) < 35:
        st.error("❌ بيانات غير كافية. تحقق من رمز السهم.")
        st.info("💡 السوق السعودي: أضف .SR مثل 2222.SR • السوق الأمريكي: AAPL, TSLA, MSFT")
        st.stop()

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    C = data["Close"].astype(float)
    H = data["High"].astype(float)
    L = data["Low"].astype(float)
    V = data["Volume"].astype(float)
    O = data["Open"].astype(float)

    # ── Compute all indicators ──
    rsi_s               = rsi(C)
    macd_line,sig_line,hist_line = macd(C)
    ema9_s              = C.ewm(span=9,adjust=False).mean()
    ema20_s             = C.ewm(span=20,adjust=False).mean()
    ema50_s             = C.ewm(span=50,adjust=False).mean()
    sma200_s            = C.rolling(200).mean()
    bb_u,bb_m,bb_l      = bb(C)
    kc_u,kc_m,kc_l      = keltner(H,L,C)
    stk_s,std_s         = stoch(H,L,C)
    atr_s               = atr(H,L,C)
    adx_s,dip_s,dim_s   = adx(H,L,C)
    cci_s               = cci(H,L,C)
    wr_s                = williams_r(H,L,C)
    mfi_s               = mfi(H,L,C,V)
    obv_s               = obv(C,V)
    vwap_s              = vwap(H,L,C,V)
    cmf_s               = cmf(H,L,C,V)
    uo_s                = ultimate_oscillator(H,L,C)
    sar_s, trend_s      = parabolic_sar(H,L)
    aroon_up,aroon_dn   = aroon(H,L)
    vol_ma20            = V.rolling(20).mean()

    def last(s): return float(s.dropna().iloc[-1]) if len(s.dropna()) else 0.0

    px       = last(C)
    rsi_v    = last(rsi_s)
    macd_v   = last(macd_line)
    macd_sv  = last(sig_line)
    ema9_v   = last(ema9_s)
    ema20_v  = last(ema20_s)
    ema50_v  = last(ema50_s)
    sma200_v = last(sma200_s)
    bbu_v    = last(bb_u); bbm_v=last(bb_m); bbl_v=last(bb_l)
    kcu_v    = last(kc_u); kcl_v=last(kc_l)
    stk_v    = last(stk_s); std_v=last(std_s)
    atr_v    = last(atr_s)
    adx_v    = last(adx_s); dip_v=last(dip_s); dim_v=last(dim_s)
    cci_v    = last(cci_s)
    wr_v     = last(wr_s)
    mfi_v    = last(mfi_s)
    obv_v    = last(obv_s)
    vwap_v   = last(vwap_s)
    cmf_v    = last(cmf_s)
    uo_v     = last(uo_s)
    sar_v    = float(sar_s.iloc[-1])
    sar_tr   = float(trend_s.iloc[-1])
    aroon_u  = last(aroon_up); aroon_d=last(aroon_dn)
    vol_v    = float(V.iloc[-1]); vol_avg=last(vol_ma20)
    prev_px  = float(C.iloc[-2]) if len(C)>1 else px
    chg_pct  = (px-prev_px)/prev_px*100

    # Pivot & Fibonacci
    piv = pivot_points(last(H.rolling(1).max()), last(L.rolling(1).min()), px)
    fib_h = float(C.tail(50).max()); fib_l = float(C.tail(50).min())
    fibs = fibonacci_levels(fib_h, fib_l)

    # Volume profile
    vp_edges, vp_vols, poc = volume_profile(C, V)

    # Score & signal
    score = master_score(rsi_v,macd_v,macd_sv,px,ema20_v,ema50_v,sma200_v,
                          stk_v,bbu_v,bbl_v,vol_v,vol_avg,adx_v,dip_v,dim_v,
                          cci_v,wr_v,mfi_v,cmf_v,sar_tr)
    sig   = signal_info(score)
    targets = calc_targets(px, atr_v, sig["type"], sym)

    company_name = info.get("longName", ticker) or ticker

    # ── Push Notification ──
    if enable_notif:
        notif_body = f"{sig['en']} | Score: {score}/100 | Price: {sym}{px:.2f} | RSI: {rsi_v:.1f}"
        send_browser_notification(f"📊 {ticker} - {sig['en']}", notif_body)

    # ── Check RSI alerts ──
    rsi_alerts = []
    if rsi_v >= alert_rsi_hi:
        rsi_alerts.append(f"⚠️ RSI = {rsi_v:.1f} — فوق مستوى ذروة الشراء ({alert_rsi_hi})")
        if enable_notif:
            send_browser_notification(f"🔴 {ticker} RSI Alert", f"RSI = {rsi_v:.1f} — ذروة شراء!")
    if rsi_v <= alert_rsi_lo:
        rsi_alerts.append(f"💡 RSI = {rsi_v:.1f} — تحت مستوى ذروة البيع ({alert_rsi_lo}) — فرصة محتملة")
        if enable_notif:
            send_browser_notification(f"🟢 {ticker} RSI Alert", f"RSI = {rsi_v:.1f} — ذروة بيع — فرصة!")

    # ═══════════════════════════════════════════════
    # SIGNAL BOX
    # ═══════════════════════════════════════════════
    st.markdown(f"<div style='color:#4a5568;font-size:14px;margin-bottom:8px'>📍 {company_name} &nbsp;|&nbsp; {market} &nbsp;|&nbsp; {currency}</div>", unsafe_allow_html=True)

    sc1,sc2,sc3 = st.columns([1,2,1])
    with sc2:
        bar_color = sig["color"]
        st.markdown(f"""
        <div class="{sig['cls']}">
            <div style="color:{sig['color']};font-size:40px;font-weight:800;line-height:1.1">
                {sig['icon']} {sig['label']}
            </div>
            <div style="color:{sig['color']};font-size:13px;margin-top:8px;opacity:0.8">{sig['en']}</div>
            <div style="color:{sig['color']};font-size:16px;margin-top:10px;font-weight:600">
                قوة الإشارة: {score} / 100
            </div>
            <div class="prog-bg">
                <div class="prog-fill" style="width:{score}%;background:{bar_color}"></div>
            </div>
            <div style="color:#4a5568;font-size:12px;margin-top:8px">{datetime.now().strftime('%Y-%m-%d  %H:%M')}</div>
        </div>
        """, unsafe_allow_html=True)

    # RSI alerts
    for a in rsi_alerts:
        st.warning(a)

    # ═══════════════════════════════════════════════
    # KEY METRICS ROW
    # ═══════════════════════════════════════════════
    st.markdown("<div class='sec-title'>📌 المؤشرات الرئيسية</div>", unsafe_allow_html=True)
    mc = st.columns(8)
    mets = [
        ("السعر", f"{sym}{fmt_num_en(px)}", "gold"),
        ("التغيير %", f"{chg_pct:+.2f}%", "green" if chg_pct>=0 else "red"),
        ("RSI(14)", fmt_num_en(rsi_v,1), "red" if rsi_v>70 else "green" if rsi_v<30 else "gray"),
        ("MACD", fmt_num_en(macd_v,4), "green" if macd_v>macd_sv else "red"),
        ("ADX", fmt_num_en(adx_v,1), "blue" if adx_v>25 else "gray"),
        ("ATR", fmt_num_en(atr_v,2), "orange"),
        ("Volume", f"{vol_v/1e6:.1f}M" if vol_v>1e6 else fmt_num_en(vol_v,0), "blue" if vol_v>vol_avg else "gray"),
        ("MFI(14)", fmt_num_en(mfi_v,1), "red" if mfi_v>80 else "green" if mfi_v<20 else "gray"),
    ]
    for i,(lbl,val,clr) in enumerate(mets):
        with mc[i]:
            st.markdown(f"""<div class="m-card">
                <div class="m-label">{lbl}</div>
                <div class="m-val c-{clr}">{val}</div>
            </div>""", unsafe_allow_html=True)

    mc2 = st.columns(8)
    mets2 = [
        ("EMA 9",   fmt_num_en(ema9_v),   "green" if px>ema9_v  else "red"),
        ("EMA 20",  fmt_num_en(ema20_v),  "green" if px>ema20_v else "red"),
        ("EMA 50",  fmt_num_en(ema50_v),  "green" if px>ema50_v else "red"),
        ("SMA 200", fmt_num_en(sma200_v), "green" if px>sma200_v else "red"),
        ("BB Upper",fmt_num_en(bbu_v),    "red"),
        ("BB Lower",fmt_num_en(bbl_v),    "green"),
        ("VWAP",    fmt_num_en(vwap_v),   "green" if px>vwap_v else "red"),
        ("SAR",     fmt_num_en(sar_v),    "green" if sar_tr==1 else "red"),
    ]
    for i,(lbl,val,clr) in enumerate(mets2):
        with mc2[i]:
            st.markdown(f"""<div class="m-card">
                <div class="m-label">{lbl}</div>
                <div class="m-val c-{clr}">{val}</div>
            </div>""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════
    # TARGETS + FIBONACCI + PIVOT POINTS
    # ═══════════════════════════════════════════════
    t_col, f_col, p_col = st.columns([2,1.5,1.5])

    with t_col:
        st.markdown("<div class='sec-title'>🎯 الأهداف السعرية (ATR-Based)</div>", unsafe_allow_html=True)
        tc = st.columns(4)
        for i,(name,tpx,clr) in enumerate(targets):
            pct=(tpx-px)/px*100
            with tc[i]:
                st.markdown(f"""<div class="t-card">
                    <div style="color:#4a5568;font-size:11px;margin-bottom:4px">{name}</div>
                    <div style="color:{clr};font-size:18px;font-weight:700">{sym}{fmt_num_en(tpx)}</div>
                    <div style="color:{clr};font-size:12px">({pct:+.1f}%)</div>
                </div>""", unsafe_allow_html=True)

    with f_col:
        st.markdown("<div class='sec-title'>📐 مستويات فيبوناتشي</div>", unsafe_allow_html=True)
        for lbl,val in list(fibs.items())[:5]:
            clr = "#00C851" if val<px else "#FF4444"
            diff_pct = (val-px)/px*100
            st.markdown(f"""<div style="display:flex;justify-content:space-between;
                padding:6px 10px;background:#0d1320;border-radius:6px;margin-bottom:4px;font-size:13px">
                <span style="color:#6b7280">{lbl}</span>
                <span style="color:{clr}">{sym}{fmt_num_en(val)} ({diff_pct:+.1f}%)</span>
            </div>""", unsafe_allow_html=True)

    with p_col:
        st.markdown("<div class='sec-title'>📍 نقاط المحور (Pivot)</div>", unsafe_allow_html=True)
        piv_display = [("R2","#FF4444"),("R1","#FF8800"),("P","#FFD700"),("S1","#00C851"),("S2","#007030")]
        for k,clr in piv_display:
            v = float(piv[k].iloc[-1]) if hasattr(piv[k],'iloc') else float(piv[k])
            diff_pct = (v-px)/px*100
            st.markdown(f"""<div style="display:flex;justify-content:space-between;
                padding:6px 10px;background:#0d1320;border-radius:6px;margin-bottom:4px;font-size:13px">
                <span style="color:{clr};font-weight:600">{k}</span>
                <span style="color:{clr}">{sym}{fmt_num_en(v)} ({diff_pct:+.1f}%)</span>
            </div>""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════
    # MAIN CHART
    # ═══════════════════════════════════════════════
    st.markdown("<div class='sec-title'>📈 الرسم البياني المتكامل</div>", unsafe_allow_html=True)

    fig = make_subplots(
        rows=5, cols=1, shared_xaxes=True,
        vertical_spacing=0.025,
        row_heights=[0.44,0.16,0.14,0.13,0.13],
        subplot_titles=("", "MACD", "RSI (14)", "Stochastic (14,3,3)", "CCI / Williams %R")
    )

    # Candles
    fig.add_trace(go.Candlestick(x=data.index,open=O,high=H,low=L,close=C,name="Price",
        increasing=dict(fillcolor="#00C851",line=dict(color="#00C851",width=0.8)),
        decreasing=dict(fillcolor="#FF4444",line=dict(color="#FF4444",width=0.8))),row=1,col=1)

    # EMAs
    if show_ema:
        fig.add_trace(go.Scatter(x=data.index,y=ema9_s, name="EMA 9",  line=dict(color="#FF9800",width=1.2)),row=1,col=1)
        fig.add_trace(go.Scatter(x=data.index,y=ema20_s,name="EMA 20", line=dict(color="#2196F3",width=1.5)),row=1,col=1)
        fig.add_trace(go.Scatter(x=data.index,y=ema50_s,name="EMA 50", line=dict(color="#9C27B0",width=1.8)),row=1,col=1)
    fig.add_trace(go.Scatter(x=data.index,y=sma200_s,name="SMA 200",line=dict(color="#F44336",width=2.2,dash="dot")),row=1,col=1)

    # Bollinger
    if show_bb:
        fig.add_trace(go.Scatter(x=data.index,y=bb_u,name="BB Upper",line=dict(color="#607D8B",width=1,dash="dash")),row=1,col=1)
        fig.add_trace(go.Scatter(x=data.index,y=bb_l,name="BB Lower",line=dict(color="#607D8B",width=1,dash="dash"),
                                  fill="tonexty",fillcolor="rgba(96,125,139,0.06)"),row=1,col=1)

    # Keltner
    if show_kc:
        fig.add_trace(go.Scatter(x=data.index,y=kc_u,name="KC Upper",line=dict(color="#795548",width=1,dash="dot")),row=1,col=1)
        fig.add_trace(go.Scatter(x=data.index,y=kc_l,name="KC Lower",line=dict(color="#795548",width=1,dash="dot")),row=1,col=1)

    # VWAP
    if show_vwap:
        fig.add_trace(go.Scatter(x=data.index,y=vwap_s,name="VWAP",line=dict(color="#00BCD4",width=1.8,dash="dashdot")),row=1,col=1)

    # Parabolic SAR
    if show_sar:
        sar_clr = ["#00C851" if t==1 else "#FF4444" for t in trend_s]
        fig.add_trace(go.Scatter(x=data.index,y=sar_s,name="SAR",mode="markers",
                                  marker=dict(symbol="circle",size=3,color=sar_clr)),row=1,col=1)

    # MACD
    h_col = ["#00C851" if v>=0 else "#FF4444" for v in hist_line]
    fig.add_trace(go.Bar(x=data.index,y=hist_line,name="Histogram",marker_color=h_col,opacity=0.7),row=2,col=1)
    fig.add_trace(go.Scatter(x=data.index,y=macd_line,name="MACD",line=dict(color="#FF9800",width=1.5)),row=2,col=1)
    fig.add_trace(go.Scatter(x=data.index,y=sig_line, name="Signal",line=dict(color="#2196F3",width=1.5)),row=2,col=1)
    fig.add_hline(y=0,line=dict(color="#333",width=0.8),row=2,col=1)

    # RSI
    fig.add_trace(go.Scatter(x=data.index,y=rsi_s,name="RSI",line=dict(color="#E91E63",width=1.8)),row=3,col=1)
    fig.add_hrect(y0=70,y1=100,fillcolor="rgba(255,68,68,0.06)",line_width=0,row=3,col=1)
    fig.add_hrect(y0=0, y1=30, fillcolor="rgba(0,200,81,0.06)", line_width=0,row=3,col=1)
    for y,clr in [(70,"#FF4444"),(50,"#444"),(30,"#00C851")]:
        fig.add_hline(y=y,line=dict(color=clr,width=0.8,dash="dot"),row=3,col=1)

    # Stochastic
    fig.add_trace(go.Scatter(x=data.index,y=stk_s,name="%K",line=dict(color="#00BCD4",width=1.5)),row=4,col=1)
    fig.add_trace(go.Scatter(x=data.index,y=std_s,name="%D",line=dict(color="#FF5722",width=1.5)),row=4,col=1)
    fig.add_hrect(y0=80,y1=100,fillcolor="rgba(255,68,68,0.06)",line_width=0,row=4,col=1)
    fig.add_hrect(y0=0, y1=20, fillcolor="rgba(0,200,81,0.06)", line_width=0,row=4,col=1)
    for y,clr in [(80,"#FF4444"),(20,"#00C851")]:
        fig.add_hline(y=y,line=dict(color=clr,width=0.8,dash="dot"),row=4,col=1)

    # CCI
    cci_clr = ["#FF4444" if v>100 else "#00C851" if v<-100 else "#607D8B" for v in cci_s.fillna(0)]
    fig.add_trace(go.Bar(x=data.index,y=cci_s,name="CCI",marker_color=cci_clr,opacity=0.7),row=5,col=1)
    for y,clr in [(100,"#FF4444"),(-100,"#00C851")]:
        fig.add_hline(y=y,line=dict(color=clr,width=0.8,dash="dot"),row=5,col=1)

    fig.update_layout(
        template="plotly_dark", height=900,
        showlegend=True,
        legend=dict(orientation="h",x=0,y=1.01,font=dict(size=10),bgcolor="rgba(0,0,0,0)"),
        xaxis_rangeslider_visible=False,
        plot_bgcolor="#060b16", paper_bgcolor="#060b16",
        font=dict(family="Tajawal,sans-serif",color="#9ca3af",size=11),
        margin=dict(l=6,r=6,t=28,b=6),
    )
    for ann in fig.layout.annotations:
        ann.font.size=11; ann.font.color="#6b7280"

    st.plotly_chart(fig, use_container_width=True)

    # ═══════════════════════════════════════════════
    # VOLUME ANALYSIS
    # ═══════════════════════════════════════════════
    st.markdown("<div class='sec-title'>📊 تحليل حجم التداول</div>", unsafe_allow_html=True)
    vc1,vc2,vc3,vc4 = st.columns(4)

    vol_ratio = vol_v/(vol_avg+1e-10)
    vol_signal = "تأكيد قوي 🔥" if vol_ratio>2 else "أعلى المتوسط ✅" if vol_ratio>1 else "أقل المتوسط ⚠️"
    vol_clr    = "#FF9800" if vol_ratio>2 else "#00C851" if vol_ratio>1 else "#FF4444"

    obv_trend = "صاعد ✅" if obv_s.iloc[-1]>obv_s.iloc[-5] else "هابط ❌"
    cmf_interp= "تدفق شراء ✅" if cmf_v>0.1 else "تدفق بيع ❌" if cmf_v<-0.1 else "محايد"

    with vc1:
        st.markdown(f"""<div class="m-card">
            <div class="m-label">حجم اليوم</div>
            <div class="m-val" style="color:{vol_clr}">{vol_v/1e6:.2f}M</div>
            <div style="color:{vol_clr};font-size:11px">{vol_signal}</div>
        </div>""", unsafe_allow_html=True)
    with vc2:
        st.markdown(f"""<div class="m-card">
            <div class="m-label">نسبة الحجم</div>
            <div class="m-val" style="color:{vol_clr}">{vol_ratio:.2f}x</div>
            <div style="color:#4a5568;font-size:11px">متوسط: {vol_avg/1e6:.2f}M</div>
        </div>""", unsafe_allow_html=True)
    with vc3:
        st.markdown(f"""<div class="m-card">
            <div class="m-label">OBV اتجاه</div>
            <div class="m-val c-{'green' if 'صاعد' in obv_trend else 'red'}">{obv_trend}</div>
            <div style="color:#4a5568;font-size:11px">{obv_s.iloc[-1]/1e6:.1f}M</div>
        </div>""", unsafe_allow_html=True)
    with vc4:
        st.markdown(f"""<div class="m-card">
            <div class="m-label">CMF (20)</div>
            <div class="m-val" style="color:{'#00C851' if cmf_v>0 else '#FF4444'}">{cmf_v:.3f}</div>
            <div style="color:#4a5568;font-size:11px">{cmf_interp}</div>
        </div>""", unsafe_allow_html=True)

    # Volume bar chart + OBV
    vfig = make_subplots(rows=1,cols=2,subplot_titles=("حجم التداول","OBV"))
    vcolors = ["#00C851" if C.iloc[i]>=O.iloc[i] else "#FF4444" for i in range(len(C))]
    vfig.add_trace(go.Bar(x=data.index,y=V,marker_color=vcolors,name="Volume",opacity=0.8),row=1,col=1)
    vfig.add_trace(go.Scatter(x=data.index,y=vol_ma20,name="Vol MA20",line=dict(color="#FFD700",width=1.5)),row=1,col=1)
    vfig.add_trace(go.Scatter(x=data.index,y=obv_s,name="OBV",line=dict(color="#00BCD4",width=1.5),fill="tozeroy",fillcolor="rgba(0,188,212,0.08)"),row=1,col=2)
    vfig.update_layout(template="plotly_dark",height=200,showlegend=False,
                       plot_bgcolor="#060b16",paper_bgcolor="#060b16",
                       margin=dict(l=6,r=6,t=28,b=6),font=dict(family="Tajawal",size=10,color="#6b7280"))
    for ann in vfig.layout.annotations: ann.font.size=10; ann.font.color="#6b7280"
    st.plotly_chart(vfig, use_container_width=True)

    # ═══════════════════════════════════════════════
    # FULL INDICATORS TABLE
    # ═══════════════════════════════════════════════
    st.markdown("<div class='sec-title'>📋 جدول التحليل الفني الشامل</div>", unsafe_allow_html=True)

    def ind_row(name, val_str, interp_str, icon, color):
        st.markdown(f"""
        <div class="t-row">
            <span style="color:#d1d5db;font-weight:500">{name}</span>
            <span style="color:#FFD700;font-family:monospace">{val_str}</span>
            <span style="color:{color}">{interp_str}</span>
            <span style="font-size:16px">{icon}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="t-row" style="background:#0a1020;border-radius:8px 8px 0 0">
        <span style="color:#4a5568;font-size:11px">المؤشر</span>
        <span style="color:#4a5568;font-size:11px">القيمة</span>
        <span style="color:#4a5568;font-size:11px">التفسير</span>
        <span></span>
    </div>""", unsafe_allow_html=True)

    rows_data = [
        ("RSI (14)", fmt_num_en(rsi_v,1),
         "ذروة شراء — احتمال تصحيح" if rsi_v>70 else "ذروة بيع — فرصة شراء" if rsi_v<30 else "قوي صعودي" if rsi_v>55 else "ضعيف هبوطي" if rsi_v<45 else "محايد",
         "🔴" if rsi_v>70 else "🟢" if rsi_v<30 else "🟢" if rsi_v>55 else "🔴" if rsi_v<45 else "⚪"),
        ("MACD vs Signal", f"{fmt_num_en(macd_v,4)} / {fmt_num_en(macd_sv,4)}",
         "تقاطع صعودي — إشارة شراء قوية" if macd_v>macd_sv else "تقاطع هبوطي — إشارة بيع",
         "🟢" if macd_v>macd_sv else "🔴"),
        ("ADX (14)", fmt_num_en(adx_v,1),
         f"اتجاه {'قوي' if adx_v>25 else 'ضعيف'} — DI+ {'>' if dip_v>dim_v else '<'} DI- ({'صعودي' if dip_v>dim_v else 'هبوطي'})",
         "🟢" if (adx_v>25 and dip_v>dim_v) else "🔴" if (adx_v>25 and dim_v>dip_v) else "⚪"),
        ("Stochastic %K", fmt_num_en(stk_v,1),
         "ذروة شراء" if stk_v>80 else "ذروة بيع — فرصة" if stk_v<20 else "منطقة محايدة",
         "🔴" if stk_v>80 else "🟢" if stk_v<20 else "⚪"),
        ("CCI (20)", fmt_num_en(cci_v,1),
         "ذروة شراء > +100" if cci_v>100 else "ذروة بيع < -100 — فرصة" if cci_v<-100 else "داخل النطاق الطبيعي",
         "🔴" if cci_v>100 else "🟢" if cci_v<-100 else "⚪"),
        ("Williams %R", fmt_num_en(wr_v,1),
         "ذروة بيع (< -80) — فرصة محتملة" if wr_v<-80 else "ذروة شراء (> -20)" if wr_v>-20 else "منطقة محايدة",
         "🟢" if wr_v<-80 else "🔴" if wr_v>-20 else "⚪"),
        ("MFI (14)", fmt_num_en(mfi_v,1),
         "ذروة شراء بالحجم" if mfi_v>80 else "ذروة بيع — ضغط مرتفع" if mfi_v<20 else "تدفق أموال طبيعي",
         "🔴" if mfi_v>80 else "🟢" if mfi_v<20 else "⚪"),
        ("Ultimate Osc.", fmt_num_en(uo_v,1),
         "ذروة شراء" if uo_v>70 else "ذروة بيع — فرصة" if uo_v<30 else "محايد",
         "🔴" if uo_v>70 else "🟢" if uo_v<30 else "⚪"),
        ("Parabolic SAR", fmt_num_en(sar_v,2),
         "السعر فوق SAR — اتجاه صاعد ✅" if sar_tr==1 else "السعر تحت SAR — اتجاه هابط ❌",
         "🟢" if sar_tr==1 else "🔴"),
        ("Aroon Up/Down", f"{fmt_num_en(aroon_u,0)} / {fmt_num_en(aroon_d,0)}",
         "Aroon Up مرتفع — زخم صعودي" if aroon_u>70 else "Aroon Down مرتفع — زخم هبوطي" if aroon_d>70 else "محايد",
         "🟢" if aroon_u>aroon_d else "🔴"),
        ("Bollinger %B", f"{fmt_num_en((px-bbl_v)/(bbu_v-bbl_v+1e-10)*100,0)}%",
         "خروج فوق النطاق العلوي" if px>bbu_v else "خروج تحت النطاق السفلي — فرصة" if px<bbl_v else "داخل النطاق",
         "🔴" if px>bbu_v else "🟢" if px<bbl_v else "⚪"),
        ("CMF (20)", fmt_num_en(cmf_v,3),
         "تدفق شراء قوي ✅" if cmf_v>0.1 else "تدفق بيع ❌" if cmf_v<-0.1 else "محايد",
         "🟢" if cmf_v>0.1 else "🔴" if cmf_v<-0.1 else "⚪"),
        ("SMA 50 vs 200", f"{fmt_num_en(ema50_v,2)} / {fmt_num_en(sma200_v,2)}",
         "Golden Cross ✅ — اتجاه صاعد قوي" if ema50_v>sma200_v else "Death Cross ❌ — اتجاه هابط",
         "🟢" if ema50_v>sma200_v else "🔴"),
        ("VWAP", fmt_num_en(vwap_v,2),
         f"السعر {'فوق' if px>vwap_v else 'تحت'} VWAP — {'قوة شراء' if px>vwap_v else 'ضغط بيع'}",
         "🟢" if px>vwap_v else "🔴"),
        ("POC (Volume)", f"{sym}{fmt_num_en(poc,2)}",
         f"أعلى تركيز حجم — {'دعم' if poc<px else 'مقاومة'}",
         "🟢" if poc<px else "🔴"),
        ("حجم التداول", f"{vol_v/1e6:.2f}M",
         f"{'أعلى المتوسط بـ' if vol_ratio>1 else 'أقل المتوسط بـ'} {abs(vol_ratio-1)*100:.0f}%",
         "🟢" if vol_ratio>1.2 else "🔴" if vol_ratio<0.5 else "⚪"),
    ]

    color_map = {"🟢":"#00C851","🔴":"#FF4444","🟡":"#FFD700","⚪":"#6b7280"}
    for name,val,interp_str,icon in rows_data:
        ind_row(name, val, interp_str, icon, color_map.get(icon,"#9ca3af"))

    # ═══════════════════════════════════════════════
    # SIGNAL LEGEND + NOTIFICATIONS GUIDE
    # ═══════════════════════════════════════════════
    st.markdown("<div class='sec-title'>🗺️ دليل الإشارات والتنبيهات</div>", unsafe_allow_html=True)
    lc = st.columns(4)
    leg = [
        ("دخول الآن ▲",    "#001a00","#00C851","≥ 65 نقطة — كل المؤشرات صاعدة","BUY NOW"),
        ("استعداد دخول ◆", "#0a2010","#7FD68A","45–64 — بداية إشارات صعودية","READY TO BUY"),
        ("استعداد خروج ◆", "#200808","#FF7070","28–44 — بداية إشارات هبوطية","READY TO SELL"),
        ("خروج الآن ▼",    "#180000","#CC0000","< 28 — إشارات هبوط قوية","SELL NOW"),
    ]
    for i,(lbl,bg,clr,desc,en) in enumerate(leg):
        with lc[i]:
            st.markdown(f"""<div style="background:{bg};border:2px solid {clr};border-radius:12px;
                padding:14px;text-align:center">
                <div style="color:{clr};font-size:16px;font-weight:700">{lbl}</div>
                <div style="color:#6b7280;font-size:10px;margin-top:2px">{en}</div>
                <div style="color:{clr};font-size:11px;margin-top:8px;opacity:0.8">{desc}</div>
            </div>""", unsafe_allow_html=True)

    # Notifications panel
    st.markdown("<div class='sec-title'>🔔 التنبيهات النشطة</div>", unsafe_allow_html=True)
    notif_items = [
        (f"📊 تحليل {ticker} — {sig['label']} | نقاط: {score}/100 | السعر: {sym}{fmt_num_en(px)}", sig["color"]),
        (f"📐 RSI = {fmt_num_en(rsi_v,1)} | {'⚠️ ذروة شراء' if rsi_v>70 else '💡 ذروة بيع' if rsi_v<30 else '✅ مستوى طبيعي'}", "#FFD700"),
        (f"📈 MACD {'صاعد ✅' if macd_v>macd_sv else 'هابط ❌'} | ADX = {fmt_num_en(adx_v,1)} ({'قوي' if adx_v>25 else 'ضعيف'})", "#60A5FA"),
        (f"💹 الحجم = {vol_ratio:.2f}x المتوسط | OBV {'صاعد ✅' if obv_trend.startswith('صاعد') else 'هابط ❌'} | CMF = {fmt_num_en(cmf_v,3)}", "#9CA3AF"),
        (f"🎯 هدف 1: {sym}{fmt_num_en(targets[0][1])} ({(targets[0][1]-px)/px*100:+.1f}%) | هدف 2: {sym}{fmt_num_en(targets[1][1])} | وقف: {sym}{fmt_num_en(targets[3][1])}", "#00C851" if sig["type"] in ("buy","watch_buy") else "#FF4444"),
    ]
    for txt,clr in notif_items:
        st.markdown(f"""<div class="alert-item" style="border-left-color:{clr}">
            <span style="color:{clr}">{txt}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("""<div style="background:#0d1320;border:1px solid #1e2d45;border-radius:10px;padding:14px 18px;margin-top:10px">
        <div style="color:#FFD700;font-size:14px;font-weight:600;margin-bottom:8px">📱 تفعيل التنبيهات على الجوال والكمبيوتر</div>
        <div style="color:#6b7280;font-size:13px;line-height:1.8">
        ✅ اضغط <b style="color:#e2e8f0">السماح</b> عند ظهور طلب التنبيهات في المتصفح<br>
        ✅ يعمل على <b style="color:#e2e8f0">Chrome / Safari / Edge</b> على الجوال والكمبيوتر<br>
        ✅ على الآيفون: افتح الموقع في Safari ← اضغط Share ← <b style="color:#e2e8f0">Add to Home Screen</b> لتنبيهات أفضل<br>
        ✅ يمكن إعداد تنبيهات RSI مخصصة من الشريط الجانبي
        </div>
    </div>""", unsafe_allow_html=True)

    # Download
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        "📥 تحميل بيانات التحليل (CSV)",
        data.to_csv().encode("utf-8"),
        file_name=f"{ticker}_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv", use_container_width=True
    )

else:
    # ─── Landing / empty state ──
    st.markdown("""
    <div style="text-align:center;padding:60px 20px">
        <div style="font-size:72px;margin-bottom:20px">📊</div>
        <div style="color:#d1d5db;font-size:24px;font-weight:600;margin-bottom:12px">ابحث عن أي سهم للبدء</div>
        <div style="color:#4a5568;font-size:15px;line-height:2">
            السوق الأمريكي: AAPL • MSFT • TSLA • NVDA • AMZN<br>
            السوق السعودي: 2222.SR (أرامكو) • 1120.SR (الراجحي) • 2010.SR (سابك)<br><br>
            <span style="color:#FFD700">15+ مؤشر فني عالمي</span> &nbsp;•&nbsp; 
            <span style="color:#00C851">أهداف سعرية ذكية</span> &nbsp;•&nbsp; 
            <span style="color:#60A5FA">تنبيهات فورية</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<hr>
<p style="text-align:center;color:#1f2937;font-size:11px;padding:8px">
📊 منصة التحليل الفني المتقدم &nbsp;|&nbsp; للأغراض التعليمية فقط &nbsp;|&nbsp; ليست توصية استثمارية
</p>""", unsafe_allow_html=True)
