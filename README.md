# 數獨產生器 (Sudoku Generator)

這是一個基於 Python 的智能數獨產生器，具備邏輯難度分級、網頁介面以及列印功能。

## ✨ 特色

*   **真正的邏輯分級**：
    *   **Simple (簡單)**：單格/單行直覺可解 (Naked/Hidden Singles)。
    *   **Medium (中等)**：需運用區塊排除法 (Pointing Pairs)。
    *   **Hard (困難)**：需運用高級技巧如 X-Wing 才能解開。
*   **網頁介面**：提供友善的 UI，可設定數量與難度。
*   **支援列印**：一鍵產生適合 A4 列印的排版，並附帶**解答頁 (Answer Key)**。
*   **高效能**：優化的演算法，快速生成高品質題目。

## 🛠️ 安裝方式

本專案使用 [Poetry](https://python-poetry.org/) 進行套件管理，並建議搭配 [pyenv](https://github.com/pyenv/pyenv) 使用。

1.  **環境確認**
    確認已安裝 Python 3.10+ 與 Poetry。

2.  **安裝依賴**
    ```bash
    poetry install
    ```

## 🚀 使用方式

### 1. 啟動網頁介面 (推薦)

這是最方便的使用方式，適合一般使用者與列印需求。

```bash
poetry run python run_web.py
```

啟動後，請用瀏覽器打開：[http://127.0.0.1:5001](http://127.0.0.1:5001)

*   選擇 **Difficulty (難度)**。
*   輸入 **Count (數量)**。
*   按下 **Generate**。
*   按下 **Print** (或 Ctrl+P)：系統會自動分頁，第一頁為題目，第二頁為解答。

### 2. 命令列模式 (CLI)

如果你想在終端機直接產生題目：

```bash
poetry run sudoku
```

### 3. 執行測試與驗證

執行自動化測試與生成腳本：

```bash
# 執行單元測試
poetry run pytest tests/

# 執行生成驗證腳本
poetry run python scripts/check.py
```

## 📂 專案結構

*   `src/sudoku/`：核心程式碼
    *   `core.py`：數獨基礎邏輯與回溯法。
    *   `solver.py`：邏輯解題機 (負責判斷難度)。
    *   `generator.py`：題目生成器。
    *   `app.py`：Flask 網頁伺服器。
    *   `templates/`：網頁前端模板。
*   `scripts/`：工具腳本 (check.py, benchmark.py)。
*   `tests/`：測試程式碼。

## 📝 開發筆記

*   難度判斷是基於人類解題技巧，而非單純的空格數量。
*   Hard 難度的題目生成較為耗時，因為需要隨機嘗試直到出現 X-Wing 結構，若嘗試次數過多系統會自動返回當前找到最難的題目。

---
Created by Antigravity
