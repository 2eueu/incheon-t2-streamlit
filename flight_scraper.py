import requests
import json
from datetime import datetime
import os

def get_flight_data():
    today = datetime.now().strftime("%Y%m%d")
    print(f"📅 조회일자: {today}")

    url = "http://apis.data.go.kr/B551177/StatusOfPassengerFlightsOdp/getPassengerDeparturesOdp"
    service_key = "kGGoic28kuWkdeS3FBZakDLtFkduZJF+Hxk4EOK0r6YGjW6aTz8tiDePFey1JaZwdXrvUrpe8vR3ZRCUJaAZVw=="

    params = {
        "serviceKey": service_key,
        "from_time": "0000",
        "to_time": "2400",
        "lang": "K",
        "type": "json",
        "pageNo": "1",
        "numOfRows": "1000"
    }

    response = requests.get(url, params=params)
    print(f"🔍 응답 코드: {response.status_code}")

    try:
        data = response.json()
        all_flights = data.get("response", {}).get("body", {}).get("items", [])

        # ✅ T2 + 공동운항 정리
        filtered = []
        seen_flights = set()

        for flight in all_flights:
            if flight.get("terminalId") != "P02":
                continue  # T2 아니면 제외
            if flight.get("codeshare") == "Slave":
                continue  # 공동운항 종속편 제외
            flight_id = flight.get("flightId")
            if flight_id and flight_id not in seen_flights:
                filtered.append(flight)
                seen_flights.add(flight_id)

        print(f"✅ 필터링 후 항공편 수: {len(filtered)}")

        # 폴더 없으면 생성
        os.makedirs("data", exist_ok=True)
        with open("data/flights.json", "w", encoding="utf-8") as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)

        print("📁 'data/flights.json' 저장 완료!")

    except Exception as e:
        print("❌ JSON 디코딩 실패:", e)
        print("📝 원본 응답:")
        print(response.text[:1000])

if __name__ == "__main__":
    get_flight_data()
