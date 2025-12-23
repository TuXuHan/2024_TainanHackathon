from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from openai import OpenAI

#chrome_options = Options()
#chrome_options.add_argument("--headless")
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver = webdriver.Chrome()

client = OpenAI(api_key='YOUR_OPENAI_API_KEY')

url = 'https://www.google.com/maps'
driver.get(url)

review_time = '2年'

searchkeys = ['小董牛肉湯爐', 'Win Chang Beef Soup Anping Main Shop', '豪牛牛肉湯（售完為止)', '新鮮牛肉湯(東門店)', '伍鍋貳牛 台南溫體牛肉湯/個人鍋 鴛鴦鍋/聚餐台南美食', '阿家牛肉湯&火鍋（營業時間以牛肉售完為止']

for key in searchkeys:
    searchbox = driver.find_element(By.ID, 'searchboxinput')
    searchbox.send_keys(key)

    searchbtn = driver.find_element(By.CLASS_NAME, 'mL3xi')
    searchbtn.click()

    reviewsbtn = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(3) > div > div > button:nth-child(2)'))
    )
    reviewsbtn.click()

    sortingbtn = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[7]/div[2]/button'))
    )
    sortingbtn.click()

#    time.sleep(5)

    newest = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.fxNQSd[data-index='1']"))
    )
    newest.click()

    ReviewsMaxNum = 100

    def words_count(sen):
        words = sen.split(' ')
        return len(words)

    pane = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'm6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde'))
    )

    flag = True
    while flag:
        reviewcount = 0
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pane)
        try:
            FullTextbtn = driver.find_element(By.CLASS_NAME, 'w8nwRe.kyuRq')
            FullTextbtn.click()
    #        time.sleep(5)
        except:
            pass
    #        print('No btn')
    #        time.sleep(2)
        review = driver.find_elements(By.CLASS_NAME, 'wiI7pd')
        for r in review:
            if(words_count(r.text) > 10):
                reviewcount+=1
            howlong = driver.find_element(By.CLASS_NAME, 'rsqaWe')
            print(howlong.text)
            if howlong.text == '2 months ago':
                flag = False
            if reviewcount >= 10:
                flag = False


    content = '以下是餐廳的評論，請你根據這些評論生成這個餐廳的三個繁體中文相關詞：'

    for r in review:
        if(words_count(r.text) > 10):
            content += str(r.text)
    #        print(r.text)

    reply = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": content},
    ]
    ).choices[0].message.content

    print(key+'\n'+reply)

    Closebtn = driver.find_element(By.CLASS_NAME, 'yAuNSb.vF7Cdb')
    Closebtn.click()
    time.sleep(5)


driver.close()