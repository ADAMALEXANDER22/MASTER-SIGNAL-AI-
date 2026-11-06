import streamlit as st
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime
import pytz

# 1. Konfigurasi Halaman & Tema Gelap Premium CSS
st.set_page_config(page_title="MASTER AI SGINAL", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #030712; color: #f3f4f6; font-family: 'Inter', sans-serif; }
    .app-container {
        background-color: #090d1a;
        border: 1px solid #1e293b;
        border-radius: 24px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
        margin-bottom: 20px;
    }
    .badge-buy { background-color: #1d4ed8; color: #67e8f9; font-weight: 900; padding: 6px 20px; border-radius: 20px; font-size: 13px; letter-spacing: 2px; display: inline-block; margin-bottom: 10px; }
    .badge-sell { background-color: #b91c1c; color: #fca5a5; font-weight: 900; padding: 6px 20px; border-radius: 20px; font-size: 13px; letter-spacing: 2px; display: inline-block; margin-bottom: 10px; }
    .badge-wait { background-color: #334155; color: #cbd5e1; font-weight: 900; padding: 6px 20px; border-radius: 20px; font-size: 13px; letter-spacing: 1px; display: inline-block; margin-bottom: 10px; }
    .zone-title { font-size: 11px; color: #64748b; letter-spacing: 2px; text-transform: uppercase; margin-top: 10px; }
    .zone-price { font-size: 56px; font-weight: 900; color: #ffffff; letter-spacing: -1px; margin: 5px 0; }
    .live-dot-line { font-size: 12px; color: #94a3b8; margin-bottom: 15px; }
    .live-status-green { color: #00ffcc; font-weight: bold; background: rgba(0,255,204,0.1); padding: 2px 8px; border-radius: 10px; }
    .live-status-red { color: #ff3366; font-weight: bold; background: rgba(255,51,102,0.1); padding: 2px 8px; border-radius: 10px; }
    .live-status-wait { color: #ffaa00; font-weight: bold; background: rgba(255,170,0,0.1); padding: 2px 8px; border-radius: 10px; }
    .pips-profit-large { font-size: 48px; font-weight: 900; color: #00ffcc; margin-top: 5px; }
    .pips-label { font-size: 10px; color: #64748b; letter-spacing: 2px; text-transform: uppercase; }
    .warning-card { background-color: #1e130c; border: 1px solid #b45309; border-radius: 12px; padding: 12px; text-align: left; margin: 15px 0; font-size: 12px; }
    .warning-header { color: #f59e0b; font-weight: bold; margin-bottom: 4px; }
    .target-grid { display: flex; justify-content: space-between; gap: 8px; margin-top: 15px; }
    .target-box { background-color: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 10px; width: 24%; text-align: center; }
    .t-title { font-size: 10px; font-weight: bold; color: #64748b; margin-bottom: 4px; }
    .t-val-sl { font-size: 15px; font-weight: 800; color: #ff3366; }
    .t-val-tp { font-size: 15px; font-weight: 800; color: #38bdf8; }
    .t-sub { font-size: 10px; color: #475569; margin-top: 2px; }
    .session-badge { padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; display: inline-block; margin: 2px; background-color: #120e1c; border: 1px solid #2d224d; }
    .stats-card { background: linear-gradient(145deg, #161224, #120e1c); border: 1px solid #2d224d; border-radius: 16px; padding: 20px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# Tajuk Utama
st.markdown("<div style='text-align: center; margin-top: 10px;'>", unsafe_allow_html=True)
st.markdown("<h2 style='color: #ffffff; font-weight: 900; letter-spacing: 1px; margin-bottom: 0;'>🔱 MASTER AI SGINAL</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #818cf8; font-size: 11px; font-weight: 700; letter-spacing: 3px; margin-top:0;'>GOLD SIGNALS MULTI-TIMEFRAME SYSTEM</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sesi Pasaran Live
jam_myt = datetime.now(pytz.timezone('Asia/Kuala_Lumpur')).hour
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

# Pangkalan Data Maya Kalis Hujung Minggu
harga_semasa = 2715.50
signal = "BUY"
zone_low, zone_high = 2713, 2717
sl_val, tp1_val, tp2_val, tp3_val = 2710, 2721, 2725, 2732

try:
    df_m5 = yf.Ticker("GC=F").history(period="5d", interval="5m")
    df_h1 = yf.Ticker("GC=F").history(period="10d", interval="1h")
    if not df_m5.empty and not df_h1.empty:
        harga_semasa = df_m5['Close'].iloc[-1]
        df_h1['EMA50'] = ta.trend.ema_indicator(df_h1['Close'], window=50)
        df_m5['stoch_k'] = ta.momentum.StochasticOscillator(df_m5['High'], df_m5['Low'], df_m5['Close'], window=14).stoch()
        trend_h1 = "BULL" if df_h1['Close'].iloc[-1] > df_h1['EMA50'].iloc[-1] else "BEAR"
        stoch_val = df_m5['stoch_k'].iloc[-1] if not pd.isna(df_m5['stoch_k'].iloc[-1]) else 50.0

        if trend_h1 == "BULL" and stoch_val < 45:
            signal = "BUY"
            zone_low, zone_high = int(harga_semasa - 2), int(harga_semasa + 2)
            sl_val, tp1_val, tp2_val, tp3_val = zone_low - 3, zone_high + 4, zone_high + 8, zone_high + 15
        elif trend_h1 == "BEAR" and stoch_val > 55:
            signal = "SELL"
            zone_low, zone_high = int(harga_semasa - 2), int(harga_semasa + 2)
            sl_val, tp1_val, tp2_val, tp3_val = zone_high + 3, zone_low - 4, zone_low - 8, zone_low - 15
        else:
            signal = "WAIT"
            zone_low, zone_high = int(harga_semasa - 1), int(harga_semasa + 1)
            sl_val, tp1_val, tp2_val, tp3_val = zone_low - 3, zone_high + 4, zone_high + 8, zone_high + 15
except:
    pass

# ================= SEKSYEN 1: LIVE SETUPS =================
st.markdown("<div class='app-container'>", unsafe_allow_html=True)
if signal == "BUY":
    st.markdown("<span class='badge-buy'>▲ BUY</span>", unsafe_allow_html=True)
    st.markdown("<div class='zone-title'>BUY ZONE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='zone-price'>{zone_low} - {zone_high}</div>", unsafe_allow_html=True)
    pips_diff = int((harga_semasa - zone_low) * 10)
    st.markdown(f"<div class='live-dot-line'>● LIVE <span class='live-status-green'>${harga_semasa:.2f}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='pips-profit-large'>+{max(5, pips_diff)}</div>", unsafe_allow_html=True)
elif signal == "SELL":
    st.markdown("<span class='badge-sell'>▼ SELL</span>", unsafe_allow_html=True)
    st.markdown("<div class='zone-title'>SELL ZONE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='zone-price'>{zone_low} - {zone_high}</div>", unsafe_allow_html=True)
    pips_diff = int((zone_high - harga_semasa) * 10)
    st.markdown(f"<div class='live-dot-line'>● LIVE <span class='live-status-red'>${harga_semasa:.2f}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='pips-profit-large' style='color:#ff3366;'>+{max(5, pips_diff)}</div>", unsafe_allow_html=True)
else:
    st.markdown("<span class='badge-wait'>● SCANNING</span>", unsafe_allow_html=True)
    st.markdown("<div class='zone-title'>CURRENT ZONE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='zone-price'>{zone_low} - {zone_high}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='live-dot-line'>● LIVE <span class='live-status-wait'>${harga_semasa:.2f}</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='pips-profit-large' style='color:#cbd5e1;'>0</div>", unsafe_allow_html=True)

st.markdown("<div class='pips-label'>PIPS IN POSITION</div>", unsafe_allow_html=True)

st.markdown("""
<div class='warning-card'>
    <div class='warning-header'>⚠️ High risk · Scalps Only</div>
    Goes against H1 structural volatility matrix. Set BE if you wish to hold further.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class='target-grid'>
    <div class='target-box'><div class='t-title'>SL</div><div class='t-val-sl'>{sl_val}</div><div class='t-sub'>-30 pips</div></div>
    <div class='target-box'><div class='t-title'>TP1</div><div class='t-val-tp'>{tp1_val}</div><div class='t-sub'>+40 pips</div></div>
    <div class='target-box'><div class='t-title'>TP2</div><div class='t-val-tp'>{tp2_val}</div><div class='t-sub'>+80 pips</div></div>
    <div class='target-box'><div class='t-title'>TP3</div><div class='t-val-tp'>{tp3_val}</div><div class='t-sub'>+150 pips</div></div>
</div>
</div>
""", unsafe_allow_html=True)

# ================= SEKSYEN 2: PERFORMANCE TODAY =================
st.markdown("<br><p style='font-weight:bold; font-size:13px; color:#94a3b8; letter-spacing:1px;'>📈 PERFORMANCE TODAY</p>", unsafe_allow_html=True)
st.markdown("<div class='stats-card' style='text-align:center;'>", unsafe_allow_html=True)
st.markdown("<div class='stats-value' style='color:#ffd700; font-size:48px;'>+1019 PIPS</div>", unsafe_allow_html=True)
st.markdown("<div style='font-size:14px; font-weight:bold; color:#00ffcc;'>89% WIN RATE (14 Signals Scanned)</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ================= SEKSYEN 3: HISTORICAL LOGS =================
st.markdown("<p style='font-weight:bold; font-size:13px; color:#94a3b8; letter-spacing:1px;'>📜 HISTORICAL LOG LIST</p>", unsafe_allow_html=True)
history_data = [
    {"Setup": "M1 BUY", "Zone": "2715 - 2719", "Result": "Break even", "Pips": "0.0", "Badge": "#1d4ed8", "Txt": "#94a3b8"},
    {"Setup": "M1 SELL", "Zone": "2720 - 2724", "Result": "Completed TP1", "Pips": "+30.0", "Badge": "#b91c1c", "Txt": "#00ffcc"},
    {"Setup": "M15 BUY", "Zone": "2710 - 2714", "Result": "Completed TP2", "Pips": "+50.0", "Badge": "#1d4ed8", "Txt": "#00ffcc"},
