
import streamlit as st
from gpt_prompt import get_forecast
from data_fetcher import fetch_market_data

st.set_page_config(page_title="BTC Forecast Light", layout="centered")
st.title("📈 BTC Forecast Light")

st.markdown("Tägliche Wahrscheinlichkeit für Bitcoin-Kursbewegungen")
data = fetch_market_data()

if data:
    result = get_forecast(data)
    st.subheader("📊 Prognose")
    st.write(result)
else:
    st.error("Fehler beim Laden der Daten.")
