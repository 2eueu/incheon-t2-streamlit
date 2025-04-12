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
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    url = "https://www.airport.kr/ap_ko/869/subview.do"
    driver.get(url)
    time.sleep(2)

    today = datetime.now()
    weekday_map = {'Mon': '월', 'Tue': '화', 'Wed': '수', 'Thu': '목', 'Fri': '금', 'Sat': '토', 'Sun': '일'}
    weekday_kor = weekday_map[today.strftime('%a')]
    today_str = today.strftime(f"%Y.%m.%d ({weekday_kor})")

    Select(driver.find_element(By.ID, "daySel")).select_by_visible_text(today_str)
    Select(driver.find_element(By.ID, "termId")).select_by_visible_text("T2")
    Select(driver.find_element(By.ID, "fromTime")).select_by_visible_text("00:00")
    Select(driver.find_element(By.ID, "toTime")).select_by_visible_text("23:59")
    time.sleep(1)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-search"))).click()
    time.sleep(3)

    body = driver.find_element(By.TAG_NAME, "body")
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(30):
        body.send_keys(Keys.END)
        time.sleep(1.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, "html.parser")
    flight_blocks = soup.select("button.toggle")

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

    with open("data/flights.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(results)} flights to data/flights.json")

if __name__ == "__main__":
    get_flight_data()
