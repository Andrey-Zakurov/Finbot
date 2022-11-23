#  Основой модуль программы

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from os import getenv

# управление базой данных
import db


#  токен управления ботом
#  id  пользователя
TOKEN: str = getenv('TOKEN')
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



#
def query_analysis_and_create_tuple_for_db(message):

    text = message.text.strip()
    ret = []
    if text[0] in '+-':
        ret = [word.strip() for word in text[1:].strip().split(' ', 1)]
        ret.insert(0, text[0])
        ret.append(str(message.date))
        print(ret)
        if len(ret) == 4:
            print(tuple(ret))
            return tuple(ret)




# справка по работе с ботом
@dp.message_handler(commands=['help'])
async def enter_help_command(message):

    text = "Введите запрос, например:\n-1800 продукты\n+40000 зп"

    await message.reply(text)


# views expenses
@dp.message_handler(commands=['expenses'])
@is_user_dec
async def print_last_expens(message: types.Message):
    exp = db.get_list_expens()
    await message.reply(exp)



# views expenses
@dp.message_handler(commands=['incom'])
@is_user_dec
async def print_last_incom(message: types.Message):
    exp = db.get_list_incom()
    await message.reply(exp)


@dp.message_handler(commands=['balance'])
@is_user_dec
async def print_balance(message: types.Message):
    return message.reply(db.get_balance())


@dp.message_handler()
@is_user_dec
async def enter_start_bot_dialog(message: types.Message):

    data =  query_analysis_and_create_tuple_for_db(message)
    if data:

        if db.write_to_db(data):
            await message.reply('Транзакция записана')
        else:
            await message.reply('Ошибка записи в базу')

    else:
        await message.reply('Не понял, введите /help для спраки\nи посмотрите как писать комманды')

# Сделай кнопки + - и отчеты(последние пять транзакций, и общее сальдо)


#  программа
if __name__ == "__main__":


    executor.start_polling(dp)
