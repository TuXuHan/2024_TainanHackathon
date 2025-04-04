# 2024_TainanHackathon
# 台南主題店家搜尋系統  

這是一個基於 **Python FastAPI** 的網頁應用，使用 `uvicorn` 作為主架構，並結合 **HTML、CSS、JavaScript** 前端技術

**專案特色**：
- 主題店家搜尋：透過網頁爬蟲收集台南市各類特色店家資訊
- AI 智能篩選：運用 OpenAI LLM 技術，為使用者與審核人員提供更完善的篩選建議
- 使用者友善介面：整合後端 API 與前端技術，提供流暢的店家搜尋與選擇體驗

此專案適用於「審核人員」與「一般使用者」，讓查找台南市特色店家變得更加直覺與高效

## 目錄結構
```
2024_TainanHackathon
│── __pycache__/
│── Client/
│── ProjectFiles/
│   │── index.html
│   │── map.html
│   │── user.css
│   │── user.js
│── Prototype/
│   │── Database.js
│   │── index.html
│   │── Prototype.css
│   │── Prototype.js
│── Review-all/
│   │── Database.js
│   │── index.html
│   │── Review.css
│   │── Review.js
│── chromedriver
│── CrawlerTest.py
│── draft.pages
│── main.py
│── map.html
│── MapCrawler.py
│── ReviewsCrawler.py
│── Threading.py
│── TopicsCrawler.py
│── user.py
```
