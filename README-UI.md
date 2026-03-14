# 🌐 Universal Multi-Agent Simulation Engine v3

這是一個基於領域無關、成本極低的 Agent 動態路由與壓縮架構打造的模擬平台。

## ✨ 快速啟動

在 GitHub 生態圈中，最直覺、對使用者最友好的方式就是提供一個 **Web 視覺化圖形介面 (Web UI)** 讓大家不需要去改動 `main.py` 程式碼即可開始體驗。為此，我們加入了 `Streamlit` 儀表板，只需幾個簡單的步驟，任何人即使 `git clone` 以後都能立即開始視覺化操作：

### 1. 安裝套件
請確認你的 Python 環境已經啟用：
```bash
pip install -r requirements.txt
```

### 2. 環境設定
建立 `.env` 檔案並填入金鑰，或是等一下在畫面上直接輸入：
```bash
cp .env.example .env
```

### 3. 啟動視覺化介面 (推薦做法 🚀)
執行以下指令啟動 Streamlit 介面：
```bash
streamlit run app.py
```
執行後，您的瀏覽器將會自動跳出一個 UI 畫面 (預設在 `http://localhost:8501`)，您可以在左側面板**直接輸入 Gemini API Key**、選擇劇本腳本、與調整回合參數，並在右側即時看到模型決策 Log 以及每一回合的**成本計價追蹤**。

### 4. 命令列啟動 (CLI)
如果您想使用無介面模式，或是需要寫腳本批量自動運行：
```bash
python main.py
```
