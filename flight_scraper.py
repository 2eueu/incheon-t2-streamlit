import requests
import json
from datetime import datetime

def get_flight_data():
    # 오늘 날짜를 'YYYYMMDD' 형식으로 설정
    today = datetime.now().strftime("%Y%m%d")
    print(f"📅 오늘 날짜: {today}")

    # API 요청에 사용할 파라미터 설정
    payload = {
        "schDate": today,         # 조회할 날짜
        "schDeptCityCode": "",    # 출발 도시 코드 (필요 시 설정)
        "schArrvCityCode": "",    # 도착 도시 코드 (필요 시 설정)
        "schAirCode": "",         # 항공사 코드 (필요 시 설정)
        "schFlightNum": "",       # 항공편 번호 (필요 시 설정)
        "schTime": "0000",        # 조회 시작 시간 (HHMM 형식)
        "schIoType": "O",         # 'O'는 출발편, 'I'는 도착편
        "schTerminalCode": "T2",  # 터미널 코드 ('T1', 'T2' 등)
        "page": "1",
        "pageSize": "1000"
    }

    # HTTP 헤더 설정
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0"
    }

    # API 엔드포인트 URL
    url = "https://www.airport.kr/dep/ap_ko/getDepPasSchList.do"

    # POST 요청 보내기
    response = requests.post(url, data=payload, headers=headers)

    # 응답 상태 확인
    if response.status_code == 200:
        data = response.json()
        flights = data.get("list", [])
        print(f"✅ 수신된 항공편 수: {len(flights)}")

        # 결과를 JSON 파일로 저장
        with open("data/flights.json", "w", encoding="utf-8") as f:
            json.dump(flights, f, ensure_ascii=False, indent=2)

        print("✅ 데이터가 'data/flights.json'에 저장되었습니다.")
    else:
        print(f"❌ 요청 실패. 상태 코드: {response.status_code}")

if __name__ == "__main__":
    get_flight_data()
