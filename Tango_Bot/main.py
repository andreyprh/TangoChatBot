import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from config import API_TOKEN, UNSPLASH_ACCESS_KEY
import keyboards
from logger import setup_logger

# Настраиваем логгер
logger = setup_logger()

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# States
class Form(StatesGroup):
    name = State()
    phone = State()
    service = State()
    level = State()
    confirmation = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    logger.info(f"Пользователь {message.from_user.id} начал диалог")
    await state.clear()  # На всякий случай очищаем состояние
    await message.reply(
        "Здравствуйте! Я Танго, бот консультант. Моя работа - сориентировать Вас по нашим услугам. Введите, пожалуйста, свое имя.",
        reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.name)


@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    logger.info(f"Пользователь {message.from_user.id} ввел имя: {message.text}")
    await state.set_state(Form.phone)
    await message.reply("Оставьте номер телефона, если хотите, чтобы Вам перезвонили.")


@dp.message(Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    logger.info(f"Пользователь {message.from_user.id} ввел телефон: {message.text}")
    await state.set_state(Form.service)
    user_data = await state.get_data()
    await message.reply(f"Что Вас интересует, {user_data['name']}? Выберите из представленных вариантов:",
                        reply_markup=keyboards.get_service_keyboard())


async def get_random_tango_photo():
    async with aiohttp.ClientSession() as session:
        url = f"https://api.unsplash.com/photos/random?query=tango&client_id={UNSPLASH_ACCESS_KEY}"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data['urls']['regular']
    return None


@dp.message(Form.service)
async def process_service(message: types.Message, state: FSMContext):
    if message.text == "Случайное танго-фото":
        photo_url = await get_random_tango_photo()
        if photo_url:
            await message.answer_photo(photo_url, caption="Танго прекрасно...")
        else:
            await message.answer("К сожалению, не удалось загрузить фото. Попробуйте еще раз.")
        return

    if message.text not in ["Групповые занятия", "Индивидуальные занятия", "Постановочный танец",
                            "Подарочный сертификат"]:
        await message.reply("Пожалуйста, выберите один из предложенных вариантов.")
        return

    await state.update_data(service=message.text)
    logger.info(f"Пользователь {message.from_user.id} выбрал услугу: {message.text}")
    await state.set_state(Form.level)
    await message.reply("Оцените Ваш уровень:", reply_markup=keyboards.get_level_keyboard())


@dp.message(Form.level)
async def process_level(message: types.Message, state: FSMContext):
    if message.text not in ["Начинающий", "Продвинутый"]:
        await message.reply("Пожалуйста, выберите один из предложенных вариантов.")
        return
    await state.update_data(level=message.text)
    logger.info(f"Пользователь {message.from_user.id} указал уровень: {message.text}")
    await state.set_state(Form.confirmation)
    user_data = await state.get_data()
    await message.reply(
        f"Итак, информация о Вас:\n"
        f"Имя: {user_data['name']}\n"
        f"Телефон: {user_data['phone']}\n"
        f"Ваш выбор: {user_data['service']}\n"
        f"Ваш уровень: {user_data['level']}\n"
        f"Все верно?",
        reply_markup=keyboards.get_confirmation_keyboard()
    )


@dp.message(Form.confirmation)
async def process_confirmation(message: types.Message, state: FSMContext):
    if message.text == "Да":
        logger.info(f"Пользователь {message.from_user.id} подтвердил информацию")
        await message.reply("Спасибо за обращение! Вам перезвонят.", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        await cmd_start(message, state)
    elif message.text == "Нет":
        logger.info(f"Пользователь {message.from_user.id} не подтвердил информацию, начинаем заново")
        await message.reply("Хорошо, давайте начнем сначала.", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        await cmd_start(message, state)
    else:
        await message.reply("Пожалуйста, выберите 'Да' или 'Нет'.")


async def main():
    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())