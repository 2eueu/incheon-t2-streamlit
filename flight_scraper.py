import requests
import json
from datetime import datetime

def get_flight_data():
    # ✅ 오늘 날짜 (yyyymmdd 형식)
    today = datetime.now().strftime("%Y%m%d")
    print(f"📅 오늘 날짜: {today}")

    # ✅ POST 요청 데이터
    payload = {
        "schDate": today,         # 날짜
        "schDeptCityCode": "",    # 출발지 필터 (없음)
        "schArrvCityCode": "",    # 도착지 필터 (없음)
        "schAirCode": "",         # 항공사 필터 (없음)
        "schFlightNum": "",       # 편명 필터 (없음)
        "schTime": "0000",        # 시작 시간 (00:00부터)
        "schIoType": "O",         # 출발편: O / 도착편: I
        "schTerminalCode": "T2",  # 터미널: T1, T2
        "page": "1",
        "pageSize": "1000"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0"
    }

    url = "https://www.airport.kr/dep/ap_ko/getDepPasSchList.do"
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        flights = data.get("list", [])

        # ✅ flights.json으로 저장
        with open("data/flights.json", "w", encoding="utf-8") as f:
            json.dump(flights, f, ensure_ascii=False, indent=2)

        print(f"✅ 저장 완료: {len(flights)}건 flights saved to data/flights.json")
    else:
        print(f"❌ 요청 실패. 상태코드: {response.status_code}")

if __name__ == "__main__":
    get_flight_data()
