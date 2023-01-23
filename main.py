import aiogram
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.utils.callback_data import CallbackData
from aiogram.utils import executor

# Конфигурация бота
bot = aiogram.Bot(token='Не забудь токен указать')
dp = Dispatcher(bot)

# Кнопка "Старт"
start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.add(KeyboardButton('Start'))

# Регистрация пользователя
registration_cb = CallbackData('registration', 'phone')

# Словарь для хранения зарегистрированных пользователей
registered_users = {}

@dp.message_handler(commands=['start'])
async def start_command(message):
    if message.from_user.id not in registered_users:
        # Запрос номера телефона
        await message.reply("Please enter your phone number to register:", reply_markup=registration_cb.new())
    else:
        # Если пользователь зарегистрирован, отправляем сообщение
        await message.reply("Welcome back!")

@dp.callback_query_handler(registration_cb.filter(phone=lambda c: c.data))
async def process_registration(callback_query):
    # Получаем номер телефона из запроса
    phone = callback_query.data

    # Добавляем пользователя в список зарегистрированных
    registered_users[callback_query.from_user.id] = phone

    # Отправляем сообщение об успешной регистрации
    await callback_query.message.answer("You have been successfully registered.")

@dp.message_handler()
async def process_message(message):
    if message.from_user.id in registered_users:
        # Если пользователь зарегистрирован, обрабатываем его сообщение
        await message.reply("You're registered, your message is: {}".format(message.text))
    else:
        # Если пользователь не зарегистрирован, отправляем сообщение об этом
        await message.reply("You're not registered, please press /start and enter your phone number")

if __name__ == "__main__":
    executor.start_polling(dp)