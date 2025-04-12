# app.py (실시간 API 호출 버전)
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ✈️ 실시간 항공편 데이터 요청 함수
@st.cache_data(ttl=3600)  # 1시간 캐시
def get_flights():
    today = datetime.now().strftime("%Y%m%d")
    url = "http://apis.data.go.kr/B551177/StatusOfPassengerFlightsOdp/getPassengerDeparturesOdp"
    service_key = "kGGoic28kuWkdeS3FBZakDLtFkduZJF+Hxk4EOK0r6YGjW6aTz8tiDePFey1JaZwdXrvUrpe8vR3ZRCUJaAZVw=="  # 🔐 네 공개키

    params = {
        "serviceKey": service_key,
        "from_time": "0000",
        "to_time": "2400",
        "lang": "K",
        "type": "json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        all_flights = data.get("response", {}).get("body", {}).get("items", [])

        # T2 + 단독 운항 필터링
        filtered = [
            f for f in all_flights
            if f.get("terminalId") == "P03" and f.get("codeshare", "").lower() != "slave"
        ]
        return filtered
    except Exception as e:
        st.error(f"❌ API 호출 실패: {e}")
        return []

# 🚀 앱 실행 시작
flights = get_flights()

# 📄 DataFrame 변환 및 정리
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

# 💻 Streamlit UI
st.set_page_config(page_title="인천공항 T2 출발편", layout="centered")
st.title("🛫 인천공항 T2 실시간 출발편 대시보드")
st.caption(f"📅 {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')} 기준")

# 📌 요약
st.metric("출발 항공편 수", f"{len(df)}편")

# 📋 테이블
st.dataframe(df, use_container_width=True)

# 안내
if df.empty:
    st.info("현재 항공편 데이터가 없습니다. 다시 시도해 주세요.")
