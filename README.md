# 本機 MP3 語音轉文字（Whisper + Streamlit）

## 1) 下載/複製專案
```sh
git clone https://github.com/BBrain778/MP3_To_Text.git
```

## 2) 建立虛擬環境並啟用
Windows
```sh
python -m venv venv
venv\Scripts\activate
```

macOS / Linux
```sh
python -m venv venv
source venv/bin/activate
```

## 3) 安裝相依套件（Python 3.13 請先裝 audioop-lts）
```sh
python -m pip install --upgrade pip
cd MP3_To_Text
pip install -r requirements.txt
```
如果你是 Python 3.13，請先
```sh
pip install audioop-lts
```

### 4)執行
```sh
streamlit run st_app.py
```
瀏覽器會自動開啟頁面（通常是 http://localhost:8501）。
上傳音檔 → 設定語言（或用 auto）→ 轉寫 → 下載 TXT/SRT。
