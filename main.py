from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import time
import googlemaps
import requests
import base64
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from openai import OpenAI
from collections import Counter
from bs4 import BeautifulSoup
import math
#import mysql.connector

app = FastAPI()


class SearchRequest(BaseModel):
    searchword: str
#    searchdistance: int
#    selectedRating: int
#    selectedAreas: list
    MaxItemNum: int

class HashtagRequest(BaseModel):
    searchword: str
    reviewsnum: int

map = googlemaps.Client(key = 'YOUR_GOOGLE_MAPS_API_KEY')
#MaxItemNum = 60

def TopicsCrawler(key):

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    client = OpenAI(api_key='YOUR_OPENAI_API_KEY')

    url = 'https://www.google.com.tw/maps/@23.546162,120.6402133,8z?hl=zh-TW'
    driver.get(url)

#    key = '小董牛肉湯爐'

    searchbox = driver.find_element(By.ID, 'searchboxinput')
    searchbox.send_keys(key)

    searchbtn = driver.find_element(By.CLASS_NAME, 'mL3xi')
    searchbtn.click()

    reviewsbtn = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(3) > div > div > button:nth-child(2)'))
    )
    reviewsbtn.click()

    #Alltopics = WebDriverWait(driver, 3).until(
    #    EC.visibility_of_element_located((By.CLASS_NAME, 'e2moi'))
    #)
    #Alltopics.click()

    topics = driver.find_elements(By.CLASS_NAME, 'uEubGf.fontBodyMedium')
    topicsnum = driver.find_elements(By.CLASS_NAME, 'bC3Nkc.fontBodySmall')

    Topics = {key.text: value.text for key, value in zip(topics[1:], topicsnum)}

    for k, v in Topics.items():
        print(k, ':', v, '則評論')

    result = [item.text for item in topics[1:]]
    
    return result

district_ec = {
    'East District': '東區', 'West Central District': '中西區', 'South District': '南區',
    'North District': '北區', 'Anping District': '安平區', 'Annan District': '安南區',
    'Yongkang District': '永康區', 'Guiren District': '歸仁區', 'Xinhua District': '新化區', 
    'Zuozhen District': '左鎮區', 'Yujing District': '玉井區', 'Nanxi District': '楠西區', 
    'Nanhua District': '南化區', 'Rende District': '仁德區', 'Guanmiao District': '關廟區', 
    'Longqi District': '龍崎區', 'Guantian District': '官田', 'Madou District': '麻豆區', 
    'Jiali District': '佳里區', 'Xigang District': '西港區', 'Qigu District': '七股區', 
    'Jiangjun District': '將軍區', 'Xuejia District': '學甲區', 'Beimen District': '北門區',
    'Xinying District': '新營區', 'Houbi District': '後壁區', 'Baihe District': '白河區',
    'Dongshan District': '東山區', 'Liujia District': '六甲區', 'Xiaying District': '下營區',
    'Liuying District': '柳營區', 'Yanshui District': '鹽水區', 'Shanhua District': '善化區',
    'Danei District': '大內區', 'Shanshang District': '山上區', 'Xinshi District': '新市區',
    'Anding District': '安定區'
}

def GetDistrict(address):
#    print(address)
    if not address:
        return None
    if ',' in address:
        parts = address.split(',')
        for part in parts:
            if "District" in part:
                return district_ec.get(part.strip(), None)
    
    space_parts = address.split(' ')
    for i, part in enumerate(space_parts):
        if "District" in part and i > 0:
            full_district = f"{space_parts[i-1]} {part}"
            return district_ec.get(full_district.strip(), None)
    return None

@app.get('/')
async def read_root():
    return {'message': 'Hello, World!'}

district_info = {'東區': 2.5, '中西區': 2, '北區': 2, '南區': 2, '安平區': 2.5}

'''                '永康區': 4, '安南區': 5, '安平區': 2.5, '新化區': 5, '沙崙區': 4, 
                '仁德區': 3.5, '歸仁區': 3.5, '新營區': 5, '鹽水區': 3.5, '白河區': 4.5,
                '柳營區': 3.5, '後壁區': 3, '東山區': 4, '麻豆區': 3.5, '下營區': 3.5,
                '六甲區': 3.5, '官田區': 3.5, '大內區': 4.5, '佳里區': 3.5, '學甲區': 3,
                '西港區': 3, '七股區': 3.5, '將軍區': 4, '北門區': 3.5, '新市區': 3.5,
                '善化區': 3.5, '安定區': 3.5, '山上區': 4, '玉井區': 4, '楠西區': 5,
                '南化區': 3.5, '左鎮區': 4}
'''

status = {'OPERATIONAL': '🟢 營業中', 'CLOSED_TEMPORARILY': '🟡 暫時歇業', 'CLOSED_PERMANENTLY': '🔴 永久歇業'}

@app.post('/search')
async def search(request: SearchRequest):

    '''
    search_result = []
    result = map.places_nearby(location, keyword=request.searchword, radius=request.searchdistance*1000)
    for r in result['results']:
        if float(r['rating']) > request.selectedRating:
            search_result.append(r)
    next = result.get('next_page_token')

    while len(search_result) < MaxItemNum:
        time.sleep(2)
        result = map.places_nearby(location, keyword=request.searchword, radius=request.searchdistance*1000, page_token = next)
        for r in result['results']:
            if float(r['rating']) > request.selectedRating:
                search_result.append(r)
        next = result.get('next_page_token')

    '''

    search_result_nu = []

#    for area in request.selectedAreas:

    for area, distance in district_info.items():
        geocode_result = map.geocode('Tainan,' + area)[0]
        location = geocode_result['geometry']['location']

        result = map.places_nearby(location, keyword=request.searchword, radius=distance*1000)
        for r in result['results']:
            r['district'] = GetDistrict(r['plus_code']['compound_code'])
            search_result_nu.append(r)

        next_page_token = result.get('next_page_token')

        while next_page_token and len(search_result_nu) < request.MaxItemNum:
            time.sleep(2)
            result = map.places_nearby(location, keyword=request.searchword, radius=distance*1000, page_token=next_page_token)
            for r in result['results']:
                if len(search_result_nu) >= request.MaxItemNum:
                    break
                r['district'] = GetDistrict(r['plus_code']['compound_code'])
                search_result_nu.append(r)
            next_page_token = result.get('next_page_token')

    search_result = []
    search_set = set()
#    print('總店家數:', len(search_result_nu))
    for item in search_result_nu:
        if item['name'] not in search_set:
            search_set.add(item['name'])
            search_result.append(item)

#    print(search_result[0])

    for i in range(len(search_result)):
        try:
            # if photo == True
            photo = map.places_photo(search_result[i]['photos'][0]['photo_reference'], 200, 200)
            photo_data = BytesIO()
            for chunk in photo:
                if chunk:
                    photo_data.write(chunk)
            
            photo_data.seek(0)
            encoded_photo = base64.b64encode(photo_data.read()).decode('utf-8')
            
            photo_url = f"data:image/jpeg;base64,{encoded_photo}"
            search_result[i]['photo_url'] = photo_url
        except (KeyError, IndexError, TypeError):
            search_result[i]['photo_url'] = '無'
    ReturnAll = ''

    ratings = [float(place['rating']) for place in search_result]
    reviews = [float(place['user_ratings_total']) for place in search_result]

    def normalize(data):
        min_val = min(data)
        max_val = max(data)
        return [(x - min_val) / (max_val - min_val) for x in data]

    normalized_ratings = normalize(ratings)
    normalized_reviews = normalize(reviews)

    for i in range(len(search_result)):
        search_result[i]['normalized_rating'] = normalized_ratings[i]
        search_result[i]['normalized_reviews'] = normalized_reviews[i]

    def scorecounter(rate, reviews):
        rate_w = 0.6
        reviews_w = 0.4
        return (rate*rate_w + reviews*reviews_w)

    for place in search_result:
        place['score'] = scorecounter(place['normalized_rating'], place['normalized_reviews'])

    search_result = sorted(search_result, key=lambda x: x['score'], reverse=True)

#    print('店家數:', len(search_result))

    for place in search_result:
        # use ID as reviews num?
        # at place-item-name
#        topics = TopicsCrawler(place['name'])
#        print(topics)

        ReturnAll += f"<div class='place-item'> <img src='{place['photo_url']}' alt='{place['name']} 的圖片' class='place-image' /> <div class='place-item-left'> <div class='place-item-name' data-name='{place['name']}' data-lat='{place['geometry']['location']['lat']}' data-lng='{place['geometry']['location']['lng']}' data-photo_url='{place['photo_url']}' data-rating='{place['rating']}' data-user_ratings_total='{place['user_ratings_total']}' data-status='{place['business_status']}' data-district='{place['district']}''>{place['name']}</div><div class='place-item-rating'>{place['rating']} <span class='star rated'>★</span> / {place['user_ratings_total']} 則評論</div><div class='place-item-status'><span class='place-item-district'>[ {place['district']} ]  </span> {status[place['business_status']]}</div></div><div class='place-item-right'><label class='place-check'><input type='checkbox'></label></div></div>"
#        ReturnAll += f"<div class='place-item'> <img src='{place['photo_url']}' alt='{place['name']} 的圖片' class='place-image' /> <div class='place-item-left'> <div class='place-item-name' data-name='{place['name']}' data-lat='{place['geometry']['location']['lat']}' data-lng='{place['geometry']['location']['lng']}' data-photo_url='{place['photo_url']}' data-rating='{place['rating']}' data-user_ratings_total='{place['user_ratings_total']}' data-status='{place['business_status']}'>{place['name']}</div><div class='place-item-rating'>{place['rating']} <span class='star rated'>★</span> / {place['user_ratings_total']} 則評論</div><div class='place-item-status'>{status[place['business_status']]}</div></div><div class='place-item-right'><label class='place-check'><input type='checkbox'></label></div></div>"

    return ReturnAll

def comments(num):
    return min(300, math.floor(num - math.log2(num)))

def HashtagCrawler(name, reviewnum):

    chrome_options = Options()
#    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    client = OpenAI(api_key='YOUR_OPENAI_API_KEY')

    url = 'https://www.google.com.tw/maps/@23.546162,120.6402133,8z?hl=zh-TW'
    driver.get(url)

    searchbox = driver.find_element(By.ID, 'searchboxinput')
    searchbox.send_keys(name)

    searchbtn = driver.find_element(By.CLASS_NAME, 'mL3xi')
    searchbtn.click()

    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    buttons = soup.find_all('button', attrs={'aria-label': True})
    reviewbuttons = [button for button in buttons if '評論' in button['aria-label']]
    rvbutton_xpath = f"//button[contains(@aria-label, '{reviewbuttons[0]['aria-label']}')]"

    reviewsbtn = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, rvbutton_xpath))
    )

    reviewsbtn.click()

    ReviewsMaxNum = math.ceil(comments(reviewnum))

    def words_count(text):
        text = [char for char in text if '\u4e00' <= char <= '\u9fff']
        counter = Counter(text)
        return len(counter)

    pane = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'm6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde'))
    )

    flag = True
    while flag:
        reviewcount = 0
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pane)
        try:
            FullTextbtn = driver.find_element(By.CLASS_NAME, 'w8nwRe.kyuRq')
            FullTextbtn.click()
        except:
            pass
        review = driver.find_elements(By.CLASS_NAME, 'wiI7pd')
        for r in review:
            if(words_count(r.text) > 10):
                reviewcount+=1
        if reviewcount >= ReviewsMaxNum:
            flag = False

    content = '以下是餐廳的評論，請你根據這些評論生成這個餐廳的三個繁體中文關鍵特色，格式為：xxx, xxx, xxx：'

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

    Closebtn = driver.find_element(By.CLASS_NAME, 'yAuNSb.vF7Cdb')
    Closebtn.click()

    driver.close()

    reply_list = [item.strip() for item in reply.split(',')]

    ReturnAll = ''

    for i in range(len(reply_list)):
        ReturnAll += f"<div class='hashtag'> # {reply_list[i]} </div>"

    return ReturnAll


@app.post('/hashtag')
async def search(request: HashtagRequest):

    chrome_options = Options()
#    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    client = OpenAI(api_key='YOUR_OPENAI_API_KEY')

    url = 'https://www.google.com.tw/maps/@23.546162,120.6402133,8z?hl=zh-TW'
    driver.get(url)

    searchbox = driver.find_element(By.ID, 'searchboxinput')
    searchbox.send_keys(request.searchword)

    searchbtn = driver.find_element(By.CLASS_NAME, 'mL3xi')
    searchbtn.click()

    time.sleep(2)

    try:
        results = WebDriverWait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'hfpxzc'))
        )

        if len(results) > 1:
            first_result = results[0]
            driver.execute_script("arguments[0].click();", first_result)  # 使用 JS 點擊

    except:
        pass

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    buttons = soup.find_all('button', attrs={'aria-label': True})
    reviewbuttons = [button for button in buttons if '評論' in button['aria-label']]
    rvbutton_xpath = f"//button[contains(@aria-label, '{reviewbuttons[0]['aria-label']}')]"

    reviewsbtn = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, rvbutton_xpath))
    )

    reviewsbtn.click()

    ReviewsMaxNum = 80 if request.reviewsnum > 80 else math.ceil(request.reviewsnum / 3)

    def words_count(text):
        text = [char for char in text if '\u4e00' <= char <= '\u9fff']
        counter = Counter(text)
        return len(counter)

    pane = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'm6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde'))
    )

    flag = True
    reviewcount = 0
    previous_height = driver.execute_script("return arguments[0].scrollHeight", pane)

    while flag:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pane)

        try:
            WebDriverWait(driver, 5).until(
                lambda driver: len(driver.find_elements(By.CLASS_NAME, 'wiI7pd')) > reviewcount
            )
        except:
            flag = False
            break

        try:
            FullTextbtn = driver.find_element(By.CLASS_NAME, 'w8nwRe.kyuRq')
            FullTextbtn.click()

        except:
            pass
    
        review = driver.find_elements(By.CLASS_NAME, 'wiI7pd')
        for r in review:
            if(words_count(r.text) > 10):
                reviewcount+=1
        if reviewcount >= ReviewsMaxNum:
            flag = False
            
        current_height = driver.execute_script("return arguments[0].scrollHeight", pane)
        if current_height == previous_height:
            flag = False

        previous_height = current_height


    content = '以下是餐廳的評論，請你根據這些評論生成這個餐廳的三個繁體中文相關詞，格式為：xxx, xxx, xxx：'

    for r in review:
        if(words_count(r.text) > 10):
            content += str(r.text)
    #        print(r.text)

    reply = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": content},
    ]
    ).choices[0].message.content
    
    print(reply)

    Closebtn = driver.find_element(By.CLASS_NAME, 'yAuNSb.vF7Cdb')
    Closebtn.click()

    driver.close()

    reply_list = [item.strip() for item in reply.split(',')]

    ReturnAll = ''

    for i in range(len(reply_list)):
        ReturnAll += f"<div class='hashtag'> # {reply_list[i]} </div>"

    return ReturnAll


app.mount('/Home', StaticFiles(directory='Prototype', html=True))
app.mount('/Review-all', StaticFiles(directory='Review-all', html=True))
