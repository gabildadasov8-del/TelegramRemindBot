import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import uuid

TOKEN = "8303674418:AAFDEKII7HKj8LlfLg8Nc_WzggcbKlV0Ins"

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# Хранилище напоминаний в памяти
reminders = {}

async def send_reminder(chat_id: int, reminder_id: str):
    reminder = reminders.get(reminder_id)
    if reminder:
        await bot.send_message(
            chat_id,
            f"⏰ *Напоминание:*\n{reminder['text']}",
            parse_mode="Markdown"
        )
        reminders.pop(reminder_id, None)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\n"
        "Я бот-напоминалка.\n\n"
        "Пример:\n"
        "`/remind 26.12 18:30 тренировка`\n\n"
        "Команды:\n"
        "/list — список напоминаний\n"
        "/delete ID — удалить\n"
        "/help — помощь",
        parse_mode="Markdown"
    )

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "📌 Формат напоминания:\n"
        "`/remind ДД.ММ ЧЧ:ММ текст`\n\n"
        "Пример:\n"
        "`/remind 27.12 09:00 учеба`\n\n"
        "/list — все напоминания\n"
        "/delete ID — удалить",
        parse_mode="Markdown"
    )

@dp.message(Command("remind"))
async def remind(message: types.Message):
    try:
        parts = message.text.split(maxsplit=3)
        date_part = parts[1]
        time_part = parts[2]
        text = parts[3]

        remind_time = datetime.strptime(
            f"{date_part} {time_part}", "%d.%m %H:%M"
        ).replace(year=datetime.now().year)

        if remind_time < datetime.now():
            await message.answer("❌ Это время уже прошло")
            return

        reminder_id = str(uuid.uuid4())[:8]

        reminders[reminder_id] = {
            "time": remind_time,
            "text": text
        }

        scheduler.add_job(
            send_reminder,
            trigger="date",
            run_date=remind_time,
            args=[message.chat.id, reminder_id]
        )

        await message.answer(
            f"✅ Напоминание сохранено\n"
            f"🆔 ID: `{reminder_id}`\n"
            f"⏰ {remind_time.strftime('%d.%m %H:%M')}",
            parse_mode="Markdown"
        )

    except Exception:
        await message.answer(
            "❌ Неверный формат\n"
            "Пример:\n"
            "`/remind 26.12 18:30 тренировка`",
            parse_mode="Markdown"
        )

@dp.message(Command("list"))
async def list_reminders(message: types.Message):
    if not reminders:
        await message.answer("📭 Напоминаний нет")
        return

    text = "📋 *Твои напоминания:*\n\n"
    for rid, r in reminders.items():
        text += f"🆔 {rid} — {r['time'].strftime('%d.%m %H:%M')} — {r['text']}\n"

    await message.answer(text, parse_mode="Markdown")

@dp.message(Command("delete"))
async def delete_reminder(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("❌ Укажи ID\nПример: `/delete a1b2c3d4`", parse_mode="Markdown")
        return

    rid = parts[1].strip()

    if rid in reminders:
        reminders.pop(rid)
        await message.answer("🗑 Напоминание удалено")
    else:
        await message.answer("❌ Напоминание не найдено")

async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



                     