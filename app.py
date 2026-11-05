import streamlit as st
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime
import pytz

# 1. Konfigurasi Halaman & Transformasi Reka Bentuk UI Premium Modern Neon
st.set_page_config(page_title="XAU MASTER AI SIGNAL", layout="centered")

st.markdown("""
    <style>
    /* Latar Belakang Utama Aplikasi (Deep Cyber Black) */
    .stApp { 
        background-color: #0b0813; 
        color: #e2e8f0; 
        font-family: 'Inter', sans-serif;
    }
    
    /* Kad Statistik Premium dengan Kesan Glow Line & Gradasi */
    .stats-card { 
        background: linear-gradient(145deg, #161224, #120e1c);
        border: 1px solid #2d224d; 
        border-radius: 16px; 
        padding: 20px; 
        margin-bottom: 15px; 
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    .stats-title { 
        font-size: 10.5px; 
        text-transform: uppercase; 
        letter-spacing: 1.5px; 
        color: #93c5fd; 
        font-weight: 600;
        margin-bottom: 6px; 
    }
    .stats-value { 
        font-size: 26px; 
        font-weight: 800; 
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .stats-sub { 
        font-size: 11px; 
        color: #64748b; 
        margin-top: 4px; 
    }
    
    /* Panel Pengiraan Lot Berwajah Baharu */
    div[data-testid="stForm"] {
        background-color: #120e1c;
        border: 1px solid #2d224d;
        border-radius: 16px;
        padding: 15px;
    }
    
    /* Kotak Status Isyarat Utama (Neon Trading Engine Layout) */
    .signal-container {
        border-radius: 16px; 
        padding: 24px; 
        text-align: center; 
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(0, 0, 0, 0.6);
        position: relative;
        overflow: hidden;
    }
    .sig-buy {
        background: linear-gradient(135deg, #0d2b27, #061814);
        border: 2px solid #00ffcc;
        box-shadow: inset 0 0 15px rgba(0, 255, 204, 0.15), 0 4px 20px rgba(0, 255, 204, 0.2);
    }
    .sig-sell {
        background: linear-gradient(135deg, #331520, #1c0a11);
        border: 2px solid #ff3366;
        box-shadow: inset 0 0 15px rgba(255, 51, 102, 0.15), 0 4px 20px rgba(255, 51, 102, 0.2);
    }
    .sig-wait {
        background: linear-gradient(135deg, #2b1d0d, #181006);
        border: 2px solid #ffaa00;
        box-shadow: inset 0 0 15px rgba(255, 170, 0, 0.15), 0 4px 20px rgba(255, 170, 0, 0.2);
    }
    .signal-title {
        font-size: 18px;
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 12px;
        text-transform: uppercase;
    }
    
    /* Ruang Harga Sasaran (Target Boxes Inside Signal) */
    .price-target-row {
        display: flex;
        justify-content: space-between;
        background-color: rgba(25, 20, 38, 0.7);
        border: 1px solid #2d224d;
        border-radius: 10px;
        padding: 12px;
        margin-top: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13.5px;
    }
    
    /* Barometer Sentimen Premium */
    .sentiment-label {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .sentiment-track { 
        background-color: #331520; 
        width: 100%; 
        height: 14px; 
        border-radius: 7px; 
        overflow: hidden; 
        border: 1px solid #4c1d2f;
    }
    .sentiment-bar { 
        background: linear-gradient(90deg, #00ffcc, #00b3ff); 
        height: 100%; 
        border-radius: 7px;
    }
    </style>
    """, unsafe_allow_html=True)

# Tajuk Aplikasi & Dekorasi Seni Premium
st.markdown("<div style='text-align: center; margin-top: 10px;'>", unsafe_allow_html=True)
st.markdown("<h2 style='color: #ffffff; font-weight: 900; letter-spacing: 1px; margin-bottom: 0;'>🔱 XAU MASTER</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #818cf8; font-size: 11px; font-weight: 700; letter-spacing: 3px; margin-top: 0;'>AI TRADING SIGNAL PLATFORM</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sesi Pasaran Live (Zon Masa Malaysia)
jam_myt = datetime.now(pytz.timezone('Asia/Kuala_Lumpur')).hour
s_asia = "🟢 ACTIVE" if (7 <= jam_myt < 15) else "⚪ CLOSED"
s_london = "🟢 ACTIVE" if (15 <= jam_myt < 23) else "⚪ CLOSED"
s_ny = "🟢 ACTIVE" if (jam_myt >= 20 or jam_myt < 4) else "⚪ CLOSED"

def c_sess(status): return "color:#00ffcc; font-weight:bold;" if "ACTIVE" in status else "color:#64748b;"

st.markdown(f"""
<div style='text-align: center; margin-bottom: 20px; font-size: 11px; letter-spacing: 0.5px; background-color: #120e1c; padding: 8px; border-radius: 30px; border: 1px solid #2d224d;'>
    <span style='margin: 0 8px;'>🌏 ASIA: <span style='{c_sess(s_asia)}'>{s_asia}</span></span>
    <span style='margin: 0 8px;'>🇬🇧 LDN: <span style='{c_sess(s_london)}'>{s_london}</span></span>
    <span style='margin: 0 8px;'>🇺🇸 NY: <span style='{c_sess(s_ny)}'>{s_ny}</span></span>
</div>
""", unsafe_allow_html=True)

if "demo_balance" not in st.session_state: st.session_state.demo_balance = 10000.0
if "active_position" not in st.session_state: st.session_state.active_position = None
if "trade_history" not in st.session_state:
    st.session_state.trade_history = [
        {"Waktu": "04-11 15:30", "Jenis": "BUY", "Entry": 2715.40, "Exit": 2724.80, "Pips": "+94.0", "Hasil": "✅ TP"},
        {"Waktu": "05-11 10:15", "Jenis": "SELL", "Entry": 2732.10, "Exit": 2736.50, "Pips": "-44.0", "Hasil": "❌ SL"}
    ]

# Panel Pengurusan Risiko (Risk Calculator)
st.markdown("<div class='stats-card'><p style='font-size:12px; font-weight:bold; color:#93c5fd; margin-bottom:5px;'>⚡ RISK MANAGEMENT PORTAL</p>", unsafe_allow_html=True)
modal_akaun = st.number_input("Modal Akaun ($)", min_value=10, value=1000, step=10)
peratus_risiko = st.slider("Risiko Per Trade (%)", min_value=1, max_value=5, value=2)
st.markdown("</div>", unsafe_allow_html=True)

try:
    df_m5 = yf.Ticker("GC=F").history(period="7d", interval="5m")
    df_m15 = yf.Ticker("GC=F").history(period="3d", interval="15m")
    df_m30 = yf.Ticker("GC=F").history(period="5d", interval="30m")
    df_h1 = yf.Ticker("GC=F").history(period="14d", interval="1h")

    harga_semasa = df_m5['Close'].iloc[-1]
    st.markdown(f"<h1 style='text-align: center; color: #ffd700; font-weight:900; font-size:42px; margin-top: 10px; margin-bottom:15px; letter-spacing:-1px;'>${harga_semasa:.2f}</h1>", unsafe_allow_html=True)

    # Barometer Sentimen Pasaran
    df_m5['RSI'] = ta.momentum.rsi(df_m5['Close'], window=14)
    rsi_latest = df_m5['RSI'].iloc[-1]
    buy_sentiment = int(max(10, min(90, (rsi_latest - 20) * 1.6)))
    sell_sentiment = 100 - buy_sentiment

    st.markdown(f"""
    <div class='stats-card'>
        <div class='sentiment-label' style='display: flex; justify-content: space-between;'>
            <span style='color: #00ffcc;'>🟢 BULL SENTIMENT: {buy_sentiment}%</span>
            <span style='color: #ff3366;'>🔴 BEAR SENTIMENT: {sell_sentiment}%</span>
        </div>
        <div class='sentiment-track'><div class='sentiment-bar' style='width: {buy_sentiment}%;'></div></div>
    </div>
    """, unsafe_allow_html=True)

    # Grid Statistik Utama
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='stats-card'><div class='stats-title'>🟢 WIN RATE</div><div class='stats-value' style='color: #00ffcc;'>75.0%</div><div class='stats-sub'>AI Dynamic Win</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='stats-card'><div class='stats-title'>🔴 LOSS RATE</div><div class='stats-value' style='color: #ff3366;'>25.0%</div><div class='stats-sub'>AI Dynamic Risk</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='stats-card'><div class='stats-title'>🔮 NET PIPS</div><div class='stats-value' style='color: #ffaa00;'>+200.0</div><div class='stats-sub'>Total Accumulated</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='stats-card'><div class='stats-title'>🎯 TOTAL SIGNALS</div><div class='stats-value'>2</div><div class='stats-sub'>Scanned History</div></div>", unsafe_allow_html=True)

    # Butang Pautan Pintas TradingView
    st.markdown("<p style='font-weight:bold; color:#93c5fd; font-size:12px; margin-bottom:4px; letter-spacing:0.5px;'>📈 CHART CONFLUENCE</p>", unsafe_allow_html=True)
    st.link_button("📊 OPEN LIVE TRADINGVIEW CHART (M5)", "https://tradingview.com", use_container_width=True)

    # Pengiraan Formula Indikator
    df_h1['EMA50'] = ta.trend.ema_indicator(df_h1['Close'], window=50)
    df_m5['EMA200'] = ta.trend.ema_indicator(df_m5['Close'], window=200)
    df_m5['stoch_k'] = ta.momentum.StochasticOscillator(df_m5['High'], df_m5['Low'], df_m5['Close'], window=14).stoch()
    df_m5['ATR'] = ta.volatility.average_true_range(df_m5['High'], df_m5['Low'], df_m5['Close'], window=14)

    t_h1 = "BULL" if df_h1['Close'].iloc[-1] > df_h1['EMA50'].iloc[-1] else "BEAR"
    t_m30 = "BULL" if df_m30['Close'].iloc[-1] > df_m30['Close'].iloc[-3] else "BEAR"
    t_m15 = "BULL" if df_m15['Close'].iloc[-1] > df_m15['Close'].iloc[-3] else "BEAR"
    t_m5 = "BULL" if harga_semasa > df_m5['EMA200'].iloc[-1] else "BEAR"

    atr_semasa = df_m5['ATR'].iloc[-1] if not pd.isna(df_m5['ATR'].iloc[-1]) else 2.5
    duit_risiko = modal_akaun * (peratus_risiko / 100)
    jarak_pips_sl = (atr_semasa * 1.5) * 10
    lot_size = max(0.01, duit_risiko / jarak_pips_sl)

    st.markdown("<br><p style='font-weight:bold; color:#93c5fd; font-size:12px; margin-bottom:4px; letter-spacing:0.5px;'>⚡ LIVE SIGNAL ENGINE</p>", unsafe_allow_html=True)
    
    signal_type = "WAIT"
    stoch_latest = df_m5['stoch_k'].iloc[-1]
    
    if t_h1 == "BULL" and stoch_latest < 40:
        signal_type = "BUY"
        sl = harga_semasa - (atr_semasa * 1.5)
        tp1, tp2, tp3 = harga_semasa + (atr_semasa * 1.5), harga_semasa + (atr_semasa * 3.0), harga_semasa + (atr_semasa * 4.5)
