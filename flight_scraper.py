# flight_scraper.py (Flask 버전 호환)
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
import csv

def get_flight_count():
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

    date_select = Select(driver.find_element(By.ID, "daySel"))
    date_select.select_by_visible_text(today_str)

    terminal_select = Select(driver.find_element(By.ID, "termId"))
    terminal_select.select_by_visible_text("T2")

    Select(driver.find_element(By.ID, "fromTime")).select_by_visible_text("00:00")
    Select(driver.find_element(By.ID, "toTime")).select_by_visible_text("23:59")
    time.sleep(1)

    search_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-search"))
    )
    driver.execute_script("arguments[0].click();", search_btn)
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

    unique_flights = set()
    for block in flight_blocks:
        try:
            dep_time = block.select_one("div.time > strong").text.strip()
            destination = block.select_one("div.location > em").text.strip()
            gate = block.select_one("div.enter > em").text.strip()
            flight_key = (dep_time, destination, gate)
            unique_flights.add(flight_key)
        except:
            continue

    driver.quit()

    with open("flights.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["출발시간", "목적지", "게이트"])
        for dep_time, destination, gate in unique_flights:
            writer.writerow([dep_time, destination, gate])

    return len(flight_blocks), len(unique_flights)