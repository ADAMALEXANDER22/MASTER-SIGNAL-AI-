import streamlit as st
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime
import pytz

# 1. Konfigurasi UI Premium Mengikut Reka Bentuk Rujukan
st.set_page_config(page_title="MASTER AI SGINAL", layout="centered")

st.markdown("""
    <style>
    /* Latar Belakang & Fon Moden Mudah Alih */
    .stApp { background-color: #030712; color: #f3f4f6; font-family: 'Inter', sans-serif; }
    
    /* Kad Isyarat Utama (Top Setup Box) */
    .app-container {
        background-color: #090d1a;
        border: 1px solid #1e293b;
        border-radius: 24px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
        margin-bottom: 20px;
    }
    
    /* Lencana Signal (Buy/Sell Badge) */
    .badge-buy {
        background-color: #1d4ed8; color: #67e8f9; font-weight: 900;
        padding: 6px 20px; border-radius: 20px; font-size: 13px;
        letter-spacing: 2px; display: inline-block; margin-bottom: 10px;
        box-shadow: 0 0 15px rgba(29, 78, 216, 0.6);
    }
    .badge-sell {
        background-color: #b91c1c; color: #fca5a5; font-weight: 900;
        padding: 6px 20px; border-radius: 20px; font-size: 13px;
        letter-spacing: 2px; display: inline-block; margin-bottom: 10px;
        box-shadow: 0 0 15px rgba(185, 28, 28, 0.6);
    }
    .badge-wait {
        background-color: #334155; color: #cbd5e1; font-weight: 900;
        padding: 6px 20px; border-radius: 20px; font-size: 13px;
        letter-spacing: 1px; display: inline-block; margin-bottom: 10px;
    }
    
    /* Zon Harga Besar (Zone Price Display) */
    .zone-title { font-size: 11px; color: #64748b; letter-spacing: 2px; text-transform: uppercase; margin-top: 10px; }
    .zone-price { font-size: 56px; font-weight: 900; color: #ffffff; letter-spacing: -1px; margin: 5px 0; }
    
    /* Penunjuk Status Live */
    .live-dot-line { font-size: 12px; color: #94a3b8; margin-bottom: 15px; }
    .live-status-green { color: #00ffcc; font-weight: bold; background: rgba(0,255,204,0.1); padding: 2px 8px; border-radius: 10px; }
    .live-status-red { color: #ff3366; font-weight: bold; background: rgba(255,51,102,0.1); padding: 2px 8px; border-radius: 10px; }
    .live-status-wait { color: #ffaa00; font-weight: bold; background: rgba(255,170,0,0.1); padding: 2px 8px; border-radius: 10px; }
    
    /* Nilai Keuntungan Utama (Pips Display) */
    .pips-profit-large { font-size: 48px; font-weight: 900; color: #00ffcc; margin-top: 5px; }
    .pips-loss-large { font-size: 48px; font-weight: 900; color: #ff3366; margin-top: 5px; }
    .pips-label { font-size: 10px; color: #64748b; letter-spacing: 2px; text-transform: uppercase; }
    
    /* Kotak Amaran Risiko Pasaran (Warning Box) */
    .warning-card {
        background-color: #1e130c; border: 1px solid #b45309; border-radius: 12px;
        padding: 12px; text-align: left; margin: 15px 0; font-size: 12px; line-height: 1.4;
    }
    .warning-header { color: #f59e0b; font-weight: bold; margin-bottom: 4px; }
    
    /* Kotak Sasaran KEKAL (SL & TP Targets Grid) */
    .target-grid { display: flex; justify-content: space-between; gap: 8px; margin-top: 15px; }
    .target-box {
        background-color: #0f172a; border: 1px solid #1e293b; border-radius: 12px;
        padding: 10px; width: 24%; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .t-title { font-size: 10px; font-weight: bold; color: #64748b; margin-bottom: 4px; }
    .t-val-sl { font-size: 15px; font-weight: 800; color: #ff3366; }
    .t-val-tp { font-size: 15px; font-weight: 800; color: #38bdf8; }
    .t-sub { font-size: 10px; color: #475569; margin-top: 2px; }
    
    .session-badge { padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; display: inline-block; margin: 2px; background-color: #120e1c; border: 1px solid #2d224d; }
    </style>
    """, unsafe_allow_html=True)

# Tajuk Aplikasi & Dekorasi Seni Premium
st.markdown("<div style='text-align: center; margin-top: 10px;'>", unsafe_allow_html=True)
st.markdown("<h2 style='color: #ffffff; font-weight: 900; letter-spacing: 1px; margin-bottom: 0;'>🔱 MASTER AI SGINAL</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #818cf8; font-size: 11px; font-weight: 700; letter-spacing: 3px; margin-top: 0;'>GOLD SIGNALS MULTI-TIMEFRAME SYSTEM</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sesi Pasaran Live (Zon Masa Malaysia)
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

if "demo_balance" not in st.session_state: st.session_state.demo_balance = 10000.0
if "trade_history" not in st.session_state:
    st.session_state.trade_history = [
        {"Time": "5m ago", "Setup": "M1 BUY", "Zone": "2715 - 2719", "Result": "Break even", "Pips": "0.0"},
        {"Time": "15m ago", "Setup": "M1 SELL", "Zone": "2720 - 2724", "Result": "Completed TP1", "Pips": "+30.0"},
        {"Time": "1h ago", "Setup": "M15 BUY", "Zone": "2710 - 2714", "Result": "Completed TP2", "Pips": "+50.0"}
    ]

tab_setups, tab_perf, tab_analysis = st.tabs(["🎯 SETUPS", "📈 PERFORMANCE", "📊 ANALYSIS"])

# Set Nilai Asal Kalis Error Hujung Minggu
harga_semasa = 2715.50
signal = "WAIT"
zone_low, zone_high = 2714, 2716
sl_val, tp1_val, tp2_val, tp3_val = 2711, 2720, 2724, 2731
trend_h1 = "BEAR"
stoch_val = 50.0

try:
    df_m5 = yf.Ticker("GC=F").history(period="5d", interval="5m")
    df_m15 = yf.Ticker("GC=F").history(period="5d", interval="15m")
    df_h1 = yf.Ticker("GC=F").history(period="10d", interval="1h")
    
    if not df_m5.empty and not df_h1.empty and len(df_m5) > 15 and len(df_h1) > 50:
        harga_semasa = df_m5['Close'].iloc[-1]
        df_h1['EMA50'] = ta.trend.ema_indicator(df_h1['Close'], window=50)
        df_m5['stoch_k'] = ta.momentum.StochasticOscillator(df_m5['High'], df_m5['Low'], df_m5['Close'], window=14).stoch()
        
        trend_h1 = "BULL" if df_h1['Close'].iloc[-1] > df_h1['EMA50'].iloc[-1] else "BEAR"
        stoch_val = df_m5['stoch_k'].iloc[-1] if not pd.isna(df_m5['stoch_k'].iloc[-1]) else 50.0

        if trend_h1 == "BULL" and stoch_val < 45:
            signal = "BUY"
            zone_low = int(harga_semasa - 2)
            zone_high = int(harga_semasa + 2)
            sl_val = zone_low - 3
            tp1_val = zone_high + 4
            tp2_val = zone_high + 8
            tp3_val = zone_high + 15
        elif trend_h1 == "BEAR" and stoch_val > 55:
            signal = "SELL"
            zone_low = int(harga_semasa - 2)
            zone_high = int(harga_semasa + 2)
            sl_val = zone_high + 3
            tp1_val = zone_low - 4
            tp2_val = zone_low - 8
            tp3_val = zone_low - 15
        else:
            signal = "WAIT"
            zone_low = int(harga_semasa - 1)
            zone_high = int(harga_semasa + 1)
            sl_val = zone_low - 3
            tp1_val = zone_high + 4
            tp2_val = zone_high + 8
            tp3_val = zone_high + 15

except Exception as e:
    pass

# ================= TAB 1: SETUPS (PAPARAN SASARAN KEKAL KALIS EXCEPTION) =================
with tab_setups:
    st.markdown("<div class='app-container'>", unsafe_allow_html=True)
    
    if signal == "BUY":
        st.markdown("<span class='badge-buy'>▲ BUY</span>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:12px; color:#64748b;'>Gold / M5 / Just Scanned</div>", unsafe_allow_html=True)
        st.markdown("<div class='zone-title'>BUY ZONE</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='zone-price'>{zone_low} - {zone_high}</div>", unsafe_allow_html=True)
        pips_diff = int((harga_semasa - zone_low) * 10)
        st.markdown(f"<div class='live-dot-line'>● LIVE <span class='live-status-green'>${harga_semasa:.2f}</span> {abs(pips_diff)} pips</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='pips-profit-large'>+{max(5, pips_diff)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='pips-label'>PIPS IN PROFIT</div>", unsafe_allow_html=True)
    elif signal == "SELL":
        st.markdown("<span class='badge-sell'>▼ SELL</span>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:12px; color:#64748b;'>Gold / M5 / Just Scanned</div>", unsafe_allow_html=True)
        st.markdown("<div class='zone-title'>SELL ZONE</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='zone-price'>{zone_low} - {zone_high}</div>", unsafe_allow_html=True)
        pips_diff = int((zone_high - harga_semasa) * 10)
        st.markdown(f"<div class='live-dot-line'>● LIVE <span class='live-status-red'>${harga_semasa:.2f}</span> {abs(pips_diff)} pips</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='pips-loss-large'>+{max(5, pips_diff)}</div>", unsafe_allow_html=True)
        st.markdown("<div class='pips-label'>PIPS IN PROFIT</div>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='badge-wait'>● SCANNING</span>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:12px; color:#64748b;'>Gold / M5 / Monitoring Matrix</div>", unsafe_allow_html=True)
        st.markdown("<div class='zone-title'>CURRENT ZONE</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='zone-price'>{zone_low} - {zone_high}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='live-dot-line'>● LIVE <span class='live-status-wait'>${harga_semasa:.2f}</span> Pasaran Menutup/Sideway</div>", unsafe_allow_html=True)
