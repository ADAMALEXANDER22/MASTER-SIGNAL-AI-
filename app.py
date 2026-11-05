import streamlit as st
import yfinance as yf
import pandas as pd
import ta

st.set_page_config(page_title="Mobile Gold AI", layout="centered")
st.title("🏆 Mobile AI Gold Signal (MTF)")

@st.cache_data(ttl=30)
def ambil_data(period, interval):
    ticker = yf.Ticker("GC=F")
    return ticker.history(period=period, interval=interval)

st.subheader("Semakan Signal Semasa")

try:
    df_h1 = ambil_data("5d", "1h")
    df_m30 = ambil_data("3d", "30m")
    df_m15 = ambil_data("2d", "15m")
    df_m5 = ambil_data("1d", "5m")

    harga_semasa = df_m5['Close'].iloc[-1]
    st.metric(label="Harga XAUUSD Semasa", value=f"${harga_semasa:.2f}")

    df_h1['EMA50'] = ta.trend.ema_indicator(df_h1['Close'], window=50)
    trend_h1 = "UPTREND" if df_h1['Close'].iloc[-1] > df_h1['EMA50'].iloc[-1] else "DOWNTREND"

    df_m30['RSI'] = ta.momentum.rsi(df_m30['Close'], window=14)
    df_m15['RSI'] = ta.momentum.rsi(df_m15['Close'], window=14)
    rsi_m30 = df_m30['RSI'].iloc[-1]
    rsi_m15 = df_m15['RSI'].iloc[-1]

    stoch = ta.momentum.StochasticOscillator(df_m5['High'], df_m5['Low'], df_m5['Close'], window=14)
    df_m5['stoch_k'] = stoch.stoch()
    stoch_m5 = df_m5['stoch_k'].iloc[-1]

    if trend_h1 == "UPTREND" and rsi_m30 < 65 and rsi_m15 < 65 and stoch_m5 < 25:
        st.success(f"🟢 **SIGNAL: BUY ENTRY**\n\nZon M5 Oversold pada harga ${harga_semasa:.2f}. Trend H1 menyokong kenaikan.")
    elif trend_h1 == "DOWNTREND" and rsi_m30 > 35 and rsi_m15 > 35 and stoch_m5 > 75:
        st.danger(f"🔴 **SIGNAL: SELL ENTRY**\n\nZon M5 Overbought pada harga ${harga_semasa:.2f}. Trend H1 menyokong penurunan.")
    else:
        st.warning("🟡 **SIGNAL: WAIT / TIADA MATRIKS**\n\nTimeframe tidak selari. Tunggu konfirmasi M5 masuk ke zon overbought/oversold.")

    st.write("---")
    st.markdown(f"**Status Petunjuk:**")
    st.write(f"- Trend H1: `{trend_h1}`")
    st.write(f"- Momentum M30 (RSI): `{rsi_m30:.1f}`")
    st.write(f"- Momentum M15 (RSI): `{rsi_m15:.1f}`")
    st.write(f"- Entry M5 (Stoch): `{stoch_m5:.1f}`")

except Exception as e:
    st.error("Sedang memuatkan data atau pasaran sedang ditutup (hujung minggu).")
