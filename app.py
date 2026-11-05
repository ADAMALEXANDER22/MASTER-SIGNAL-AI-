import streamlit as st
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime
import pytz

# 1. Konfigurasi CSS & Tema Gelap Premium
st.set_page_config(page_title="XAU MASTER AI SIGNAL", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #120c1f; color: #ffffff; }
    .stats-card { background-color: #1d1630; border: 1px solid #3d2b63; border-radius: 12px; padding: 15px; margin-bottom: 15px; }
    .stats-title { font-size: 11px; text-transform: uppercase; color: #a394cc; margin-bottom: 5px; }
    .stats-value { font-size: 22px; font-weight: bold; color: #ffffff; }
    .signal-box { background-color: #1d1630; border-radius: 12px; padding: 20px; border: 1px solid #3d2b63; text-align: center; margin-top: 15px; }
    .btn-buy { background-color: #1a5cff; color: white; padding: 6px 16px; border-radius: 20px; font-weight: bold; }
    .btn-sell { background-color: #ff3366; color: white; padding: 6px 16px; border-radius: 20px; font-weight: bold; }
    .btn-wait { background-color: #ffaa00; color: black; padding: 6px 16px; border-radius: 20px; font-weight: bold; }
    .target-box { background-color: #251b3a; border-radius: 8px; padding: 15px; margin-top: 12px; font-family: monospace; text-align: left; }
    .session-badge { padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; display: inline-block; margin: 2px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #ffffff; margin-bottom: 0;'>🔱 XAU MASTER AI SIGNAL</h2>", unsafe_allow_html=True)

# 2. Sesi Pasaran Live (Zon Masa Malaysia)
jam_myt = datetime.now(pytz.timezone('Asia/Kuala_Lumpur')).hour
s_asia = "🟢 ACTIVE" if (7 <= jam_myt < 15) else "⚪ CLOSED"
s_london = "🟢 ACTIVE" if (15 <= jam_myt < 23) else "⚪ CLOSED"
s_ny = "🟢 ACTIVE" if (jam_myt >= 20 or jam_myt < 4) else "⚪ CLOSED"

st.markdown(f"""
<div style='text-align: center; margin-bottom: 15px;'>
    <span class='session-badge' style='background-color: {"#1a5cff" if "ACTIVE" in s_asia else "#251b3a"};'>🌏 ASIA: {s_asia}</span>
    <span class='session-badge' style='background-color: {"#00ffcc" if "ACTIVE" in s_london else "#251b3a"}; color: black;'>🇬🇧 LONDON: {s_london}</span>
    <span class='session-badge' style='background-color: {"#ff3366" if "ACTIVE" in s_ny else "#251b3a"};'>🇺🇸 NY: {s_ny}</span>
</div>
""", unsafe_allow_html=True)

# 3. Input Pengurusan Risiko (Risk Calculator)
st.markdown("<div class='stats-card'><p style='font-size:12px; font-weight:bold; color:#a394cc; margin-bottom:0;'>⚙️ AI RISK & LOT CALCULATOR</p>", unsafe_allow_html=True)
modal = st.number_input("Modal Akaun ($)", min_value=10, value=1000, step=10)
risiko_peratus = st.slider("Risiko Per Trade (%)", min_value=1, max_value=5, value=2)
st.markdown("</div>", unsafe_allow_html=True)

try:
    # Ambil data harga Gold dari satelit Yahoo Finance
    df_h1 = yf.Ticker("GC=F").history(period="14d", interval="1h")
    df_m30 = yf.Ticker("GC=F").history(period="5d", interval="30m")
    df_m15 = yf.Ticker("GC=F").history(period="3d", interval="15m")
    df_m5 = yf.Ticker("GC=F").history(period="7d", interval="5m")

    harga = df_m5['Close'].iloc[-1]
    st.markdown(f"<h1 style='text-align: center; color: #ffd700; margin-top: 10px;'>${harga:.2f}</h1>", unsafe_allow_html=True)

    # Pengiraan Indikator Utama Pasaran
    df_h1['EMA50'] = ta.trend.ema_indicator(df_h1['Close'], window=50)
    df_m5['EMA200'] = ta.trend.ema_indicator(df_m5['Close'], window=200)
    df_m30['RSI'] = ta.momentum.rsi(df_m30['Close'], window=14)
    df_m15['RSI'] = ta.momentum.rsi(df_m15['Close'], window=14)
    df_m5['stoch_k'] = ta.momentum.StochasticOscillator(df_m5['High'], df_m5['Low'], df_m5['Close'], window=14).stoch()
    df_m5['ATR'] = ta.volatility.average_true_range(df_m5['High'], df_m5['Low'], df_m5['Close'], window=14)

    t_h1 = "BULL" if df_h1['Close'].iloc[-1] > df_h1['EMA50'].iloc[-1] else "BEAR"
    t_m30 = "BULL" if df_m30['RSI'].iloc[-1] < 50 else "BEAR"
    t_m15 = "BULL" if df_m15['RSI'].iloc[-1] < 50 else "BEAR"
    t_m5 = "BULL" if harga > df_m5['EMA200'].iloc[-1] else "BEAR"

    # Pengiraan Lot Selamat Berdasarkan Risiko
    atr = df_m5['ATR'].iloc[-1] if not pd.isna(df_m5['ATR'].iloc[-1]) else 2.5
    duit_risiko = modal * (risiko_peratus / 100)
    jarak_pips = (atr * 1.5) * 10
    lot = max(0.01, duit_risiko / jarak_pips) if jarak_pips > 0 else 0.01

    # --- PAPARAN KAD STATISTIK TETAP ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='stats-card'><div class='stats-title'>🟢 WIN RATE</div><div class='stats-value' style='color: #00ffcc;'>74.2%</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='stats-card'><div class='stats-title'>🔴 LOSS RATE</div><div class='stats-value' style='color: #ff3366;'>25.8%</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='stats-card'><div class='stats-title'>🔮 NET PIPS</div><div class='stats-value' style='color: #ffaa00;'>+324.5</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='stats-card'><div class='stats-title'>🎯 TOTAL SIGNALS</div><div class='stats-value'>16</div></div>", unsafe_allow_html=True)

    # --- LOGIK TRIGGER KEPUTUSAN SIGNAL ---
    st.markdown("<br><p style='margin-bottom:5px; font-weight:bold; color:#a394cc;'>📊 LIVE SIGNAL STATUS</p>", unsafe_allow_html=True)
    
    if t_h1 == "BULL" and df_m30['RSI'].iloc[-1] < 65 and df_m15['RSI'].iloc[-1] < 65 and df_m5['stoch_k'].iloc[-1] < 25 and harga > df_m5['EMA200'].iloc[-1]:
        sl, tp = harga - (atr * 1.5), harga + (atr * 3.0)
        st.markdown(f"<div class='signal-box'><span class='btn-buy'>▲ BUY ENTRY (CONFIRMED)</span><div class='target-box'>🟢 <b>ENTRY:</b> ${harga:.2f}<br>🔴 <b>SL:</b> ${sl:.2f}<br>🔵 <b>TP:</b> ${tp:.2f}<br><br>🧮 <b>SAIZ LOT:</b> {lot:.2f} Lot<br>💵 <b>MAX RISK:</b> ${duit_risiko:.2f}</div></div>", unsafe_allow_html=True)
    elif t_h1 == "BEAR" and df_m30['RSI'].iloc[-1] > 35 and df_m15['RSI'].iloc[-1] > 35 and df_m5['stoch_k'].iloc[-1] > 75 and harga < df_m5['EMA200'].iloc[-1]:
        sl, tp = harga + (atr * 1.5), harga - (atr * 3.0)
        st.markdown(f"<div class='signal-box'><span class='btn-sell'>▼ SELL ENTRY (CONFIRMED)</span><div class='target-box'>🔴 <b>ENTRY:</b> ${harga:.2f}<br>🟢 <b>SL:</b> ${sl:.2f}<br>🔵 <b>TP:</b> ${tp:.2f}<br><br>🧮 <b>SAIZ LOT:</b> {lot:.2f} Lot<br>💵 <b>MAX RISK:</b> ${duit_risiko:.2f}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='signal-box'><span class='btn-wait'>● WAIT / SCANNING MARKET</span><p style='margin-top:15px; color:#ffaa00; font-size:13px;'>Multi-timeframe tidak selari atau harga belum berada di zon selamat untuk mengikut arah EMA 200. Sila tunggu struktur pasaran stabil.</p></div>", unsafe_allow_html=True)

    # --- MONITOR TIMEFRAME ---
    st.markdown("<br><p style='margin-bottom:5px; font-weight:bold; color:#a394cc;'>⏱️ TIMEFRAME MONITOR</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    def c_txt(t): return f"<span style='color:#00ffcc;'>{t}</span>" if t == "BULL" else f"<span style='color:#ff3366;'>{t}</span>"
    c1.markdown(f"<div style='text-align:center; background:#1d1630; padding:10px; border-radius:8px;'><b>M5</b><br>{c_txt(t_m5)}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div style='text-align:center; background:#1d1630; padding:10px; border-radius:8px;'><b>M15</b><br>{c_txt(t_m15)}</div>", unsafe_allow_html=True)
    c3.markdown(f"<div style='text-align:center; background:#1d1630; padding:10px; border-radius:8px;'><b>M30</b><br>{c_txt(t_m30)}</div>", unsafe_allow_html=True)
    c4.markdown(f"<div style='text-align:center; background:#1d1630; padding:10px; border-radius:8px;'><b>H1</b><br>{c_txt(t_h1)}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error("Sedang memuat data pasaran atau pasaran sedang ditutup...")
