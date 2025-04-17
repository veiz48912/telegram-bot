import os
import logging
from flask import Flask, request
from transformers import AutoModelForCausalLM, AutoTokenizer
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Telegram Token і HF Token з environment
TELEGRAM_TOKEN = os.environ.get("7699486025:AAGgmU_xf6mQ5UK3v9xSaVNYMWZ_8wkXEdE")
HF_TOKEN = os.environ.get("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")

# Завантаження моделі
model_name = "bigcode/starcoder"
tokenizer = AutoTokenizer.from_pretrained(model_name, token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(model_name, token=HF_TOKEN)

# Flask app
app = Flask(__name__)

# Telegram bot setup
app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Обробка повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=256)
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    await update.message.reply_text(reply)

# Команда старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привіт! Я бот для написання професійних скриптів.")

# Додаємо хендлери
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Flask маршрут для вебхука
@app.route("/")
def home():
    return "Бот працює!"

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app_telegram.bot)
    app_telegram.update_queue.put(update)
    return "ok"

# Запуск Flask
if __name__ == "__main__":
    app.run(port=10000)
