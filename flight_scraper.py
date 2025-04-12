# flight_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json

def get_flight_data():
    # ✅ 크롬 옵션 설정 (headless 환경용)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    # ✅ 크롬 드라이버 실행
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://www.airport.kr/ap_ko/869/subview.do"
    driver.get(url)
    print(f"🌐 접속한 URL: {url}")
    time.sleep(2)

    # ✅ 날짜 설정 (한국어 요일 포함)
    today = datetime.now()
    weekday_map = {'Mon': '월', 'Tue': '화', 'Wed': '수', 'Thu': '목', 'Fri': '금', 'Sat': '토', 'Sun': '일'}
    weekday_kor = weekday_map[today.strftime('%a')]
    today_str = today.strftime(f"%Y.%m.%d ({weekday_kor})")
    print(f"📅 오늘 날짜: {today_str}")

    # ✅ 드롭다운 선택
    Select(driver.find_element(By.ID, "daySel")).select_by_visible_text(today_str)
    Select(driver.find_element(By.ID, "termId")).select_by_visible_text("T2")
    Select(driver.find_element(By.ID, "fromTime")).select_by_visible_text("00:00")
    Select(driver.find_element(By.ID, "toTime")).select_by_visible_text("23:59")
    time.sleep(10)

    # 🔍 HTML 일부 출력해서 렌더링 확인!
    print("📄 페이지 일부 HTML:")
    print(driver.page_source[:1500])
    
    # ✅ 안정적인 버튼 클릭 (수정 포인트!)
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-search")))
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-search"))).click()
    time.sleep(3)

    # ✅ 페이지 스크롤
    body = driver.find_element(By.TAG_NAME, "body")
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(30):
        body.send_keys(Keys.END)
        time.sleep(1.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # ✅ 데이터 파싱
    soup = BeautifulSoup(driver.page_source, "html.parser")
    flight_blocks = soup.select("button.toggle")

    if not flight_blocks:
        print("⚠️ No flight data found. Check if the page loaded properly.")

    results = []
    for block in flight_blocks:
        try:
            dep_time = block.select_one("div.time > strong").text.strip()
            destination = block.select_one("div.location > em").text.strip()
            gate = block.select_one("div.enter > em").text.strip()
            results.append({
                "departure_time": dep_time,
                "destination": destination,
                "gate": gate
            })
        except:
            continue

    driver.quit()

    # ✅ JSON 저장
    with open("data/flights.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ 저장 완료: {len(results)} flights saved to data/flights.json")

if __name__ == "__main__":
    get_flight_data()
