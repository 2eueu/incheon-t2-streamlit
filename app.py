# app.py
import streamlit as st
import requests
import json
from datetime import datetime

@st.cache
def get_flights():
    url = "http://apis.data.go.kr/B551177/StatusOfPassengerFlightsOdp/getPassengerDeparturesOdp"
    service_key = "kGGoic28kuWkdeS3FBZakDLtFkduZJF+Hxk4EOK0r6YGjW6aTz8tiDePFey1JaZwdXrvUrpe8vR3ZRCUJaAZVw=="
    params = {
        "serviceKey": service_key,
        "from_time": "0000",
        "to_time": "2400",
        "lang": "K",
        "type": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()
    all_flights = data.get("response", {}).get("body", {}).get("items", [])

    # T2 & 단독 항공편만 필터링
    filtered = [
        flight for flight in all_flights
        if flight.get("terminalId") == "P03" and flight.get("codeshare", "").lower() != "slave"
    ]
    return filtered

# 페이지 설정
st.set_page_config(page_title="인천공항 출발편 대시보드", layout="centered")
st.title("🛫 인천공항 출발 항공편 대시보드")
st.caption(f"{datetime.now().strftime('%Y년 %m월 %d일')} 기준, 인천공항 T2 출발편")

flights = get_flights()

# 요약 정보
st.markdown("### ✈️ 요약")
st.metric(label="총 항공편 수", value=f"{len(flights)}편")

# 항공편 테이블
st.markdown("### 📋 항공편 목록")
st.dataframe(flights, use_container_width=True)
