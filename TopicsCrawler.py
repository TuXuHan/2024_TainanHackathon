from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from openai import OpenAI

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
client = OpenAI(api_key='YOUR_OPENAI_API_KEY')

url = 'https://www.google.com.tw/maps/@23.546162,120.6402133,8z?hl=zh-TW'
driver.get(url)

searchkeys = ['納咖啡（當日營業時間請看IG限動）', '日澗咖啡', 'Life Tree Coffee', '浮游咖啡（店休日及營業時間以IG公告為主）', 'July 8th Cafe']

AllTopics = []

for key in searchkeys:
    searchbox = driver.find_element(By.ID, 'searchboxinput')
    searchbox.send_keys(key)

    searchbtn = driver.find_element(By.CLASS_NAME, 'mL3xi')
    searchbtn.click()

    reviewsbtn = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(3) > div > div > button:nth-child(2)'))
    )
    reviewsbtn.click()

    #Alltopics = WebDriverWait(driver, 3).until(
    #    EC.visibility_of_element_located((By.CLASS_NAME, 'e2moi'))
    #)
    #Alltopics.click()


    topics = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'uEubGf.fontBodyMedium'))
    )
    topicsnum = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'bC3Nkc.fontBodySmall'))
    )

    Topics = {key.text: value.text for key, value in zip(topics[1:], topicsnum)}

    for k, v in Topics.items():
        print(k, ':', v, '則評論')
        AllTopics.append(k)
    
    Closebtn = driver.find_element(By.CLASS_NAME, 'yAuNSb.vF7Cdb')
    Closebtn.click()
    

content = '以下是根據餐廳評論歸納出來的關鍵字，請你根據這些關鍵字挑選這些餐廳的10個最有代表性的繁體中文相關詞：'

for t in AllTopics:
    content += t + '、'

reply = client.chat.completions.create(
model="gpt-4o-mini",
messages=[
    {"role": "system", "content": content},
]
).choices[0].message.content

print(AllTopics)
print(reply)