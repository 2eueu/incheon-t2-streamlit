# flight_scraper.py
import requests
from bs4 import BeautifulSoup

def get_flight_count():
    url = "https://www.airport.kr/ap/ko/dpt/scheduelList.do"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 항공편 정보 추출
    rows = soup.select(".resultList > li")
    total = len(rows)

    # 중복 항공편 제거 기준 (예: 항공편 번호 + 시간)
    unique_flights = set()
    for row in rows:
        flight = row.select_one(".airline > strong")  # 항공사 정보
        time = row.select_one(".time")                # 시간 정보
        if flight and time:
            unique_flights.add(f"{flight.text.strip()}_{time.text.strip()}")

    return total, len(unique_flights)
