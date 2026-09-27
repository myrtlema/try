# 專屬 AI 助手 (Telegram Bot)

用 Telegram 當介面、Claude API 當大腦的個人 AI 助手骨架。用途還沒定案,先讓它能在 Telegram 上聊起來,之後再依需求加功能(記憶、工具、特定任務等)。

## 運作方式

- `bot.py` 用 polling 模式跟 Telegram 要訊息,不需要對外開放網址或 webhook。
- 每個 Telegram 對話 (chat) 各自保留最近幾則訊息當記憶,重啟程式後會清空(純記憶體,沒有存檔)。
- `/start` 開始對話,`/reset` 清空目前對話記錄。

## 前置準備

1. **拿 Telegram Bot Token**:在 Telegram 找 [@BotFather](https://t.me/BotFather),傳 `/newbot`,依指示取名後會拿到一個 token。
2. **拿 Anthropic API Key**:到 [console.anthropic.com](https://console.anthropic.com/) 建立 API key。

## 設定環境變數

需要兩個變數:`TELEGRAM_BOT_TOKEN`、`ANTHROPIC_API_KEY`。

- **本機執行**:複製 `.env.example` 成 `.env`,填入對應的值(`.env` 已加入 `.gitignore`,不會被提交)。
- **在這個雲端環境執行**:到 session 標題列的「Cloud environment」選單裡按 Edit,新增這兩個環境變數,存檔後開新的 session 就會生效。

不要把 token 或 key 直接貼在對話訊息裡。

## 安裝與執行

```bash
pip install -r requirements.txt
python bot.py
```

程式跑起來後,直接在 Telegram 找到你剛建立的 bot,傳訊息測試。

## 客製化

- `ANTHROPIC_MODEL`:換用的模型,預設 `claude-sonnet-5`。
- `ASSISTANT_SYSTEM_PROMPT`:助手的系統提示詞,可以用來定義它的角色、語氣、專長。

## 部署成 24 小時在線的服務

這個雲端開發環境是暫時性的,不適合長期掛著跑。polling 模式的好處是不需要公開網址,可以直接部署到任何能長期跑一個 Python 程式的地方,例如 Railway、Render、Fly.io 或自己的伺服器。

## 之後可以加的方向

- 換 / 加其他聊天平台(WhatsApp、LINE、Discord)
- 對話記錄改成存資料庫,重啟不會消失
- 加工具(查天氣、讀自己的筆記、排程提醒等),讓它變成「特定任務助手」
