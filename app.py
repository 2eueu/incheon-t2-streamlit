import streamlit as st
import json
from datetime import datetime
import os
import pandas as pd

# 📁 flights.json 불러오기 (없으면 빈 리스트 반환)
def load_flights():
    path = "data/flights.json"
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# 📊 데이터 불러오기
flights = load_flights()

# 📄 DataFrame 변환 및 정리
if flights:
    df = pd.DataFrame(flights)
    
    # 컬럼 정리 및 한글화
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

# 🌐 페이지 설정
st.set_page_config(page_title="인천공항 출발편 대시보드", layout="centered")
st.title("🛫 인천공항 출발 항공편 대시보드")
st.caption(f"📅 {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')} 기준, 인천공항 T2 출발편")

# 📌 요약 정보
st.markdown("## ✈️ 요약 정보")
st.metric(label="총 출발 항공편 수", value=f"{len(df)}편")

# 📋 항공편 목록 테이블
st.markdown("## 📋 항공편 목록")
st.dataframe(df, use_container_width=True)

# ❗ 파일이 없을 경우 안내 메시지
if df.empty:
    st.warning("⚠️ 현재 항공편 정보가 없습니다.\n\nflight_scraper.py를 실행해 data/flights.json 파일을 먼저 생성하세요.")
