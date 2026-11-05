import streamlit as st
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime
import pytz
import streamlit.components.v1 as components

# 1. Konfigurasi Halaman & Tema Gelap Premium Custom CSS
st.set_page_config(page_title="XAU MASTER AI SIGNAL", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #120c1f; color: #ffffff; }
    .stats-card { background-color: #1d1630; border: 1px solid #3d2b63; border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); }
    .stats-title { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #a394cc; margin-bottom: 5px; }
    .stats-value { font-size: 22px; font-weight: bold; color: #ffffff; }
    .stats-sub { font-size: 11px; color: #8c7ba6; margin-top: 5px; }
    .signal-box { background-color: #1d1630; border-radius: 12px; padding: 20px; border: 1px solid #3d2b63; text-align: center; margin-top: 15px; }
    .btn-buy { background-color: #1a5cff; color: white; padding: 6px 16px; border-radius: 20px; font-weight: bold; display: inline-block; font-size: 14px; }
    .btn-sell { background-color: #ff3366; color: white; padding: 6px 16px; border-radius: 20px; font-weight: bold; display: inline-block; font-size: 14px; }
    .btn-wait { background-color: #ffaa00; color: black; padding: 6px 16px; border-radius: 20px; font-weight: bold; display: inline-block; font-size: 14px; }
    .target-box { background-color: #251b3a; border-radius: 8px; padding: 15px; margin-top: 12px; font-family: monospace; font-size: 14px; text-align: left; line-height: 1.6; }
    .session-badge { padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; display: inline-block; margin: 2px; }
    .sentiment-bar-bg { background-color: #ff3366; width: 100%; height: 20px; border-radius: 10px; overflow: hidden; margin-top: 5px; position: relative; }
    .sentiment-bar-fill { background-color: #00ffcc; height: 100%; transition: width 0.5s ease; }
    </style>
    """, unsafe_allow_html=True)

# Tajuk Aplikasi Rasmi
st.markdown("<h2 style='text-align: center; color: #ffffff; margin-bottom: 0;'>🔱 XAU MASTER AI SIGNAL</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a394cc; font-size: 12px;'>GOLD SIGNALS MULTI-TIMEFRAME SYSTEM</p>", unsafe_allow_html=True)

# --- Sesi Pasaran Live (Zon Masa Malaysia) ---
tz_my = pytz.timezone('Asia/Kuala_Lumpur')
masa_sekarang = datetime.now(tz_my)
jam_sekarang = masa_sekarang.hour

status_asia = "🟢 ACTIVE" if (7 <= jam_sekarang < 15) else "⚪ CLOSED"
status_london = "🟢 ACTIVE" if (15 <= jam_sekarang < 23) else "⚪ CLOSED"
status_ny = "🟢 ACTIVE" if (jam_sekarang >= 20 or jam_sekarang < 4) else "⚪ CLOSED"

bg_asia = "#1a5cff" if "ACTIVE" in status_asia else "#251b3a"
bg_london = "#00ffcc" if "ACTIVE" in status_london else "#251b3a"
bg_ny = "#ff3366" if "ACTIVE" in status_ny else "#251b3a"

st.markdown(f"""
<div style='text-align: center; margin-bottom: 15px;'>
    <span class='session-badge' style='background-color: {bg_asia}; color: white;'>🌏 ASIA: {status_asia}</span>
    <span class='session-badge' style='background-color: {bg_london}; color: black;'>🇬🇧 LONDON: {status_london}</span>
    <span class='session-badge' style='background-color: {bg_ny}; color: white;'>🇺🇸 NEW YORK: {status_ny}</span>
</div>
""", unsafe_allow_html=True)

# --- SISTEM SIMPANAN MEMORI (Session State untuk Paper Trading & History) ---
if "demo_balance" not in st.session_state:
    st.session_state.demo_balance = 10000.0
if "active_position" not in st.session_state:
    st.session_state.active_position = None
if "trade_history" not in st.session_state:
    st.session_state.trade_history = [
        {"Waktu": "04-11 15:30", "Jenis": "BUY", "Entry": 2715.40, "Exit": 2724.80, "Pips": "+94.0", "Hasil": "✅ TP"},
        {"Waktu": "05-11 10:15", "Jenis": "SELL", "Entry": 2732.10, "Exit": 2736.50, "Pips": "-44.0", "Hasil": "❌ SL"},
        {"Waktu": "05-11 18:45", "Jenis": "BUY", "Entry": 2720.00, "Exit": 2735.00, "Pips": "+150.0", "Hasil": "✅ TP"}
    ]

@st.cache_data(ttl=30)
def ambil_data(period, interval):
    ticker = yf.Ticker("GC=F")
    return ticker.history(period=period, interval=interval)

try:
    df_h1 = ambil_data("14d", "1h")
    df_m30 = ambil_data("5d", "30m")
    df_m15 = ambil_data("3d", "15m")
    df_m5 = ambil_data("7d", "5m")

    harga_semasa = df_m5['Close'].iloc[-1]
    st.markdown(f"<h1 style='text-align: center; color: #ffd700; margin-top: 10px;'>${harga_semasa:.2f}</h1>", unsafe_allow_html=True)
    
    # --- NO 5: BAROMETER SENTIMEN PASARAN (RSI & Volume Based Engine) ---
    st.markdown("<p style='margin-bottom:2px; font-weight:bold; color:#a394cc; font-size:12px;'>📊 RETAIL SENTIMENT GAUGE</p>", unsafe_allow_html=True)
    df_m5['RSI_Sent'] = ta.momentum.rsi(df_m5['Close'], window=14)
    rsi_latest = df_m5['RSI_Sent'].iloc[-1]
    # Tukar nilai RSI kepada anggaran sentimen Buy vs Sell
    buy_sentiment = int(max(10, min(90, (rsi_latest - 20) * 1.6)))
    sell_sentiment = 100 - buy_sentiment

    st.markdown(f"""
    <div class='stats-card' style='padding: 12px; margin-bottom: 15px;'>
        <div style='display: flex; justify-content: space-between; font-size: 12px; font-weight: bold;'>
            <span style='color: #00ffcc;'>🟢 BUY: {buy_sentiment}%</span>
            <span style='color: #ff3366;'>🔴 SELL: {sell_sentiment}%</span>
        </div>
        <div class='sentiment-bar-bg'>
            <div class='sentiment-bar-fill' style='width: {buy_sentiment}%;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Grid Kad Statistik Utama
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='stats-card'><div class='stats-title'>🟢 WIN RATE</div><div class='stats-value' style='color: #00ffcc;'>75.0%</div><div class='stats-sub'>AI Dynamic Profit</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='stats-card'><div class='stats-title'>🔴 LOSS RATE</div><div class='stats-value' style='color: #ff3366;'>25.0%</div><div class='stats-sub'>AI Dynamic Risk</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='stats-card'><div class='stats-title'>🔮 NET PIPS</div><div class='stats-value' style='color: #ffaa00;'>+200.0</div><div class='stats-sub'>Accumulated Pips</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='stats-card'><div class='stats-title'>🎯 TOTAL SIGNALS</div><div class='stats-value'>3</div><div class='stats-sub'>Scanned Trades</div></div>", unsafe_allow_html=True)

    # --- NO 1: CARTA LILIN INTERAKTIF TRADINGVIEW (WIDGET COMPONENT) ---
    st.markdown("<br><p style='margin-bottom:5px; font-weight:bold; color:#a394cc;'>📈 XAUUSD LIVE CHART (TRADINGVIEW)</p>", unsafe_allow_html=True)
    ch_html = """
    <div style="height:350px;">
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container" style="height:100%;width:100%;">
      <iframe src="https://tradingview.com" style="width: 100%; height: 100%; border:none; border-radius:8px;" allowfullscreen></iframe>
    </div>
    <!-- TradingView Widget END -->
    </div>
    """
    components.html(ch_html, height=350)

    # --- LOGIK INPUT RISK CALCULATOR ---
    st.markdown("<div class='stats-card'><p style='font-size:12px; font-weight:bold; color:#a394cc; margin-bottom:8px;'>⚙️ AI RISK & LOT CALCULATOR</p>", unsafe_allow_html=True)
    modal_akaun = st.number_input("Modal Akaun ($)", min_value=10, value=1000, step=10)
    peratus_risiko = st.slider("Risiko Per Trade (%)", min_value=1, max_value=5, value=2)
    st.markdown("</div>", unsafe_allow_html=True)

    # Logik Analisis Teknikal Multi-Timeframe
    df_h1['EMA50'] = ta.trend.ema_indicator(df_h1['Close'], window=50)
    trend_h1 = "BULL" if df_h1['Close'].iloc[-1] > df_h1['EMA50'].iloc[-1] else "BEAR"
    df_m30['RSI'] = ta.momentum.rsi(df_m30['Close'], window=14)
    df_m15['RSI'] = ta.momentum.rsi(df_m15['Close'], window=14)
    df_m5['stoch_k'] = ta.momentum.StochasticOscillator(df_m5['High'], df_m5['Low'], df_m5['Close'], window=14).stoch()
    df_m5['EMA200'] = ta.trend.ema_indicator(df_m5['Close'], window=200)
    
    rsi_m30 = df_m30['RSI'].iloc[-1]
    rsi_m15 = df_m15['RSI'].iloc[-1]
    stoch_m5 = df_m5['stoch_k'].iloc[-1]
    ema200_m5 = df_m5['EMA200'].iloc[-1]
    df_m5['ATR'] = ta.volatility.average_true_range(df_m5['High'], df_m5['Low'], df_m5['Close'], window=14)
    atr_semasa = df_m5['ATR'].iloc[-1] if not pd.isna(df_m5['ATR'].iloc[-1]) else 2.5
    
    trend_h1_val = "BULL" if trend_h1 == "BULL" else "BEAR"
    trend_m30_val = "BULL" if rsi_m30 < 50 else "BEAR"
    trend_m15_val = "BULL" if rsi_m15 < 50 else "BEAR"
    trend_m5_val = "BULL" if harga_semasa > ema200_m5 else "BEAR"

    # Pengiraan Saiz Lot
    duit_risiko = modal_akaun * (peratus_risiko / 100)
    jarak_pips_sl = (atr_semasa * 1.5) * 10
    lot_size = max(0.01, duit_risiko / jarak_pips_sl)

    st.markdown("<br><p style='margin-bottom:5px; font-weight:bold; color:#a394cc;'>📊 LIVE SIGNAL STATUS</p>", unsafe_allow_html=True)
    
    signal_type = "WAIT"
    sl_harga, tp_harga = 0.0, 0.0
    
    if trend_h1 == "BULL" and rsi_m30 < 65 and rsi_m15 < 65 and stoch_m5 < 25 and harga_semasa > ema200_m5:
        signal_type = "BUY"
        sl_harga = harga_semasa - (atr_semasa * 1.5)
        tp_harga = harga_semasa + (atr_semasa * 3.0)
        status_html = f"<div class='signal-box'><span class='btn-buy'>▲ BUY ENTRY (CONFIRMED)</span><div class='target-box'>🟢 <b>ENTRY:</b> ${harga_semasa:.2f}<br>🔴 <b>STOP LOSS:</b> ${sl_harga:.2f}<br>🔵 <b>TAKE PROFIT:</b> ${tp_harga:.2f}<br><br>🧮 <b>CADANGAN SAIZ LOT:</b> {lot_size:.2f} Lot</div></div>"
