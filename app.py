# app.py
import streamlit as st
import json
from datetime import datetime
import os
import pandas as pd

def load_flights():
    path = "data/flights.json"
    if not os.path.exists(path):
        st.warning("⚠️ flights.json 파일이 존재하지 않습니다.")
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.error("❌ flights.json 파일이 손상되었거나 잘못된 JSON입니다.")
        return []

flights = load_flights()

# 데이터프레임 정리
if flights:
    df = pd.DataFrame(flights)
    df = df.rename(columns={
        "flightId": "항공편",
        "airline": "항공사",
        "scheduleDateTime": "예정 시간",
        "estimatedDateTime": "변경 시간",
        "gatenumber": "게이트",
        "chkinrange": "탑승수속",
        "airport": "목적지",
        "remark": "상태"
    })
    df = df.sort_values(by="예정 시간")
else:
    df = pd.DataFrame(columns=["항공편", "항공사", "예정 시간", "변경 시간", "게이트", "탑승수속", "목적지", "상태"])

# Streamlit UI 구성
st.set_page_config(page_title="인천공항 출발편 대시보드", layout="centered")
st.title("🛫 인천공항 출발 항공편 대시보드")
st.caption(f"📅 {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')} 기준, T2 출발편")

# 요약 정보
st.markdown("## ✈️ 요약")
st.metric(label="출발 항공편 수", value=f"{len(df)}편")

# 테이블 출력
st.markdown("## 📋 항공편 목록")
st.dataframe(df, use_container_width=True)

# 안내
if df.empty:
    st.info("✉️ 데이터를 보려면 먼저 `flight_scraper.py`를 실행해 주세요.")
