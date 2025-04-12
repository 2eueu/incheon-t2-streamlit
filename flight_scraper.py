import requests
import json
from datetime import datetime

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
        "type": "json"
    }

    response = requests.get(url, params=params)
    print(f"🔍 응답 코드: {response.status_code}")

    try:
        data = response.json()
        print("✅ 응답 JSON 일부:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
    except Exception as e:
        print("❌ JSON 디코딩 실패:", e)
        print("📝 원본 응답 내용:")
        print(response.text[:1000])
        return

    # 결과 필터링: 제2터미널(T2), codeshare != Slave
    flights = data.get("response", {}).get("body", {}).get("items", [])
    filtered = [
        flight for flight in flights
        if flight.get("terminalId") == "P03" and flight.get("codeshare", "").lower() != "slave"
    ]
    print(f"✈️ T2 & 단독 항공편 수: {len(filtered)}")

    with open("data/flights.json", "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
    print("✅ 'data/flights.json'에 저장 완료")

if __name__ == "__main__":
    get_flight_data()
