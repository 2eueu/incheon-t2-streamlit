# app.py (for Streamlit)
import streamlit as st
from flight_scraper import get_flight_count

st.set_page_config(page_title="인천공항 항공편 카운터", page_icon="🛫")

st.title("🛫 인천공항 출발 항공편 대시보드")
st.markdown("2025년 오늘 날짜 기준, **인천공항 출발편 수**를 확인해보세요!")

# 데이터 가져오기
total, unique = get_flight_count()

# 시각적 출력
st.metric(label="✈️ 전체 항공편 블록 수", value=f"{total}편")
st.metric(label="🧮 중복 제외 항공편 수", value=f"{unique}편")
