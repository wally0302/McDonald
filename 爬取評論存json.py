from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# 初始化 WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")  # 禁用 GPU（必要時）
driver = webdriver.Chrome(options=options)

try:
    # 打開目標頁面
    url = "https://www.google.com/search?q=%E6%96%B0%E7%AB%B9+%E9%BA%A5%E7%95%B6%E5%8B%9E&sca_esv=c959b87647eb8a0a&hl=zh-TW&sxsrf=ADLYWIK19Nd1tEFNoY05ivSMiVp8JTfqtg%3A1735836911756&source=hp&ei=78R2Z9z6Kv_31e8PxYy3sQQ&iflsig=AL9hbdgAAAAAZ3bS_0KaSvv7vCTCJdLTLKoyUb1h9YeT&ved=0ahUKEwicroq0wNeKAxX_e_UHHUXGLUYQ4dUDCBk&uact=5&oq=%E6%96%B0%E7%AB%B9+%E9%BA%A5%E7%95%B6%E5%8B%9E&gs_lp=Egdnd3Mtd2l6IhDmlrDnq7kg6bql55W25YueMgoQIxiABBgnGIoFMgQQIxgnMgQQIxgnMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgQQABgeSNMvUABYgCVwAngAkAEBmAHOBaAB3DWqAQ0wLjEuNy40LjQuMi4xuAEDyAEA-AEBmAINoAKtHagCCsICERAuGIAEGLEDGNEDGIMBGMcBwgILEAAYgAQYsQMYgwHCAggQABiABBixA8ICDRAAGIAEGLEDGEMYigXCAg0QLhiABBixAxhDGIoFwgIOEAAYgAQYsQMYgwEYigXCAgcQIxgnGOoCwgIUEC4YgAQYsQMYgwEYxwEYjgUYrwHCAgIQJsICCBAAGIAEGKIEwgIFEAAY7wXCAgoQABiABBhDGIoFwgIQEC4YgAQYQxjHARiKBRivAcICChAuGIAEGEMYigXCAgsQABiABBixAxiKBcICFBAuGIAEGLEDGNEDGIMBGMcBGIoFwgIUEC4YgAQYsQMYgwEYxwEYigUYrwHCAgsQLhiABBjHARivAZgDBvEFFvFFNqtOm1ySBwsyLjEuNC4zLjIuMaAH6Hc&sclient=gws-wiz#lkt=LocalPoiReviews&rlimm=1075161863879597081"
    driver.get(url)
    time.sleep(7.0)  # 等待頁面加載完成

    # 定位滾動容器
    scroll_container = driver.find_element(By.CSS_SELECTOR, "div.R4aD0e.AVvGRc")
    print(f"scroll_container: {scroll_container}")

    # 初始化滾動
    last_height = driver.execute_script("return arguments[0].scrollTop", scroll_container)

    all_reviews = []  # 用於存儲所有評論

    for i in range(1):  # 設定滾動次數，這裡是 3 次
        # 滾動至底部
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
        time.sleep(5)  # 等待新內容加載

        # 獲取新高度並比較是否到底
        new_height = driver.execute_script("return arguments[0].scrollTop", scroll_container)
        if new_height == last_height:
            break
        last_height = new_height

        # 點擊「閱讀更多」按鈕
        expand_buttons = driver.find_elements(By.CLASS_NAME, "MtCSLb")
        for button in expand_buttons:
            button.click()
            time.sleep(5.0)  # 確保按鈕被完全展開

        # 將評論格式化為字典
        reviews_data = {
            "reviews": all_reviews
        }
        

    # 將評論保存到 JSON 文件
    with open("food_reviews.json", "w", encoding="utf-8") as f:
        json.dump(reviews_data, f, ensure_ascii=False, indent=4)

    print(f"成功保存 {len(all_reviews)} 條評論至 food_reviews.json 文件！")

except Exception as e:
    print(f"error: {e}")

finally:
    # 關閉 WebDriver
    driver.quit()
