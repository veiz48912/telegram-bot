import logging
import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from transformers import AutoModelForCausalLM, AutoTokenizer
from flask import Flask

# Створення Flask застосунку для роботи на порту
app = Flask(__name__)

# Завантаження моделі StarCoder
model_name = "bigcode/starcoder"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Функція генерації відповіді
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=200)  # Обмеження довжини відповіді
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Функція для обробки всіх повідомлень
def handle_message(update: Update, context: CallbackContext):
    try:
        user_input = update.message.text
        # Генерація відповіді від моделі
        response = generate_response(user_input)
        update.message.reply_text(response)  # Відправка відповіді користувачу
    except Exception as e:
        logging.error(f"Error while generating response: {e}")
        update.message.reply_text("Виникла помилка при генерації відповіді. Спробуйте ще раз.")

# Налаштування логування для дебагу
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Основна функція для налаштування Telegram-бота
def main():
    # Вставте токен вашого Telegram-бота
    TOKEN = "7699486025:AAGgmU_xf6mQ5UK3v9xSaVNYMWZ_8wkXEdE"  # Заміни на свій токен
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Обробка всіх текстових повідомлень
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

# Запуск Flask серверу
if __name__ == '__main__':
    # Отримуємо порт з середовища
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)  # Запуск Flask на зазначеному порту
