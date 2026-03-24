import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="منصة التحليل الفني",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');

* { font-family: 'Tajawal', sans-serif !important; font-variant-numeric: tabular-nums; }
body, .stApp { background: #F5F6FA !important; color: #1a1a2e !important; direction: rtl; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* TOP NAV */
.top-nav {
    background: #fff;
    border-bottom: 1px solid #E8EAF0;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 56px;
    position: sticky;
    top: 0;
    z-index: 100;
}
.nav-logo { font-size: 20px; font-weight: 800; color: #1a1a2e; }
.nav-logo span { color: #2563EB; }

/* SEARCH BAR */
.search-section {
    background: #fff;
    padding: 16px 24px;
    border-bottom: 1px solid #E8EAF0;
}

/* SIGNAL BADGE */
.badge-buy-now    { background:#DCFCE7; color:#15803D; border:1.5px solid #86EFAC; border-radius:8px; padding:6px 16px; font-size:13px; font-weight:700; display:inline-block; }
.badge-ready-buy  { background:#D1FAE5; color:#059669; border:1.5px solid #6EE7B7; border-radius:8px; padding:6px 16px; font-size:13px; font-weight:700; display:inline-block; }
.badge-ready-sell { background:#FEF9C3; color:#B45309; border:1.5px solid #FDE68A; border-radius:8px; padding:6px 16px; font-size:13px; font-weight:700; display:inline-block; }
.badge-sell-now   { background:#FEE2E2; color:#DC2626; border:1.5px solid #FCA5A5; border-radius:8px; padding:6px 16px; font-size:13px; font-weight:700; display:inline-block; }

/* STOCK HEADER */
.stock-header {
    background: #fff;
    padding: 20px 24px 16px;
    border-bottom: 1px solid #E8EAF0;
}
.stock-name { font-size: 22px; font-weight: 800; color: #1a1a2e; }
.stock-price { font-size: 36px; font-weight: 800; color: #1a1a2e; font-variant-numeric: tabular-nums; }
.price-change-up   { color: #16A34A; font-size: 15px; font-weight: 600; }
.price-change-down { color: #DC2626; font-size: 15px; font-weight: 600; }

/* CARDS */
.info-card {
    background: #fff;
    border-radius: 14px;
    padding: 16px;
    border: 1px solid #E8EAF0;
    height: 100%;
}
.info-card-title { font-size: 12px; color: #6B7280; margin-bottom: 6px; font-weight: 500; }
.info-card-val   { font-size: 22px; font-weight: 800; color: #1a1a2e; font-variant-numeric: tabular-nums; }
.info-card-sub   { font-size: 12px; color: #9CA3AF; margin-top: 3px; }

/* TARGET CARDS */
.tgt-card {
    background: #fff;
    border-radius: 12px;
    padding: 14px 16px;
    border: 1px solid #E8EAF0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}
.tgt-label { font-size: 13px; color: #6B7280; font-weight: 500; }
.tgt-price-up   { font-size: 18px; font-weight: 800; color: #16A34A; font-variant-numeric: tabular-nums; }
.tgt-price-down { font-size: 18px; font-weight: 800; color: #DC2626; font-variant-numeric: tabular-nums; }
.tgt-price-stop { font-size: 18px; font-weight: 800; color: #DC2626; font-variant-numeric: tabular-nums; }
.tgt-pct-up   { font-size: 12px; color: #16A34A; font-weight: 600; }
.tgt-pct-down { font-size: 12px; color: #DC2626; font-weight: 600; }

/* INDICATOR PILL */
.ind-pill {
    background: #F9FAFB;
    border: 1px solid #E8EAF0;
    border-radius: 10px;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
    font-size: 13px;
}
.ind-name  { color: #374151; font-weight: 500; }
.ind-val   { color: #1a1a2e; font-weight: 700; font-variant-numeric: tabular-nums; }
.ind-green { color: #16A34A; font-size: 11px; font-weight: 600; }
.ind-red   { color: #DC2626; font-size: 11px; font-weight: 600; }
.ind-gray  { color: #9CA3AF; font-size: 11px; font-weight: 600; }

/* CALC */
.calc-card {
    background: #fff;
    border-radius: 14px;
    padding: 20px;
    border: 1px solid #E8EAF0;
}
.calc-title { font-size: 15px; font-weight: 700; color: #1a1a2e; margin-bottom: 14px; }
.calc-result-box {
    background: #F0FDF4;
    border: 1.5px solid #86EFAC;
    border-radius: 10px;
    padding: 14px;
    text-align: center;
    margin-top: 12px;
}
.calc-result-box.loss {
    background: #FFF1F2;
    border-color: #FCA5A5;
}
.result-val-profit { font-size: 28px; font-weight: 800; color: #15803D; font-variant-numeric: tabular-nums; }
.result-val-loss   { font-size: 28px; font-weight: 800; color: #DC2626; font-variant-numeric: tabular-nums; }
.result-pct { font-size: 14px; font-weight: 600; }
.calc-row-item {
    display: flex; justify-content: space-between;
    padding: 7px 0; border-bottom: 1px solid #F3F4F6;
    font-size: 13px;
}
.calc-row-label { color: #6B7280; }
.calc-row-val   { color: #1a1a2e; font-weight: 600; font-variant-numeric: tabular-nums; }

/* ALERT CARD */
.alert-card {
    background: #fff;
    border-radius: 12px;
    padding: 12px 16px;
    border: 1px solid #E8EAF0;
    border-right: 4px solid #2563EB;
    margin-bottom: 8px;
    font-size: 13px;
}

/* SCORE BAR */
.score-wrap { background: #F3F4F6; border-radius: 99px; height: 8px; overflow: hidden; margin-top: 6px; }
.score-fill { height: 8px; border-radius: 99px; }

/* PAGE CONTENT */
.page-body { padding: 20px 24px; background: #F5F6FA; }
.section-label { font-size: 14px; font-weight: 700; color: #374151; margin: 18px 0 10px; }

/* Streamlit fixes */
.stButton > button {
    background: #2563EB !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    height: 42px !important;
    width: 100% !important;
}
.stTextInput > div > input {
    background: #F9FAFB !important;
    border: 1.5px solid #E8EAF0 !important;
    border-radius: 10px !important;
    color: #1a1a2e !important;
    font-size: 15px !important;
    height: 42px !important;
    text-align: right !important;
    direction: ltr !important;
}
.stNumberInput > div > div > input {
    background: #F9FAFB !important;
    border: 1.5px solid #E8EAF0 !important;
    border-radius: 8px !important;
    color: #1a1a2e !important;
    text-align: left !important;
}
.stSelectbox > div > div {
    background: #F9FAFB !important;
    border: 1.5px solid #E8EAF0 !important;
    border-radius: 8px !important;
    color: #1a1a2e !important;
}
div[data-testid="stNotification"] { display: none; }
.stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# HELPERS
# ══════════════════════════════════════
def N(v, d=2):
    """English numerals always"""
    s = f"{v:,.{d}f}"
    for a,e in zip('٠١٢٣٤٥٦٧٨٩','0123456789'): s=s.replace(a,e)
    return s

def flt(s):
    try: return float(s.dropna().iloc[-1])
    except: return 0.0

def detect(ticker):
    t = ticker.upper()
    if t.endswith(".SR"): return "ر.س", "SAR"
    return "$", "USD"

# ══════════════════════════════════════
# INDICATORS  (all run in background)
# ══════════════════════════════════════
def rsi(c,n=14):
    d=c.diff();g=d.clip(lower=0).rolling(n).mean();l=(-d.clip(upper=0)).rolling(n).mean()
    return 100-100/(1+g/(l+1e-9))

def macd(c,f=12,sl=26,sg=9):
    ef=c.ewm(span=f,adjust=False).mean();es=c.ewm(span=sl,adjust=False).mean()
    m=ef-es;s=m.ewm(span=sg,adjust=False).mean();return m,s,m-s

def bb(c,n=20,k=2):
    m=c.rolling(n).mean();sd=c.rolling(n).std();return m+k*sd,m,m-k*sd

def stoch(h,l,c,kp=14,dp=3):
    ll=l.rolling(kp).min();hh=h.rolling(kp).max()
    k=100*(c-ll)/(hh-ll+1e-9);return k,k.rolling(dp).mean()

def atr(h,l,c,n=14):
    tr=pd.concat([(h-l),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    return tr.rolling(n).mean()

def adx(h,l,c,n=14):
    tr=pd.concat([(h-l),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    dmp=(h-h.shift()).clip(lower=0);dmm=(l.shift()-l).clip(lower=0)
    dmp=dmp.where(dmp>dmm,0);dmm=dmm.where(dmm>dmp,0)
    a=tr.ewm(span=n,adjust=False).mean()
    dip=100*dmp.ewm(span=n,adjust=False).mean()/(a+1e-9)
    dim=100*dmm.ewm(span=n,adjust=False).mean()/(a+1e-9)
    dx=100*(dip-dim).abs()/(dip+dim+1e-9)
    return dx.ewm(span=n,adjust=False).mean(),dip,dim

def cci(h,l,c,n=20):
    tp=(h+l+c)/3;return (tp-tp.rolling(n).mean())/(0.015*tp.rolling(n).std()+1e-9)

def wr(h,l,c,n=14):
    hh=h.rolling(n).max();ll=l.rolling(n).min()
    return -100*(hh-c)/(hh-ll+1e-9)

def mfi(h,l,c,v,n=14):
    tp=(h+l+c)/3;mf=tp*v
    pos=mf.where(tp>tp.shift(),0).rolling(n).sum()
    neg=mf.where(tp<tp.shift(),0).rolling(n).sum()
    return 100-100/(1+pos/(neg+1e-9))

def cmf(h,l,c,v,n=20):
    mfv=((c-l)-(h-c))/(h-l+1e-9)*v
    return mfv.rolling(n).sum()/(v.rolling(n).sum()+1e-9)

def sar(h,l,af=0.02,afm=0.2):
    sv=np.zeros(len(h));tr=np.ones(len(h))
    sv[0]=float(l.iloc[0]);ep=float(h.iloc[0]);a=af
    for i in range(1,len(h)):
        ps=sv[i-1]
        if tr[i-1]==1:
            sv[i]=ps+a*(ep-ps)
            sv[i]=min(sv[i],float(l.iloc[max(0,i-1)]),float(l.iloc[max(0,i-2)]))
            if float(l.iloc[i])<sv[i]: tr[i]=-1;sv[i]=ep;ep=float(l.iloc[i]);a=af
            else:
                tr[i]=1
                if float(h.iloc[i])>ep: ep=float(h.iloc[i]);a=min(a+af,afm)
        else:
            sv[i]=ps+a*(ep-ps)
            sv[i]=max(sv[i],float(h.iloc[max(0,i-1)]),float(h.iloc[max(0,i-2)]))
            if float(h.iloc[i])>sv[i]: tr[i]=1;sv[i]=ep;ep=float(h.iloc[i]);a=af
            else:
                tr[i]=-1
                if float(l.iloc[i])<ep: ep=float(l.iloc[i]);a=min(a+af,afm)
    return pd.Series(sv,index=h.index),pd.Series(tr,index=h.index)

def fib_levels(c):
    hi=float(c.tail(60).max());lo=float(c.tail(60).min());d=hi-lo
    return {"0%":hi,"23.6%":hi-0.236*d,"38.2%":hi-0.382*d,
            "50%":hi-0.5*d,"61.8%":hi-0.618*d,"100%":lo}

def pivot(h,l,c):
    hv=float(h.tail(20).max());lv=float(l.tail(20).min());cv=float(c.iloc[-1])
    p=(hv+lv+cv)/3
    return {"P":p,"R1":2*p-lv,"R2":p+(hv-lv),"S1":2*p-hv,"S2":p-(hv-lv)}

def smart_targets(px,atr_v,sig_type,fibs,pivs):
    if sig_type in ("buy","watch_buy"):
        t1=fibs["38.2%"] if fibs["38.2%"]>px else px+atr_v*1.5
        t2=pivs["R1"]    if pivs["R1"]>t1    else px+atr_v*3.0
        t3=pivs["R2"]    if pivs["R2"]>t2    else fibs["61.8%"] if fibs["61.8%"]>t2 else px+atr_v*5.0
        sl=pivs["S1"]    if pivs["S1"]<px    else px-atr_v*2.0
        return [("الهدف الأول",round(t1,2),True),
                ("الهدف الثاني",round(t2,2),True),
                ("الهدف الثالث",round(t3,2),True),
                ("وقف الخسارة",round(sl,2),False)]
    else:
        t1=pivs["S1"]  if pivs["S1"]<px  else px-atr_v*1.5
        t2=pivs["S2"]  if pivs["S2"]<t1  else px-atr_v*3.0
        t3=fibs["61.8%"] if fibs["61.8%"]<t2 else px-atr_v*5.0
        sl=pivs["R1"]  if pivs["R1"]>px  else px+atr_v*2.0
        return [("هدف هبوط 1",round(t1,2),False),
                ("هدف هبوط 2",round(t2,2),False),
                ("هدف هبوط 3",round(t3,2),False),
                ("نقطة إعادة دخول",round(sl,2),True)]

def score_all(rsi_v,macd_v,macd_sv,px,e20,e50,s200,stk_v,bbu,bbl,
              vol,vol_avg,adx_v,dip_v,dim_v,cci_v,wr_v,mfi_v,cmf_v,sar_tr):
    sc=50; breakdown={}
    # RSI
    if rsi_v<30:   sc+=8;  breakdown["RSI"]=("ذروة بيع","g")
    elif rsi_v<45: sc+=10; breakdown["RSI"]=("صعودي","g")
    elif rsi_v<60: sc+=5;  breakdown["RSI"]=("محايد","n")
    elif rsi_v<70: sc+=0;  breakdown["RSI"]=("قرب الذروة","y")
    else:          sc-=20; breakdown["RSI"]=("ذروة شراء","r")
    # MACD
    if macd_v>macd_sv: sc+=18; breakdown["MACD"]=("صاعد","g")
    else:              sc-=18; breakdown["MACD"]=("هابط","r")
    # MAs
    mp=0
    if px>e20:  mp+=5
    if px>e50:  mp+=7
    if px>s200: mp+=8
    sc+=mp-10
    breakdown["المتوسطات"]=("فوق المتوسطات","g") if mp>=15 else ("مختلطة","y") if mp>=8 else ("تحت المتوسطات","r")
    # ADX
    if adx_v>25:
        if dip_v>dim_v: sc+=10; breakdown["ADX"]=("اتجاه صاعد","g")
        else:           sc-=10; breakdown["ADX"]=("اتجاه هابط","r")
    else: breakdown["ADX"]=("جانبي","n")
    # Stoch
    if stk_v<20:   sc+=8; breakdown["Stoch"]=("ذروة بيع","g")
    elif stk_v>80: sc-=8; breakdown["Stoch"]=("ذروة شراء","r")
    else:          sc+=2; breakdown["Stoch"]=("محايد","n")
    # BB
    if px<bbl:   sc+=6; breakdown["BB"]=("تحت النطاق","g")
    elif px>bbu: sc-=6; breakdown["BB"]=("فوق النطاق","r")
    else:        sc+=1; breakdown["BB"]=("داخل النطاق","n")
    # CCI
    if cci_v<-100: sc+=5; breakdown["CCI"]=("ذروة بيع","g")
    elif cci_v>100:sc-=5; breakdown["CCI"]=("ذروة شراء","r")
    else:          sc+=1; breakdown["CCI"]=("محايد","n")
    # WR
    if wr_v<-80:  sc+=5; breakdown["W%R"]=("ذروة بيع","g")
    elif wr_v>-20:sc-=5; breakdown["W%R"]=("ذروة شراء","r")
    else:         sc+=1; breakdown["W%R"]=("محايد","n")
    # MFI
    if mfi_v<20:  sc+=4; breakdown["MFI"]=("ضغط بيع","g")
    elif mfi_v>80:sc-=4; breakdown["MFI"]=("ضغط شراء","r")
    else:         sc+=1; breakdown["MFI"]=("طبيعي","n")
    # CMF
    if cmf_v>0.1:  sc+=5; breakdown["CMF"]=("تدفق شراء","g")
    elif cmf_v<-0.1:sc-=5;breakdown["CMF"]=("تدفق بيع","r")
    else:          sc+=0; breakdown["CMF"]=("محايد","n")
    # Volume
    vr=vol/(vol_avg+1e-9)
    if vr>1.5:  sc+=5; breakdown["Volume"]=("تأكيد حجم","g")
    elif vr<0.5:sc-=3; breakdown["Volume"]=("حجم ضعيف","r")
    else:       sc+=1; breakdown["Volume"]=("طبيعي","n")
    # SAR
    if sar_tr==1: sc+=5; breakdown["SAR"]=("صاعد","g")
    else:         sc-=5; breakdown["SAR"]=("هابط","r")
    return max(0,min(100,int(sc))), breakdown

def get_signal(score):
    if score>=65:   return "دخول الآن","buy-now","buy","#16A34A"
    elif score>=45: return "استعداد دخول","ready-buy","watch_buy","#059669"
    elif score>=28: return "استعداد خروج","ready-sell","watch_sell","#D97706"
    else:           return "خروج الآن","sell-now","sell","#DC2626"

def market_state(px,e50,s200,adx_v,dip_v,dim_v):
    if px>e50 and px>s200 and adx_v>25 and dip_v>dim_v: return "اتجاه صاعد قوي","#16A34A"
    elif px<e50 and px<s200 and adx_v>25: return "اتجاه هابط قوي","#DC2626"
    elif adx_v<20: return "تداول جانبي","#D97706"
    elif px>e50:   return "صاعد معتدل","#059669"
    else:          return "هابط معتدل","#DC2626"

# ══════════════════════════════════════
# TOP NAV
# ══════════════════════════════════════
st.markdown("""
<div class="top-nav">
  <div class="nav-logo">يلا<span>سكالب</span></div>
  <div style="color:#6B7280;font-size:13px">التحليل الفني الاحترافي</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# SEARCH
# ══════════════════════════════════════
st.markdown('<div class="search-section">', unsafe_allow_html=True)
sc1,sc2,sc3,sc4 = st.columns([4,1,1,1])
with sc1:
    ticker = st.text_input("",placeholder="ابحث عن رمز السهم... (مثال: 2222.SR أو AAPL)",
                           label_visibility="collapsed").upper().strip()
with sc2:
    analyze = st.button("تحليل", use_container_width=True)
with sc3:
    period = st.selectbox("",["3mo","6mo","1y"],index=1,
                          format_func=lambda x:{"3mo":"3م","6mo":"6م","1y":"سنة"}[x],
                          label_visibility="collapsed")
with sc4:
    interval = st.selectbox("",["1d","1wk"],index=0,
                            format_func=lambda x:{"1d":"يومي","1wk":"أسبوعي"}[x],
                            label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════
# ANALYSIS
# ══════════════════════════════════════
if analyze and ticker:
    sym, currency = detect(ticker)

    with st.spinner(""):
        try:
            data = yf.download(ticker,period=period,interval=interval,
                               progress=False,auto_adjust=True)
            try: info = yf.Ticker(ticker).info or {}
            except: info = {}
        except Exception as e:
            st.error(f"خطأ في التحميل: {e}"); st.stop()

    if data is None or data.empty or len(data)<30:
        st.error("لم يتم العثور على بيانات. تحقق من رمز السهم.")
        st.stop()

    if isinstance(data.columns,pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    C=data["Close"].astype(float); H=data["High"].astype(float)
    L=data["Low"].astype(float);   V=data["Volume"].astype(float)
    O=data["Open"].astype(float)

    # All indicators (background)
    rsi_s              = rsi(C)
    ml,ms,mh           = macd(C)
    bbu_s,bbm_s,bbl_s  = bb(C)
    stk_s,std_s        = stoch(H,L,C)
    atr_s              = atr(H,L,C)
    adx_s,dip_s,dim_s  = adx(H,L,C)
    cci_s              = cci(H,L,C)
    wr_s               = wr(H,L,C)
    mfi_s              = mfi(H,L,C,V)
    cmf_s              = cmf(H,L,C,V)
    sar_s,sar_tr_s     = sar(H,L)
    e20_s              = C.ewm(span=20,adjust=False).mean()
    e50_s              = C.ewm(span=50,adjust=False).mean()
    s200_s             = C.rolling(200).mean()
    vol_ma             = V.rolling(20).mean()
    fibs               = fib_levels(C)
    pivs               = pivot(H,L,C)

    px      = float(C.iloc[-1])
    rsi_v   = flt(rsi_s);  macd_v=flt(ml);  macd_sv=flt(ms)
    bbu_v   = flt(bbu_s);  bbl_v=flt(bbl_s)
    stk_v   = flt(stk_s);  std_v=flt(std_s)
    atr_v   = flt(atr_s)
    adx_v   = flt(adx_s);  dip_v=flt(dip_s); dim_v=flt(dim_s)
    cci_v   = flt(cci_s);  wr_v=flt(wr_s);  mfi_v=flt(mfi_s); cmf_v=flt(cmf_s)
    sar_tr  = float(sar_tr_s.iloc[-1])
    e20_v   = flt(e20_s);  e50_v=flt(e50_s); s200_v=flt(s200_s)
    vol_v   = float(V.iloc[-1]); vol_avg=flt(vol_ma)
    prev    = float(C.iloc[-2]) if len(C)>1 else px
    chg     = px-prev; chg_pct=(chg/prev)*100

    score, breakdown = score_all(rsi_v,macd_v,macd_sv,px,e20_v,e50_v,s200_v,
                                  stk_v,bbu_v,bbl_v,vol_v,vol_avg,
                                  adx_v,dip_v,dim_v,cci_v,wr_v,mfi_v,cmf_v,sar_tr)
    sig_lbl,sig_cls,sig_type,sig_color = get_signal(score)
    targets = smart_targets(px,atr_v,sig_type,fibs,pivs)
    mkt_lbl,mkt_clr = market_state(px,e50_v,s200_v,adx_v,dip_v,dim_v)
    company = info.get("longName",ticker) or ticker
    vol_ratio = vol_v/(vol_avg+1e-9)

    badge_map = {
        "buy-now":   "badge-buy-now",
        "ready-buy": "badge-ready-buy",
        "ready-sell":"badge-ready-sell",
        "sell-now":  "badge-sell-now",
    }

    # ══ STOCK HEADER ══════════════════════
    st.markdown(f"""
    <div class="stock-header">
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">
        <div>
          <div class="stock-name">{company} &nbsp;<span style="color:#6B7280;font-size:14px;font-weight:400">{ticker}</span></div>
          <div style="display:flex;align-items:baseline;gap:12px;margin-top:4px">
            <span class="stock-price">{sym}{N(px)}</span>
            <span class="{'price-change-up' if chg>=0 else 'price-change-down'}">
              {'▲' if chg>=0 else '▼'} {N(abs(chg))} ({N(abs(chg_pct),2)}%)
            </span>
          </div>
          <div style="color:#6B7280;font-size:12px;margin-top:4px">{currency} • {datetime.now().strftime('%Y-%m-%d  %H:%M')}</div>
        </div>
        <div style="text-align:left">
          <div class="{badge_map[sig_cls]}" style="font-size:16px;padding:10px 24px;margin-bottom:8px">{sig_lbl}</div>
          <div style="color:#6B7280;font-size:12px;text-align:center">قوة الإشارة: {score}/100</div>
          <div class="score-wrap" style="width:160px">
            <div class="score-fill" style="width:{score}%;background:{sig_color}"></div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══ PAGE BODY ══════════════════════
    st.markdown('<div class="page-body">', unsafe_allow_html=True)

    left_col, right_col = st.columns([2, 1], gap="medium")

    with left_col:
        # ── Quick Stats ──
        qc = st.columns(4)
        stats = [
            ("RSI (14)",   N(rsi_v,1), "ذروة شراء" if rsi_v>70 else "ذروة بيع" if rsi_v<30 else "محايد",
             "#DC2626" if rsi_v>70 else "#16A34A" if rsi_v<30 else "#6B7280"),
            ("ADX (14)",   N(adx_v,1), "قوي" if adx_v>25 else "ضعيف", "#1D4ED8" if adx_v>25 else "#6B7280"),
            ("ATR (14)",   f"{sym}{N(atr_v)}", "التذبذب اليومي", "#374151"),
            ("الحجم",      f"{vol_v/1e6:.1f}M" if vol_v>1e5 else N(vol_v,0),
             f"{vol_ratio:.1f}x المتوسط", "#16A34A" if vol_ratio>1.2 else "#DC2626" if vol_ratio<0.6 else "#6B7280"),
        ]
        for i,(lbl,val,sub,clr) in enumerate(stats):
            with qc[i]:
                st.markdown(f"""<div class="info-card">
                    <div class="info-card-title">{lbl}</div>
                    <div class="info-card-val" style="color:{clr}">{val}</div>
                    <div class="info-card-sub">{sub}</div>
                </div>""", unsafe_allow_html=True)

        # ── Chart ──
        st.markdown('<div class="section-label">الرسم البياني</div>', unsafe_allow_html=True)

        fig = make_subplots(rows=3,cols=1,shared_xaxes=True,
                            vertical_spacing=0.02,row_heights=[0.60,0.20,0.20],
                            subplot_titles=("","RSI","MACD"))

        # Candles only
        fig.add_trace(go.Candlestick(
            x=data.index,open=O,high=H,low=L,close=C,name="السعر",
            increasing=dict(fillcolor="#16A34A",line=dict(color="#16A34A",width=0.8)),
            decreasing=dict(fillcolor="#DC2626",line=dict(color="#DC2626",width=0.8))),
            row=1,col=1)

        # Target lines on candles ONLY
        tgt_colors = ["#16A34A","#15803D","#166534","#DC2626"]
        tgt_dashes = ["dash","dash","dash","dot"]
        for i,(name,tpx,is_up) in enumerate(targets):
            pct=(tpx-px)/px*100
            clr = "#16A34A" if is_up else "#DC2626"
            dash = "dash" if is_up else "dot"
            fig.add_hline(y=tpx,row=1,col=1,
                line=dict(color=clr,width=1.5,dash=dash),
                annotation_text=f"  {name}: {sym}{N(tpx)} ({pct:+.1f}%)",
                annotation_position="right",
                annotation_font=dict(size=10,color=clr))

        # RSI
        fig.add_trace(go.Scatter(x=data.index,y=rsi_s,name="RSI",
            line=dict(color="#2563EB",width=1.8)),row=2,col=1)
        fig.add_hrect(y0=70,y1=100,fillcolor="rgba(220,38,38,0.05)",line_width=0,row=2,col=1)
        fig.add_hrect(y0=0,y1=30,fillcolor="rgba(22,163,74,0.05)",line_width=0,row=2,col=1)
        for y,c in [(70,"#DC2626"),(50,"#D1D5DB"),(30,"#16A34A")]:
            fig.add_hline(y=y,line=dict(color=c,width=0.8,dash="dot"),row=2,col=1)

        # MACD
        hc=["#16A34A" if v>=0 else "#DC2626" for v in mh.fillna(0)]
        fig.add_trace(go.Bar(x=data.index,y=mh,name="Hist",marker_color=hc,opacity=0.7),row=3,col=1)
        fig.add_trace(go.Scatter(x=data.index,y=ml,name="MACD",line=dict(color="#2563EB",width=1.5)),row=3,col=1)
        fig.add_trace(go.Scatter(x=data.index,y=ms,name="Signal",line=dict(color="#F59E0B",width=1.5)),row=3,col=1)
        fig.add_hline(y=0,line=dict(color="#E5E7EB",width=0.8),row=3,col=1)

        fig.update_layout(
            height=560,
            showlegend=False,
            xaxis_rangeslider_visible=False,
            plot_bgcolor="#fff",
            paper_bgcolor="#F5F6FA",
            font=dict(family="Tajawal,sans-serif",color="#374151",size=11),
            margin=dict(l=4,r=130,t=8,b=4),
            separators=",.",
        )
        for ann in fig.layout.annotations:
            ann.font.size=10

        fig.update_xaxes(showgrid=True,gridcolor="#F3F4F6",zeroline=False)
        fig.update_yaxes(showgrid=True,gridcolor="#F3F4F6",zeroline=False)

        st.plotly_chart(fig,use_container_width=True)

        # ── Targets ──
        st.markdown('<div class="section-label">نقاط الأهداف</div>', unsafe_allow_html=True)
        tc = st.columns(4)
        for i,(name,tpx,is_up) in enumerate(targets):
            pct=(tpx-px)/px*100
            clr="#16A34A" if is_up else "#DC2626"
            icon="▲" if is_up else "▼"
            rr=abs(tpx-px)/abs(px-targets[3][1]+1e-9) if i<3 else 0
            with tc[i]:
                st.markdown(f"""<div class="info-card" style="border-right:3px solid {clr}">
                    <div class="info-card-title">{name}</div>
                    <div class="info-card-val" style="color:{clr}">{sym}{N(tpx)}</div>
                    <div style="color:{clr};font-size:12px;font-weight:600">{icon} {pct:+.1f}%</div>
                    {'<div class="info-card-sub">R/R: '+N(rr,1)+'x</div>' if i<3 else ''}
                </div>""", unsafe_allow_html=True)

        # ── Indicators Breakdown ──
        st.markdown('<div class="section-label">تفصيل المؤشرات الفنية</div>', unsafe_allow_html=True)
        color_map = {"g":"#16A34A","r":"#DC2626","y":"#D97706","n":"#6B7280"}
        ic = st.columns(2)
        items = list(breakdown.items())
        half = len(items)//2
        for col_idx, col_items in enumerate([items[:half+1], items[half+1:]]):
            with ic[col_idx]:
                for k,(label,ctype) in col_items:
                    clr = color_map.get(ctype,"#6B7280")
                    st.markdown(f"""<div class="ind-pill">
                        <span class="ind-name">{k}</span>
                        <span style="color:{clr};font-size:12px;font-weight:600">{label}</span>
                    </div>""", unsafe_allow_html=True)

    # ══ RIGHT COLUMN ══════════════════════
    with right_col:

        # ── Signal Summary Card ──
        st.markdown(f"""<div class="info-card" style="margin-bottom:12px;border-right:3px solid {sig_color}">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                <div style="font-size:13px;font-weight:700;color:#374151">ملخص التحليل</div>
                <div class="{badge_map[sig_cls]}">{sig_lbl}</div>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                <span style="color:#6B7280;font-size:13px">حالة السوق</span>
                <span style="color:{mkt_clr};font-size:13px;font-weight:600">{mkt_lbl}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                <span style="color:#6B7280;font-size:13px">قوة الإشارة</span>
                <span style="color:{sig_color};font-size:13px;font-weight:700">{score}/100</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                <span style="color:#6B7280;font-size:13px">MACD</span>
                <span style="color:{'#16A34A' if macd_v>macd_sv else '#DC2626'};font-size:13px;font-weight:600">{'صاعد ▲' if macd_v>macd_sv else 'هابط ▼'}</span>
            </div>
            <div style="display:flex;justify-content:space-between">
                <span style="color:#6B7280;font-size:13px">Stochastic</span>
                <span style="color:{'#DC2626' if stk_v>80 else '#16A34A' if stk_v<20 else '#6B7280'};font-size:13px;font-weight:600">{N(stk_v,1)}</span>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── Profit Calculator ──
        st.markdown('<div class="calc-card">', unsafe_allow_html=True)
        st.markdown('<div class="calc-title">💰 حاسبة الأرباح</div>', unsafe_allow_html=True)

        shares = st.number_input("عدد الأسهم", min_value=1, value=100, step=1)
        entry  = st.number_input(f"سعر الدخول ({sym})", min_value=0.01,
                                  value=round(px,2), step=0.01, format="%.2f")
        tgt_opts = {
            f"الهدف الأول  {sym}{N(targets[0][1])}": targets[0][1],
            f"الهدف الثاني  {sym}{N(targets[1][1])}": targets[1][1],
            f"الهدف الثالث  {sym}{N(targets[2][1])}": targets[2][1],
            "سعر مخصص": None,
        }
        chosen = st.selectbox("السعر المستهدف", list(tgt_opts.keys()))
        if tgt_opts[chosen] is None:
            exit_px = st.number_input(f"أدخل السعر ({sym})", min_value=0.01,
                                       value=round(px*1.05,2), step=0.01, format="%.2f")
        else:
            exit_px = tgt_opts[chosen]

        cr = 0.0015
        cost   = shares * entry
        out    = shares * exit_px
        comm   = (cost+out)*cr
        gross  = out - cost
        net    = gross - comm
        pct    = net/cost*100 if cost>0 else 0
        profit = net>=0

        st.markdown(f"""
        <div class="calc-result-box {'loss' if not profit else ''}">
            <div class="{'result-val-profit' if profit else 'result-val-loss'}">{sym}{N(abs(net))}</div>
            <div class="result-pct" style="color:{'#15803D' if profit else '#DC2626'}">{pct:+.2f}%</div>
            <div style="color:#6B7280;font-size:11px;margin-top:4px">صافي الربح/الخسارة</div>
        </div>
        <div style="margin-top:12px">
          <div class="calc-row-item">
            <span class="calc-row-label">رأس المال</span>
            <span class="calc-row-val">{sym}{N(cost)}</span>
          </div>
          <div class="calc-row-item">
            <span class="calc-row-label">القيمة عند الهدف</span>
            <span class="calc-row-val">{sym}{N(out)}</span>
          </div>
          <div class="calc-row-item">
            <span class="calc-row-label">العمولة (0.15%)</span>
            <span class="calc-row-val" style="color:#D97706">-{sym}{N(comm)}</span>
          </div>
          <div class="calc-row-item" style="border:none">
            <span class="calc-row-label">وقف الخسارة</span>
            <span class="calc-row-val" style="color:#DC2626">{sym}{N(targets[3][1])}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # R/R
        st.markdown('<div style="margin-top:10px">', unsafe_allow_html=True)
        for i,(name,tpx,is_up) in enumerate(targets[:3]):
            risk_ = abs(px - targets[3][1])
            rew_  = abs(tpx - px)
            rr    = rew_/(risk_+1e-9)
            rrc   = "#16A34A" if rr>=2 else "#D97706" if rr>=1 else "#DC2626"
            st.markdown(f"""<div style="display:flex;justify-content:space-between;
                padding:5px 0;font-size:12px;border-bottom:1px solid #F3F4F6">
                <span style="color:#6B7280">{name}</span>
                <span style="color:{rrc};font-weight:600">R/R {N(rr,1)}x {"✓" if rr>=2 else "!"}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Alerts ──
        st.markdown('<div class="section-label">التنبيهات</div>', unsafe_allow_html=True)
        alerts = []
        if rsi_v > 70:
            alerts.append(("🔴","RSI في ذروة الشراء","يحتمل تصحيح — انتبه","#DC2626"))
        if rsi_v < 30:
            alerts.append(("🟢","RSI في ذروة البيع","فرصة شراء محتملة","#16A34A"))
        if macd_v > macd_sv and macd_v < 0:
            alerts.append(("🟢","MACD تقاطع صعودي","بداية زخم إيجابي","#16A34A"))
        if macd_v < macd_sv and macd_v > 0:
            alerts.append(("🔴","MACD تقاطع هبوطي","بداية زخم سلبي","#DC2626"))
        if stk_v < 20:
            alerts.append(("🟢","Stochastic ذروة بيع","منطقة دعم قوية","#16A34A"))
        if stk_v > 80:
            alerts.append(("🔴","Stochastic ذروة شراء","منطقة مقاومة","#DC2626"))
        if vol_ratio > 2:
            alerts.append(("🟡","حجم تداول مرتفع جداً",f"{vol_ratio:.1f}x المتوسط — تأكيد الحركة","#D97706"))
        if e50_v > s200_v and abs(e50_v-s200_v)/s200_v < 0.005:
            alerts.append(("🟢","Golden Cross قريب","EMA50 تقترب من SMA200","#16A34A"))
        if not alerts:
            alerts.append(("⚪","لا توجد تنبيهات فعالة","المؤشرات في نطاق طبيعي","#6B7280"))

        for icon,title,desc,clr in alerts:
            st.markdown(f"""<div class="alert-card" style="border-right-color:{clr}">
                <div style="display:flex;align-items:center;gap:8px">
                    <span style="font-size:16px">{icon}</span>
                    <div>
                        <div style="font-weight:700;color:#1a1a2e;font-size:13px">{title}</div>
                        <div style="color:#6B7280;font-size:12px">{desc}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center;padding:100px 20px">
        <div style="font-size:56px;margin-bottom:16px">📈</div>
        <div style="font-size:22px;font-weight:800;color:#1a1a2e;margin-bottom:8px">ابحث عن أي سهم للبدء</div>
        <div style="color:#6B7280;font-size:15px;line-height:2.4">
            السوق السعودي: 2222.SR &nbsp;•&nbsp; 1120.SR &nbsp;•&nbsp; 2010.SR<br>
            السوق الأمريكي: AAPL &nbsp;•&nbsp; TSLA &nbsp;•&nbsp; MSFT &nbsp;•&nbsp; NVDA
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:20px;color:#D1D5DB;font-size:11px;background:#fff;border-top:1px solid #E8EAF0;margin-top:20px">
للأغراض التعليمية فقط • ليست توصية استثمارية
</div>
""", unsafe_allow_html=True)
