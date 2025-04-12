import streamlit as st
import requests
import json
from datetime import datetime

@st.cache_data(ttl=3600)
def get_flights():
    today = datetime.now().strftime("%Y%m%d")
    url = "http://apis.data.go.kr/B551177/StatusOfPassengerFlightsOdp/getPassengerDeparturesOdp"
    service_key = "너의_실제_키"  # URL 인코딩된 키

    params = {
        "serviceKey": service_key,
        "from_time": "0000",
        "to_time": "2400",
        "lang": "K",
        "type": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    flights = data.get("response", {}).get("body", {}).get("items", [])
    filtered = [
        flight for flight in flights
        if flight.get("terminalId") == "P03" and flight.get("codeshare", "").lower() != "slave"
    ]
    return filtered

# Streamlit 화면 구성
st.set_page_config(page_title="인천공항 출발편 대시보드", layout="centered")
st.title("🛫 인천공항 출발 항공편 대시보드")
st.caption(f"{datetime.now().strftime('%Y년 %m월 %d일')} 기준, 인천공항 T2 출발편")

flights = get_flights()

st.markdown("### ✈️ 요약")
st.metric(label="총 항공편 수", value=f"{len(flights)}편")

st.markdown("### 📋 항공편 목록")
st.dataframe(flights, use_container_width=True)
