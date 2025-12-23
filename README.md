# 2024 台南黑客松 - 主題美食搜尋系統

一個基於 Google Maps API 和 AI 的台南美食搜尋與分析系統，能夠搜尋特定主題的餐廳、爬取評論，並使用 AI 生成餐廳特色標籤。

## 專案簡介

本專案是一個整合 Google Maps 搜尋、Selenium 網頁爬蟲和 OpenAI API 的美食搜尋平台，專為台南地區設計。系統可以：

- 根據關鍵字搜尋台南地區的餐廳
- 自動爬取 Google Maps 評論
- 使用 AI 分析評論並生成餐廳特色標籤（Hashtag）
- 提供互動式地圖介面顯示搜尋結果
- 根據評分和評論數進行智能排序

## 功能特色

### 1. 餐廳搜尋
- 支援關鍵字搜尋（如：牛肉湯、咖啡廳等）
- 可指定搜尋店家數量
- 自動過濾重複店家
- 顯示店家照片、評分、評論數、營業狀態和區域資訊

### 2. 智能評分系統
- 結合評分（權重 60%）和評論數（權重 40%）進行綜合評分
- 自動正規化數據並排序

### 3. AI 標籤生成
- 自動爬取 Google Maps 評論
- 使用 OpenAI GPT 模型分析評論內容
- 生成三個繁體中文特色標籤

### 4. 區域搜尋
- 支援台南各行政區搜尋
- 目前預設搜尋區域：東區、中西區、北區、南區、安平區

## 技術架構

### 後端
- **FastAPI**: Web 框架
- **Google Maps API**: 地點搜尋與地理編碼
- **Selenium**: 網頁爬蟲（爬取 Google Maps 評論）
- **OpenAI API**: AI 評論分析與標籤生成
- **BeautifulSoup**: HTML 解析

### 前端
- HTML/CSS/JavaScript
- 互動式地圖介面
- 響應式設計

### 爬蟲模組
- `MapCrawler.py`: 地圖資料爬取測試
- `ReviewsCrawler.py`: 評論爬取功能
- `TopicsCrawler.py`: 主題標籤爬取
- `Threading.py`: 多執行緒爬蟲實作

## 安裝與設定

### 環境需求
- Python 3.8+
- Chrome 瀏覽器
- ChromeDriver（已包含在專案中，或使用 webdriver-manager 自動下載）

### 安裝步驟

1. **克隆專案**
```bash
git clone <repository-url>
cd 2024_TainanHackathon
```

2. **安裝 Python 套件**
```bash
pip install fastapi uvicorn googlemaps selenium beautifulsoup4 openai webdriver-manager pydantic
```

3. **設定 API 金鑰**

在 `main.py` 中設定您的 API 金鑰：

```python
# 第 37 行：設定 Google Maps API 金鑰
map = googlemaps.Client(key = 'YOUR_GOOGLE_MAPS_API_KEY')

# 第 46、251、338 行：設定 OpenAI API 金鑰
client = OpenAI(api_key='YOUR_OPENAI_API_KEY')
```

4. **啟動伺服器**
```bash
uvicorn main:app --reload
```

5. **開啟前端介面**
- 主頁面：`http://localhost:8000/Home/`
- 評論頁面：`http://localhost:8000/Review-all/`

## API 端點

### POST `/search`
搜尋餐廳

**請求格式：**
```json
{
  "searchword": "牛肉湯",
  "MaxItemNum": 20
}
```

**回應：** HTML 格式的餐廳列表

### POST `/hashtag`
生成餐廳特色標籤

**請求格式：**
```json
{
  "searchword": "小董牛肉湯爐",
  "reviewsnum": 100
}
```

**回應：** HTML 格式的標籤列表

## 專案結構

```
2024_TainanHackathon/
├── main.py                 # FastAPI 主程式
├── MapCrawler.py           # 地圖爬蟲測試
├── ReviewsCrawler.py       # 評論爬蟲
├── TopicsCrawler.py        # 主題爬蟲
├── Threading.py            # 多執行緒爬蟲
├── CrawlerTest.py          # 爬蟲測試
├── Prototype/              # 前端原型
│   ├── index.html
│   ├── Prototype.css
│   ├── Prototype.js
│   └── Database.js
├── Review-all/             # 評論頁面
│   ├── index.html
│   ├── Review.css
│   ├── Review.js
│   └── Database.js
└── Client/                 # 客戶端檔案
    ├── map.html
    ├── user.css
    └── user.js
```

## 使用說明

1. **搜尋餐廳**
   - 在搜尋框輸入關鍵字（如：牛肉湯、咖啡廳）
   - 調整搜尋店家數量滑桿
   - 點擊「搜尋」按鈕

2. **查看結果**
   - 搜尋結果會顯示在右側面板
   - 每個結果包含：照片、名稱、評分、評論數、區域、營業狀態
   - 點擊店家名稱可查看詳細資訊

3. **生成標籤**
   - 點擊特定店家可觸發 AI 標籤生成
   - 系統會自動爬取評論並分析生成特色標籤

## 注意事項

⚠️ **重要提醒**

1. **API 金鑰安全**
   - 請勿將 API 金鑰提交到公開版本控制系統
   - 建議使用環境變數或設定檔管理金鑰

2. **爬蟲使用規範**
   - 請遵守 Google Maps 的使用條款
   - 避免過於頻繁的請求
   - 建議在開發環境中使用

3. **ChromeDriver**
   - 確保 Chrome 瀏覽器版本與 ChromeDriver 相容
   - 或使用 `webdriver-manager` 自動管理驅動程式

4. **API 費用**
   - Google Maps API 和 OpenAI API 皆為付費服務
   - 請注意 API 使用量以避免超額費用

## 開發團隊

2024 台南黑客松參賽專案

## 授權

本專案僅供學習與研究使用。

## 未來改進方向

- [ ] 整合資料庫儲存搜尋結果
- [ ] 實作使用者收藏功能
- [ ] 優化爬蟲效能與穩定性
- [ ] 增加更多篩選條件（評分、距離等）
- [ ] 實作地圖視覺化顯示
- [ ] 增加評論情感分析
- [ ] 支援多語言介面

## 聯絡資訊

如有問題或建議，歡迎提出 Issue 或 Pull Request。

