# 本機 MP3 語音轉文字（Whisper + Streamlit）

## 1) 下載/複製專案
git clone <你的 repo>
cd <repo-root>

## 2) 建立虛擬環境並啟用
Windows
'''
python -m venv venv
venv\Scripts\activate
'''

macOS / Linux
'''
python -m venv venv
source venv/bin/activate
'''

## 3) 安裝相依套件（Python 3.13 請先裝 audioop-lts）
'''
python -m pip install --upgrade pip
pip install -r requirements.txt
'''
如果你是 Python 3.13，請先
'''
pip install audioop-lts
'''

### 4)執行
'''
streamlit run st_app.py
'''
瀏覽器會自動開啟頁面（通常是 http://localhost:8501）。
上傳音檔 → 設定語言（或用 auto）→ 轉寫 → 下載 TXT/SRT。
