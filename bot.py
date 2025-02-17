from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import random
import os
from dotenv import load_dotenv

# Загружаем токен бота из .env файла
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список обращений
names = ["Анастасия", "Настена", "Настенька", "девочка моя", "ягодка моя", "богиня моя", "королева"]

# Список романтических и страстных сообщений
romantic_messages = [
    "ты, как восход солнца над морем, приносишь свет и тепло. 🌅",
    "твои глаза — глубокий океан страсти и тайны. 🌊",
    "ты невероятно женственная и сексуальная, как летняя ночь, полная тайн. 🌙",
    "твои губы — словно сладкий мёд, они манят и сводят с ума. 💋",
    "ты — волшебство в чистом виде, твоя энергия наполняет мир сиянием. ✨",
    "твоя улыбка — как тёплый солнечный луч, который греет мою душу. ☀️",
    "твоя грация и шарм оставляют неизгладимый след в сердцах. ❤️",
    "мои мысли о тебе — сладкий огонь, который я не хочу тушить. 🔥",
    "твои прикосновения — как электричество, пробегающее по коже. ⚡",
    "я бы растворился в тебе, как ночное небо в бесконечности звёзд. 🌌",
    "твои слова — это музыка, мелодия, что играет в моём сердце. 🎶",
    "если бы любовь была стихией, ты была бы бурей, завораживающей своей мощью. 🌪️",
    "твои губы — врата к наслаждению, которым я бы наслаждался вечно. 🔥",
    "ты — магия, которую невозможно объяснить, но которой невозможно сопротивляться. 🪄",
    "твой голос — как шелест листьев в тёплую ночь, убаюкивающий и чарующий. 🍃",
]

# Функция для отправки случайного романтического сообщения с обращением
async def send_romantic_message():
    if CHAT_ID:
        name = random.choice(names)  # Выбираем случайное обращение
        message = f"{name}, {random.choice(romantic_messages)}"  # Добавляем обращение в начало
        await bot.send_message(CHAT_ID, message)
    else:
        print("Chat ID не задан. Установите его с помощью команды /setchat.")

# Настройка планировщика с графиком 05:00 - 21:00 (по МСК)
async def start_scheduler():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_romantic_message, CronTrigger(hour="5-21", minute=0))  # Каждое начало часа
    scheduler.start()

# Обработка команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.reply("Привет, моя волшебница! ✨ Теперь я буду присылать тебе магические и страстные послания каждый час с 05:00 до 21:00! 💖")

# Обработка команды для установки chat_id
@dp.message(Command("setchat"))
async def set_chat_id(message: Message):
    global CHAT_ID
    CHAT_ID = message.chat.id
    with open('.env', 'a') as f:
        f.write(f"\nCHAT_ID={CHAT_ID}")
    await message.reply("Chat ID установлен! Теперь я буду присылать тебе романтические сообщения. 💖")

# Запуск бота
async def main():
    print("Бот запущен...")
    
    # Запуск планировщика
    await start_scheduler()
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
