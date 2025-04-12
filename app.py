import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ✅ 가장 먼저 페이지 설정
st.set_page_config(page_title="인천공항 T2 출발편", layout="centered")

# ✈️ 실시간 항공편 데이터 요청 함수
@st.cache_data(ttl=3600)
def get_flights():
    today = datetime.now().strftime("%Y%m%d")
    url = "http://apis.data.go.kr/B551177/StatusOfPassengerFlightsOdp/getPassengerDeparturesOdp"
    service_key = "kGGoic28kuWkdeS3FBZakDLtFkduZJF+Hxk4EOK0r6YGjW6aTz8tiDePFey1JaZwdXrvUrpe8vR3ZRCUJaAZVw=="

    params = {
        "serviceKey": service_key,
        "from_time": "0000",
        "to_time": "2400",
        "lang": "K",
        "type": "json",
        "depPlandTime": today  # ✅ 날짜 명시
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        flights = data.get("response", {}).get("body", {}).get("items", [])
        return [
            f for f in flights
            if f.get("terminalId") == "P03" and f.get("codeshare", "").lower() != "slave"
        ]
    except Exception as e:
        st.error(f"❌ API 호출 실패: {e}")
        return []

# 🚀 데이터 가져오기
flights = get_flights()

# 📊 DataFrame 구성
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

# 🖥️ 화면 구성
st.title("🛫 인천공항 T2 실시간 출발편 대시보드")
st.caption(f"📅 {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')} 기준")

st.metric("출발 항공편 수", f"{len(df)}편")
st.dataframe(df, use_container_width=True)

if df.empty:
    st.info("✉️ 현재 항공편 데이터가 없습니다. 잠시 후 다시 확인해 주세요.")
