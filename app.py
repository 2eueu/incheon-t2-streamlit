# app.py (Streamlit)
import streamlit as st
import json
from datetime import datetime

# Load flight data
with open("data/flights.json", "r", encoding="utf-8") as f:
    flights = json.load(f)

st.set_page_config(page_title="Incheon Flight Board", layout="wide")
st.title("🛫 Incheon Airport Flight Dashboard")

# Summary
st.markdown("### 📅 Flight Overview for Today")
st.info(f"Total Flights: **{len(flights)}** | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')} KST")

# Table
st.dataframe(flights, use_container_width=True)
