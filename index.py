#  Основой модуль программы

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from os import getenv

# управление базой данных
import db


#  токен управления ботом
TOKEN: str = getenv('TOKEN')
#  id  пользователя
ID_USER: int = int(getenv('ID_TLGM'))


#  инициализация диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



#  проверка id пользователя
def is_user_dec(func):
    async def wrapper(message):
        if message['from']['id'] != ID_USER:
            return await message.reply('Вы не зарегистрированы\n В доступе отказано!')
        else:
            return await func(message)
    return wrapper



#  определение типа операции
def query_analysis(message):

    if message.text[0] in '-+':
        data = message.text.strip(' ').split(' ', 2)

        if data[2].isnumeric() and not data[1].isnumeric():
            data[1], data[2] = int(data[2]), data[1]

        data[1] = int(data[1])
        data.append(str(message.date))

        return data



# справка по работе с ботом
@dp.message_handler(commands=['help'])
async def enter_help_command(message):

    text = "Введите запрос, например:\n-1800 продукты\n+40000 зп"

    await message.reply(text)


@dp.message_handler()
@is_user_dec
async def enter_start_bot_dialog(message: types.Message):

    data = query_analysis(message)

    if data:

        if db.write_to_db(data):
            await message.reply('Транзакция записана')
        else:
            await message.reply('Ошибка записи в базу')

    else:
        await message.reply('Не понял, введите /help для спраки\nи посмотрите как писать комманды')



#  программа
if __name__ == "__main__":


    executor.start_polling(dp)
