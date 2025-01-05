from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


# 設置 WebDriver
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # 如果需要非可視化模式，取消註解這行
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

# 爬取目標
query = "新竹 麥當勞"
url = f"https://www.google.com/maps/search/{query}"
driver.get(url)

try:
    # 初始化變數
    stores = []
    last_height = 0  # 初始化滾動高度

    while True:
        # 定位滾動容器
        try:
            scrollable_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
            )
        except TimeoutException:
            print("滾動容器加載超時，無法繼續。")
            break

        # 抓取結果卡片
        results = driver.find_elements(By.CSS_SELECTOR, ".Nv2PK")
        for result in results:
            try:
                name = result.find_element(By.CSS_SELECTOR, ".qBF1Pd").text             
                star = result.find_element(By.CLASS_NAME, "MW4etd").text
                store_data = {"name": name,  "star": star}
                if store_data not in stores:
                    stores.append(store_data)
            except Exception as e:
                print(f"解析失敗: {e}")

        # 模擬滾動
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        time.sleep(3)  # 等待新內容加載

        # 判斷是否滾動到底部
        new_height = driver.execute_script("return arguments[0].scrollTop", scrollable_div)
        if new_height == last_height:
            break
        last_height = new_height

    # 輸出結果
    for store in stores:
        print(f"分店名稱: {store['name']},  星等: {store['star']}")

finally:
    driver.quit()  # 結束 WebDriver
