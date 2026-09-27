import logging
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


TELEGRAM_BOT_TOKEN = _require_env("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = _require_env("GEMINI_API_KEY")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-flash-latest")
SYSTEM_PROMPT = os.environ.get(
    "ASSISTANT_SYSTEM_PROMPT",
    "You are a helpful, concise personal assistant reachable over Telegram.",
)
MAX_HISTORY_MESSAGES = 20

client = genai.Client(api_key=GEMINI_API_KEY)
histories: dict[int, list[dict]] = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    histories[update.effective_chat.id] = []
    await update.message.reply_text(
        "嗨,我是你的專屬 AI 助手,直接打字跟我說話就可以了。\n"
        "用 /reset 可以清空對話記錄。"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    histories[update.effective_chat.id] = []
    await update.message.reply_text("對話記錄已清空。")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_text = update.message.text
    history = histories.setdefault(chat_id, [])

    history.append({"role": "user", "parts": [{"text": user_text}]})
    del history[:-MAX_HISTORY_MESSAGES]

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT, max_output_tokens=1024
            ),
        )
        reply_text = response.text
    except Exception:
        logger.exception("Gemini API call failed")
        history.pop()
        await update.message.reply_text("抱歉,剛剛請求 AI 服務時發生錯誤,請稍後再試一次。")
        return

    history.append({"role": "model", "parts": [{"text": reply_text}]})
    await update.message.reply_text(reply_text)


def main() -> None:
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot starting (polling mode)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
