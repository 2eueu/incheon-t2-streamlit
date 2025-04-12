import streamlit as st
import requests
from datetime import datetime

# 실시간 API 호출 함수
@st.cache_data(ttl=3600)  # 1시간 캐싱
def get_flights():
    today = datetime.now().strftime("%Y%m%d")
    url = "http://apis.data.go.kr/B551177/StatusOfPassengerFlightsOdp/getPassengerDeparturesOdp"
    service_key = "kGGoic28kuWkdeS3FBZakDLtFkduZJF+Hxk4EOK0r6YGjW6aTz8tiDePFey1JaZwdXrvUrpe8vR3ZRCUJaAZVw=="

    params = {
        "serviceKey": service_key,
        "from_time": "0000",
        "to_time": "2400",
        "lang": "K",
        "type": "json"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        flights = data.get("response", {}).get("body", {}).get("items", [])
        # T2(terminalId = P03) & 단독편만 필터링
        filtered = [
            f for f in flights
            if f.get("terminalId") == "P03" and f.get("codeshare", "").lower() != "slave"
        ]
        return filtered
    except:
        return []

# UI
st.set_page_config(page_title="인천공항 출발편 대시보드", layout="wide")
st.title("🛫 인천공항 T2 출발 항공편")
st.caption(f"{datetime.now().strftime('%Y-%m-%d')} 기준, 실시간 API 데이터")

flights = get_flights()

# 요약
st.metric("출발편 수 (T2)", f"{len(flights)}편")

# 테이블 표시용 데이터 정리
if flights:
    table_data = [
        {
            "항공사": f.get("airline"),
            "편명": f.get("flightId"),
            "출발 예정": f.get("scheduleDateTime"),
            "출발 실제": f.get("estimatedDateTime"),
            "목적지": f.get("airport"),
            "게이트": f.get("gatenumber"),
            "상태": f.get("remark")
        }
        for f in flights
    ]
    st.markdown("### 📋 항공편 목록")
    st.dataframe(table_data, use_container_width=True)
else:
    st.warning("⚠️ 항공편 데이터를 불러오지 못했습니다.")
