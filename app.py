# app.py
import streamlit as st
import json
from datetime import datetime

# JSON 불러오기
with open("data/flights.json", "r", encoding="utf-8") as f:
    flights = json.load(f)

# 페이지 설정
st.set_page_config(page_title="인천공항 출발편 대시보드", layout="centered")
st.title("🛫 인천공항 출발 항공편 대시보드")
st.caption(f"{datetime.now().strftime('%Y년 %m월 %d일')} 기준, 인천공항 T2 출발편")

# 요약 정보
st.markdown("### ✈️ 요약")
st.metric(label="총 항공편 수", value=f"{len(flights)}편")

# 항공편 테이블
st.markdown("### 📋 항공편 목록")
st.dataframe(flights, use_container_width=True)
