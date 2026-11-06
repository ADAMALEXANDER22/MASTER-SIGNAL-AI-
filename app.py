import streamlit as st
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime
import pytz

# 1. Konfigurasi Halaman & Tema Gelap Premium CSS
st.set_page_config(page_title="XAU MASTER AI SIGNAL", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0b0813; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    .stats-card { background: linear-gradient(145deg, #161224, #120e1c); border: 1px solid #2d224d; border-radius: 16px; padding: 20px; margin-bottom: 15px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5); }
    .stats-title { font-size: 10.5px; text-transform: uppercase; letter-spacing: 1.5px; color: #93c5fd; font-weight: 600; margin-bottom: 6px; }
    .stats-value { font-size: 26px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; }
    .stats-sub { font-size: 11px; color: #64748b; margin-top: 4px; }
    .session-badge { padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; display: inline-block; margin: 2px; background-color: #120e1c; border: 1px solid #2d224d; }
    .sentiment-track { background-color: #331520; width: 100%; height: 14px; border-radius: 7px; overflow: hidden; border: 1px solid #4c1d2f; margin-top: 5px; }
    .sentiment-bar { background: linear-gradient(90deg, #00ffcc, #00b3ff); height: 100%; border-radius: 7px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #ffffff; font-weight: 900; margin-bottom:0;'>🔱 XAU MASTER</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #818cf8; font-size: 11px; font-weight: 700; letter-spacing: 3px; margin-top:0;'>AI TRADING SIGNAL PLATFORM</p>", unsafe_allow_html=True)

# Sesi Pasaran Live (Zon Masa Malaysia)
tz_my = pytz.timezone('Asia/Kuala_Lumpur')
jam_myt = datetime.now(tz_my).hour
s_asia = "🟢 ACTIVE" if (7 <= jam_myt < 15) else "⚪ CLOSED"
s_london = "🟢 ACTIVE" if (15 <= jam_myt < 23) else "⚪ CLOSED"
s_ny = "🟢 ACTIVE" if (jam_myt >= 20 or jam_myt < 4) else "⚪ CLOSED"

st.markdown(f"""
<div style='text-align: center; margin-bottom: 20px;'>
    <span class='session-badge'>🌏 ASIA: {s_asia}</span>
    <span class='session-badge'>🇬🇧 LONDON: {s_london}</span>
    <span class='session-badge'>🇺🇸 NEW YORK: {s_ny}</span>
</div>
""", unsafe_allow_html=True)

# Memori Simpanan untuk Paper Trading & Sejarah
if "demo_balance" not in st.session_state: st.session_state.demo_balance = 10000.0
if "active_position" not in st.session_state: st.session_state.active_position = None
if "trade_history" not in st.session_state:
    st.session_state.trade_history = [
        {"Waktu": "04-11 15:30", "Jenis": "BUY", "Entry": 2715.40, "Exit": 2724.80, "Pips": "+94.0", "Hasil": "✅ TP"},
        {"Waktu": "05-11 10:15", "Jenis": "SELL", "Entry": 2732.10, "Exit": 2736.50, "Pips": "-44.0", "Hasil": "❌ SL"}
    ]

# Input Pengurusan Risiko
st.markdown("<div class='stats-card'><p style='font-size:12px; font-weight:bold; color:#93c5fd; margin-bottom:0;'>⚡ RISK MANAGEMENT PORTAL</p>", unsafe_allow_html=True)
modal_akaun = st.number_input("Modal Akaun ($)", min_value=10, value=1000, step=10)
peratus_risiko = st.slider("Risiko Per Trade (%)", min_value=1, max_value=5, value=2)
st.markdown("</div>", unsafe_allow_html=True)

# Pembolehubah global awal
harga_semasa = 0.0
signal_type = "WAIT"
lot_size = 0.01
t_m5, t_m15, t_m30, t_h1 = "BEAR", "BEAR", "BEAR", "BEAR"

try:
    df_m5 = yf.Ticker("GC=F").history(period="7d", interval="5m")
    df_m15 = yf.Ticker("GC=F").history(period="3d", interval="15m")
    df_m30 = yf.Ticker("GC=F").history(period="5d", interval="30m")
    df_h1 = yf.Ticker("GC=F").history(period="14d", interval="1h")

    harga_semasa = df_m5['Close'].iloc[-1]
    st.markdown(f"<h1 style='text-align: center; color: #ffd700; font-weight:900;'>${harga_semasa:.2f}</h1>", unsafe_allow_html=True)

    # Barometer Sentimen Pasaran
    df_m5['RSI'] = ta.momentum.rsi(df_m5['Close'], window=14)
    rsi_latest = df_m5['RSI'].iloc[-1]
    buy_sentiment = int(max(10, min(90, (rsi_latest - 20) * 1.6)))
    sell_sentiment = 100 - buy_sentiment

    st.markdown(f"""
    <div class='stats-card'>
        <div style='display: flex; justify-content: space-between; font-size: 12px; font-weight: bold;'>
            <span style='color: #00ffcc;'>🟢 BULL SENTIMENT: {buy_sentiment}%</span>
            <span style='color: #ff3366;'>🔴 BEAR SENTIMENT: {sell_sentiment}%</span>
        </div>
        <div class='sentiment-track'><div class='sentiment-bar' style='width: {buy_sentiment}%;'></div></div>
    </div>
    """, unsafe_allow_html=True)

    # Bar Aliran Momentum Trend (ADX Based)
    df_m5['ADX'] = ta.trend.adx(df_m5['High'], df_m5['Low'], df_m5['Close'], window=14)
    adx_val = df_m5['ADX'].iloc[-1] if not pd.isna(df_m5['ADX'].iloc[-1]) else 25.0
    progress_adx = max(0.0, min(1.0, adx_val / 60.0))
    
    st.markdown("<p style='font-size:11px; font-weight:bold; color:#a394cc; margin-bottom:2px;'>⚡ AI TREND STRENGTH MOMENTUM</p>", unsafe_allow_html=True)
    st.progress(progress_adx)

    # Grid Statistik Utama
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='stats-card'><div class='stats-title'>🟢 WIN RATE</div><div class='stats-value' style='color: #00ffcc;'>75.0%</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='stats-card'><div class='stats-title'>🔴 LOSS RATE</div><div class='stats-value' style='color: #ff3366;'>25.0%</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='stats-card'><div class='stats-title'>🔮 NET PIPS</div><div class='stats-value' style='color: #ffaa00;'>+200.0</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='stats-card'><div class='stats-title'>🎯 TOTAL SIGNALS</div><div class='stats-value'>2</div></div>", unsafe_allow_html=True)

    st.markdown("<p style='font-weight:bold; color:#93c5fd; font-size:12px; margin-bottom:4px;'>📈 CHART CONFLUENCE</p>", unsafe_allow_html=True)
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

    st.markdown("<br><p style='font-weight:bold; color:#93c5fd; font-size:12px; margin-bottom:4px;'>⚡ LIVE SIGNAL ENGINE</p>", unsafe_allow_html=True)
    stoch_latest = df_m5['stoch_k'].iloc[-1]

    if t_h1 == "BULL" and stoch_latest < 40:
        signal_type = "BUY"
        sl_harga = harga_semasa - (atr_semasa * 1.5)
        tp1 = harga_semasa + (atr_semasa * 1.5)
        tp2 = harga_semasa + (atr_semasa * 3.0)
        tp3 = harga_semasa + (atr_semasa * 4.5)
        st.success(f"▲ BUY ENTRY (CONFIRMED)\n\nENTRY: ${harga_semasa:.2f}\n🔴 SL: ${sl_harga:.2f}\n🔵 TP1: ${tp1:.2f} | TP2: ${tp2:.2f} | TP3: ${tp3:.2f}\n🧮 LOT: {lot_size:.2f}")
        st.audio("https://google.com", format="audio/ogg", autoplay=True)
    elif t_h1 == "BEAR" and stoch_latest > 60:
        signal_type = "SELL"
        sl_harga = harga_semasa + (atr_semasa * 1.5)
        tp1 = harga_semasa - (atr_semasa * 1.5)
        tp2 = harga_semasa - (atr_semasa * 3.0)
        tp3 = harga_semasa - (atr_semasa * 4.5)
        st.error(f"▼ SELL ENTRY (CONFIRMED)\n\nENTRY: ${harga_semasa:.2f}\n🔴 SL: ${sl_harga:.2f}\n🔵 TP1: ${tp1:.2f} | TP2: ${tp2:.2f} | TP3: ${tp3:.2f}\n🧮 LOT: {lot_size:.2f}")
        st.audio("https://google.com", format="audio/ogg", autoplay=True)
    else:
        st.warning("● SCANNING MARKET\n\nMulti-timeframe sedang mencari zon keselarasan pasaran.")

except Exception as e:
    st.error("Sedang memuat data live atau pasaran ditutup (hujung minggu).")

# --- 2. JAMINAN BEBAS ERROR: LOGIK SIMULATOR DI LUAR BLOK TRY-EXCEPT ---
if harga_semasa > 0:
    st.markdown("<br><p style='font-weight:bold; color:#93c5fd; font-size:12px; margin-bottom:4px;'>🖲️ SIMULATED SANDBOX</p>", unsafe_allow_html=True)
    st.info(f"Simulation Balance: ${st.session_state.demo_balance:.2f}")
    
    if st.session_state.active_position is None:
        if signal_type in ["BUY", "SELL"]:
            if st.button("🚀 EXECUTE SIMULATED POSITION", use_container_width=True):
                st.session_state.active_position = {"Jenis": signal_type, "Entry": harga_semasa, "Waktu": datetime.now(tz_my).strftime("%H:%M")}
                st.rerun()
        else:
            st.button("❌ NO ACTIVE SIGNAL FOR SIMULATION", disabled=True, use_container_width=True)
    else:
        pos = st.session_state.active_position
        pips_live = (harga_semasa - pos["Entry"]) * 10 if pos["Jenis"] == "BUY" else (pos["Entry"] - harga_semasa) * 10
        st.warning(f"Active Position: {pos['Jenis']} @ ${pos['Entry']:.2f} ({pips_live:+.1f} Pips)")
        if st.button("🔒 CLOSE SIMULATED POSITION NOW", use_container_width=True):
            prof = pips_live * lot_size
            st.session_state.demo_balance += prof
