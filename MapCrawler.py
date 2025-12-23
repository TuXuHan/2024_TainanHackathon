from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import googlemaps
import folium

#driver = webdriver.Chrome()

map = googlemaps.Client(key = 'AIzaSyAiBroOElwIbiRMwUud5LQAg_6UwWOafJA')

MaxItemNum = 30

#searchword = input('搜尋關鍵字：')
#print('你要搜尋的是：', searchword)

#keyword = '台南 牛肉湯'

geocode_result = map.geocode('Tainan, 東區')[0]
location = geocode_result['geometry']['location']

#print(location)

#map = folium.Map(location=[22.98133, 120.2224227], zoom_start=13)

#folium.Marker(
#    location=[22.98133, 120.2224227],
#    popup='Tainan',
#).add_to(map)

#map.save("map.html")

search_result = []

#search_result = map.places_nearby(location, keyword=searchword, radius=50000)
result = map.places_nearby(location, keyword='牛肉湯', radius=2000)
#print(result['results'])
search_result.extend(result['results'])
next = result['next_page_token']
#print(result)

while len(search_result) < MaxItemNum:
    time.sleep(2)
    result = map.places_nearby(location, keyword='牛肉湯', radius=2000, page_token = next)
#    print(result)
    search_result.extend(result['results'])
    next = result.get('next_page_token')

print(search_result[0])

#print(search_result)

#print(search_result[0]['photos'][0]['photo_reference'])
#photo = map.places_photo(search_result[0]['photos'][0]['photo_reference'], 100, 100)
#photo_data = BytesIO(photo.content)
#encoded_photo = base64.b64encode(photo_data.getvalue()).decode('utf-8')
#print(photo)
#image_url = f"data:image/jpeg;base64,{encoded_photo}"

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
    rate_w = 0.7
    reviews_w = 0.3
    return (rate*rate_w + reviews*reviews_w)

for place in search_result:
    place['score'] = scorecounter(place['normalized_rating'], place['normalized_reviews'])

search_result = sorted(search_result, key=lambda x: x['score'], reverse=True)

for place in search_result:
    print(place['name'], place['rating'], place['user_ratings_total']) #, place['score']) 

