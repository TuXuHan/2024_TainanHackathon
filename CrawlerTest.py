from selenium import webdriver
from selenium.webdriver.common.by import By
from openai import OpenAI

driver = webdriver.Chrome()

client = OpenAI(api_key='YOUR_OPENAI_API_KEY')

url = 'https://aithon2024.goodideas-studio.com/topic-list/'
driver.get(url)

description = []
elements = driver.find_elements(By.CLASS_NAME, 'action-button-primary')
for element in elements:
    element.click()
    description.append(driver.find_element(By.CLASS_NAME, 'modal-body-description').text)
#    print('append')
    xbtn = driver.find_element(By.CLASS_NAME, 'btn-close')
    xbtn.click()
#print(description)



titles = driver.find_elements(By.CLASS_NAME, 'title')
#for title in titles:
#    print(title.text, end=' ')

content = '這是來自台南市政府'+titles[0].text+'的問題，以下是詳細描述，請生成一個可行的做法：'+elements[0].text

reply = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": content},
  ]
).choices[0].message.content

print(reply)

driver.close()