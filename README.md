# RemindGabilBot

Telegram bot, который присылает напоминания по расписанию.

## Как работает

- Бот принимает команду `/remind ДД.ММ ЧЧ:ММ текст`  
- В указанное время присылает напоминание в Telegram  

## Переменные окружения

- `TOKEN` — токен от @BotFather (обязательно для работы бота)

## Зависимости

- Python 3
- aiogram
- apscheduler

## Запуск локально

```bash
pip install aiogram apscheduler
python3 main.py

