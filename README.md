# Telegram Gift Tracker Bot 🎁

Этот бот отслеживает появление новых подарков на Telegram Web и присылает уведомления в Telegram.

## Как использовать

1. Клонируй репозиторий
2. Установи зависимости:
   ```bash
   pip install python-telegram-bot telebot python-dotenv requests
   ```
3. Создай `.env` файл и добавь:
   ```env
   BOT_TOKEN=your_token_here
   CHAT_ID=your_chat_id_here
   ```
4. Запусти бота:
   ```bash
   python bot.py
   ```

Бот проверяет наличие новых подарков каждые 30 секунд. Если подарки появляются — сразу отправляет 10 уведомлений.