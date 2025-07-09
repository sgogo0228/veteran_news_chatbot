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
driver = webdriver.Chrome(service=svc, options=options)
# driver = webdriver.Chrome(service=svc)

for page in range(78, 123):
    res = requests.get(f"https://udn.com/api/more?page={page}&id=search:%E6%A6%AE%E7%B8%BD&channelId=2&type=searchword&last_page=287")
    soup = BeautifulSoup(res.text, "html.parser")
    soup = re.sub(r"\\", "", soup.text) 
    news_titles = re.findall('(?<="title":").+?(?=",)', soup)
    news_links = re.findall('(?<="titleLink":")https:.+?(?=",)', soup)
    news_dates = re.findall(r'(?<="date":").+?(?= \d\d:\d\d"},)', soup)
    
    with open(content_path, "a", encoding="utf-8") as f:
        for i in range(0, len(news_titles)):
            title = news_titles[i]
            date = news_dates[i]
            url = news_links[i]
            try:
                driver.get(url)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p:not([style], [class])")))

                body_height = driver.find_element(By.TAG_NAME, "body").size["height"]
                loc_y = 500
                while loc_y < body_height:
                    driver.execute_script(f"window.scrollTo(0, {loc_y})")
                    loc_y += 500
                    time.sleep(0.04)
                contents = driver.find_elements(By.CSS_SELECTOR, "p:not([style], [class])")
                f.write("--------------------------\n")
                f.write(date + "\n")
                f.write(title + "\n")
                for p in contents:
                    if p.text != "":
                        f.write(p.text + "\n")
            except:
                print(f"Error, Page:{page}, news_seq: {i}")
                continue

driver.quit()