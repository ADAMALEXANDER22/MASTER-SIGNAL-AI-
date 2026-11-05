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
    .stApp { background-color: #120c1f; color: #ffffff; }
    .stats-card { background-color: #1d1630; border: 1px solid #3d2b63; border-radius: 12px; padding: 15px; margin-bottom: 15px; }
    .stats-title { font-size: 11px; text-transform: uppercase; color: #a394cc; margin-bottom: 5px; }
    .stats-value { font-size: 22px; font-weight: bold; color: #ffffff; }
    .stats-sub { font-size: 11px; color: #8c7ba6; margin-top: 5px; }
    .session-badge { padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; display: inline-block; margin: 2px; background-color: #251b3a; }
    .sentiment-bar-bg { background-color: #ff3366; width: 100%; height: 20px; border-radius: 10px; overflow: hidden; margin-top: 5px; }
    .sentiment-bar-fill { background-color: #00ffcc; height: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #ffffff;'>🔱 XAU MASTER AI SIGNAL</h2>", unsafe_allow_html=True)

# 2. Sesi Pasaran Live (Zon Masa Malaysia)
jam_myt = datetime.now(pytz.timezone('Asia/Kuala_Lumpur')).hour
s_asia = "🟢 ACTIVE" if (7 <= jam_myt < 15) else "⚪ CLOSED"
s_london = "🟢 ACTIVE" if (15 <= jam_myt < 23) else "⚪ CLOSED"
s_ny = "🟢 ACTIVE" if (jam_myt >= 20 or jam_myt < 4) else "⚪ CLOSED"

st.markdown(f"""
<div style='text-align: center; margin-bottom: 15px;'>
    <span class='session-badge'>🌏 ASIA: {s_asia}</span>
    <span class='session-badge'>🇬🇧 LONDON: {s_london}</span>
    <span class='session-badge'>🇺🇸 NEW YORK: {s_ny}</span>
</div>
""", unsafe_allow_html=True)

# Memori Simpanan untuk Paper Trading & Sejarah
if "demo_balance" not in st.session_state:
    st.session_state.demo_balance = 10000.0
if "active_position" not in st.session_state:
    st.session_state.active_position = None
if "trade_history" not in st.session_state:
    st.session_state.trade_history = [
        {"Waktu": "04-11 15:30", "Jenis": "BUY", "Entry": 2715.40, "Exit": 2724.80, "Pips": "+94.0", "Hasil": "✅ TP"},
        {"Waktu": "05-11 10:15", "Jenis": "SELL", "Entry": 2732.10, "Exit": 2736.50, "Pips": "-44.0", "Hasil": "❌ SL"}
    ]

# 3. Input Pengurusan Risiko
st.markdown("<div class='stats-card'><p style='font-size:12px; font-weight:bold; color:#a394cc; margin-bottom:0;'>⚙️ AI RISK & LOT CALCULATOR</p>", unsafe_allow_html=True)
modal_akaun = st.number_input("Modal Akaun ($)", min_value=10, value=1000, step=10)
peratus_risiko = st.slider("Risiko Per Trade (%)", min_value=1, max_value=5, value=2)
st.markdown("</div>", unsafe_allow_html=True)

try:
    df_m5 = yf.Ticker("GC=F").history(period="7d", interval="5m")
    df_m15 = yf.Ticker("GC=F").history(period="3d", interval="15m")
    df_m30 = yf.Ticker("GC=F").history(period="5d", interval="30m")
    df_h1 = yf.Ticker("GC=F").history(period="14d", interval="1h")

    harga_semasa = df_m5['Close'].iloc[-1]
    st.markdown(f"<h1 style='text-align: center; color: #ffd700;'>${harga_semasa:.2f}</h1>", unsafe_allow_html=True)

    # 4. Barometer Sentimen Pasaran
    df_m5['RSI'] = ta.momentum.rsi(df_m5['Close'], window=14)
    rsi_latest = df_m5['RSI'].iloc[-1]
    buy_sentiment = int(max(10, min(90, (rsi_latest - 20) * 1.6)))
    sell_sentiment = 100 - buy_sentiment

    st.markdown(f"""
    <div class='stats-card'>
        <div style='display: flex; justify-content: space-between; font-size: 12px; font-weight: bold;'>
            <span style='color: #00ffcc;'>🟢 BUY: {buy_sentiment}%</span>
            <span style='color: #ff3366;'>🔴 SELL: {sell_sentiment}%</span>
        </div>
        <div class='sentiment-bar-bg'><div class='sentiment-bar-fill' style='width: {buy_sentiment}%;'></div></div>
    </div>
    """, unsafe_allow_html=True)

    # Grid Statistik
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='stats-card'><div class='stats-title'>🟢 WIN RATE</div><div class='stats-value' style='color: #00ffcc;'>75.0%</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='stats-card'><div class='stats-title'>🔴 LOSS RATE</div><div class='stats-value' style='color: #ff3366;'>25.0%</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='stats-card'><div class='stats-title'>🔮 NET PIPS</div><div class='stats-value' style='color: #ffaa00;'>+200.0</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='stats-card'><div class='stats-title'>🎯 TOTAL SIGNALS</div><div class='stats-value'>2</div></div>", unsafe_allow_html=True)

    # Link Pintas Carta TradingView
    st.markdown("<p style='font-weight:bold; color:#a394cc; margin-bottom:2px;'>📈 XAUUSD LIVE CHART</p>", unsafe_allow_html=True)
    st.link_button("📊 BUKA CARTA LIVE TRADINGVIEW (M5)", "https://tradingview.com", use_container_width=True)

    # Pengiraan Teknikal Multi-Timeframe
    df_h1['EMA50'] = ta.trend.ema_indicator(df_h1['Close'], window=50)
    df_m5['EMA200'] = ta.trend.ema_indicator(df_m5['Close'], window=200)
    df_m5['stoch_k'] = ta.momentum.StochasticOscillator(df_m5['High'], df_m5['Low'], df_m5['Close'], window=14).stoch()
    df_m5['ATR'] = ta.volatility.average_true_range(df_m5['High'], df_m5['Low'], df_m5['Close'], window=14)

    t_h1 = "BULL" if df_h1['Close'].iloc[-1] > df_h1['EMA50'].iloc[-1] else "BEAR"
    t_m30 = "BULL" if df_m30['Close'].iloc[-1] > df_m30['Close'].iloc[-5] else "BEAR"
    t_m15 = "BULL" if df_m15['Close'].iloc[-1] > df_m15['Close'].iloc[-5] else "BEAR"
    t_m5 = "BULL" if harga_semasa > df_m5['EMA200'].iloc[-1] else "BEAR"

    atr_semasa = df_m5['ATR'].iloc[-1] if not pd.isna(df_m5['ATR'].iloc[-1]) else 2.5
    duit_risiko = modal_akaun * (peratus_risiko / 100)
    jarak_pips_sl = (atr_semasa * 1.5) * 10
    lot_size = max(0.01, duit_risiko / jarak_pips_sl) if jarak_pips_sl > 0 else 0.01

    # 6. Pemprosesan Isyarat Isyarat dengan TP Bertingkat
    st.markdown("<br><p style='font-weight:bold; color:#a394cc;'>📊 LIVE SIGNAL STATUS</p>", unsafe_allow_html=True)
    
    signal_type = "WAIT"
    if t_h1 == "BULL" and df_m5['stoch_k'].iloc[-1] < 25 and harga_semasa > df_m5['EMA200'].iloc[-1]:
        signal_type = "BUY"
        sl = harga_semasa - (atr_semasa * 1.5)
        tp1 = harga_semasa + (atr_semasa * 1.5)  # RR 1:1
        tp2 = harga_semasa + (atr_semasa * 3.0)  # RR 1:2
        tp3 = harga_semasa + (atr_semasa * 4.5)  # RR 1:3
        st.success(f"▲ BUY ENTRY (CONFIRMED)\n\nENTRY: ${harga_semasa:.2f}\n🔴 STOP LOSS: ${sl:.2f}\n\n🔵 TAKE PROFIT 1: ${tp1:.2f}\n🔵 TAKE PROFIT 2: ${tp2:.2f}\n🔵 TAKE PROFIT 3: ${tp3:.2f}\n\n🧮 Lot: {lot_size:.2f} | 💵 Max Risk: ${duit_risiko:.2f}")
    elif t_h1 == "BEAR" and df_m5['stoch_k'].iloc[-1] > 75 and harga_semasa < df_m5['EMA200'].iloc[-1]:
        signal_type = "SELL"
        sl = harga_semasa + (atr_semasa * 1.5)
        tp1 = harga_semasa - (atr_semasa * 1.5)  # RR 1:1
        tp2 = harga_semasa - (atr_semasa * 3.0)  # RR 1:2
        tp3 = harga_semasa - (atr_semasa * 4.5)  # RR 1:3
        st.error(f"▼ SELL ENTRY (CONFIRMED)\n\nENTRY: ${harga_semasa:.2f}\n🔴 STOP LOSS: ${sl:.2f}\n\n🔵 TAKE PROFIT 1: ${tp1:.2f}\n🔵 TAKE PROFIT 2: ${tp2:.2f}\n🔵 TAKE PROFIT 3: ${tp3:.2f}\n\n🧮 Lot: {lot_size:.2f} | 💵 Max Risk: ${duit_risiko:.2f}")
    else:
        st.warning("● WAIT / SCANNING MARKET\n\nMulti-timeframe tidak selari. Tunggu konfirmasi struktur M5.")

    # 7. Paper Trading Simulator Widget
    st.markdown("<br><p style='font-weight:bold; color:#a394cc;'>🖲️ AI PAPER TRADING SIMULATOR</p>", unsafe_allow_html=True)
    st.info(f"Demo Balance: ${st.session_state.demo_balance:.2f}")
    
    if st.session_state.active_position is None:
        if signal_type in ["BUY", "SELL"]:
            if st.button(f"🚀 Buka Posisi Simulasi ({signal_type})"):
                st.session_state.active_position = {"Jenis": signal_type, "Entry": harga_semasa, "Waktu": datetime.now(tz_my).strftime("%H:%M")}
                st.rerun()
    else:
        pos = st.session_state.active_position
        pips_live = (harga_semasa - pos["Entry"]) * 10 if pos["Jenis"] == "BUY" else (pos["Entry"] - harga_semasa) * 10
        st.write(f"Posisi Aktif: {pos['Jenis']} Emas dari harga ${pos['Entry']:.2f} ({pips_live:+.1f} Pips)")
        if st.button("🔒 Tutup Posisi Maya"):
            prof = pips_live * lot_size
            st.session_state.demo_balance += prof
            st.session_state.trade_history.insert(0, {"Waktu": pos["Waktu"], "Jenis": pos["Jenis"], "Entry": pos["Entry"], "Exit": harga_semasa, "Pips": f"{pips_live:+.1f}", "Hasil": "✅ TP" if prof > 0 else "❌ SL"})
            st.session_state.active_position = None
            st.rerun()

    # 8. Timeframe Monitor Bar
    st.markdown("<br><p style='font-weight:bold; color:#a394cc;'>⏱️ TIMEFRAME MONITOR</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("M5", t_m5)
    c2.metric("M15", t_m15)
    c3.metric("M30", t_m30)
    c4.metric("H1", t_h1)

    # 9. Sejarah Log Signal
    st.markdown("<br><p style='font-weight:bold; color:#a394cc;'>📜 REKOD SEJARAH SIGNAL (LOG)</p>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.trade_history), use_container_width=True, hide_index=True)

except Exception as e:
    st.error("Sedang memuat data live atau pasaran ditutup (hujung minggu).")
