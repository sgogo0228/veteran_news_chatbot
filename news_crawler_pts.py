if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import re, time
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


driver_path = r".\chromedriver-win64\chromedriver-win64\chromedriver.exe"
content_path = r".\output\news.txt"
svc = Service(driver_path)
options = webdriver.ChromeOptions()
options.page_load_strategy = 'none'
list_driver = webdriver.Chrome(service=svc)
driver = webdriver.Chrome(service=svc, options=options)

for page in range(1, 7):
    list_url = f"https://news.pts.org.tw/search/%E6%A6%AE%E7%B8%BD?page={page}"
    list_driver.get(list_url)
    time.sleep(2)
    news_list = list_driver.find_elements(By.CSS_SELECTOR, "li.row h2 a")
    
    with open(content_path, "a", encoding="utf-8") as f:
        for i, element in enumerate(news_list):
            title = element.text
            url = element.get_attribute('href')
            try:
                driver.get(url)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p:not([style], [class])")))

                date = driver.find_element(By.CSS_SELECTOR, "span.text-nowrap.mr-2 time").text
                date = re.sub(r" \d\d:\d\d", "", date)
                body_height = driver.find_element(By.TAG_NAME, "body").size["height"]
                loc_y = 500
                while loc_y < body_height:
                    driver.execute_script(f"window.scrollTo(0, {loc_y})")
                    loc_y += 500
                    time.sleep(0.04)
                contents = driver.find_elements(By.CSS_SELECTOR, "div.post-article p:not([style], [class])")
                f.write("--------------------------\n")
                f.write(date + "\n")
                f.write(title + "\n")
                for p in contents:
                    if p.text != "" and "按讚追蹤粉絲頁" not in p.text:
                        f.write(p.text + "\n")
            except:
                print(f"Error, Page:{page}, news_seq: {i}")
                continue

list_driver.quit()
driver.quit()