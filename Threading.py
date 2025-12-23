
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
import threading
from concurrent.futures import ThreadPoolExecutor

def search(key):
    driver = webdriver.Chrome()
    client = OpenAI(api_key='YOUR_OPENAI_API_KEY')
    
    url = 'https://www.google.com/maps'
    driver.get(url)
    searchbox = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'searchboxinput'))
    )
    searchbox.send_keys(key)

    searchbtn = driver.find_element(By.CLASS_NAME, 'mL3xi')
    searchbtn.click()

    reviewsbtn = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(3) > div > div > button:nth-child(2)'))
    )

    reviewsbtn.click()

    # 取list中最低
    ReviewsMaxNum = 10

    def words_count(sen):
        words = sen.split(' ')
        return len(words)

    pane = WebDriverWait(driver, 10).until(
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
        if reviewcount >= ReviewsMaxNum:
            flag = False


    content = '以下是餐廳的評論，請你根據這些評論生成這個餐廳的三個繁體中文相關詞，格式為[xxx, xxx, xxx]：'

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

#    print(key+'\n'+reply)
    results[key] = reply

    Closebtn = driver.find_element(By.CLASS_NAME, 'yAuNSb.vF7Cdb')
    Closebtn.click()

    driver.quit()

# test: Beef Soup
searchkeys = ['小董牛肉湯爐', 'Win Chang Beef Soup Anping Main Shop', '豪牛牛肉湯（售完為止)', '新鮮牛肉湯(東門店)', '伍鍋貳牛 台南溫體牛肉湯/個人鍋 鴛鴦鍋/聚餐台南美食', '阿家牛肉湯&火鍋（營業時間以牛肉售完為止', 'Xiluodian Beef Soup', '樑記正老店牛肉湯', '阿杰溫體牛肉湯（每天售完為止）', '旗哥牛肉湯']

# test: Dessert
#searchkeys = ['起士公爵未來飲食研究所-東橋門巿生活健康館', '時之幸福輕手工蛋捲（開放加盟中）南美館概念店', '躺著就好｜甜點工作室 - 磅蛋糕、台式鹹派專賣(欲購買請來電或洽粉專詢問)', '娟娟甜點窩', 'D.D Lai Croffle（營業日請參閱FB/IG最新動態）']


results = {}

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(search, key) for key in searchkeys]

print(results)

# ↓ if you wanna burn your pc
#threads = []
#for key in searchkeys:
#    thread = threading.Thread(target=search, args=(key,))
#    threads.append(thread)
#    thread.start()

#for thread in threads:
#    thread.join()
