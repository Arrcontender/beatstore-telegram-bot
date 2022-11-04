import time
import logging
from db.db_commands import register_user, \
    show_all_beats, filter_by_genre_from_db
from db.db_beats_init import init_beats
from details.details import REQUISITES, STORES, TOKEN

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class DataInput(StatesGroup):
    genre_state = State()


@dp.message_handler(commands=['init'])
async def admin_init_all_beats(message: types.Message):
    """ Init database table with beats (command for owner) """
    init = init_beats()
    if init:
        await message.answer('All beats were initialized!')
    else:
        await message.answer('Oops... beats were not initialized')


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    """ Command to register new user and start bot """
    user = register_user(message)
    if user:
        await message.answer('You successfully registered!')
    else:
        await message.answer('You already have been registered!')
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')

    await message.answer(f"<b>Hello, <i>{user_full_name}</i>! "
                         f"Welcome to Ambrosko's Beat Store.</b>\n\n"
                         f"Here you can listen to my instrumentals, "
                         f"choose the ones you like the most and buy them. "
                         f"Also you can donate me some money here :)\n\n"
                         f"Enter <i>/store</i> to enter the store, "
                         f"<i>/reqs</i> to see payments details, "
                         f"<i>/links</i> to see stores on the internet, "
                         f"enter <i>/donate</i> to donate",
                         parse_mode='html')


@dp.message_handler(commands=['store'])
async def store_handler(message: types.Message):
    await message.answer(f"{message.from_user.full_name}, "
                         f"enter <i>/genres</i> "
                         f"to see beats sorted by genres "
                         f"or <i>/beats</i> to see all instrumentals",
                         parse_mode='html')


@dp.message_handler(commands=['beats'])
async def beats_handler(message: types.Message):
    """ Send all beats to user with additional information """
    all_beats = show_all_beats()
    for i in all_beats:
        await bot.send_audio(message.from_user.id,
                             audio=types.InputFile(i['url']),
                             caption=i['genre'])
        await message.answer(f'Leasing: {i["leasing"]}\n'
                             f'Exclusive: {i["exclusive"]}')


@dp.message_handler(commands=['genres'])
async def genres_handler(message: types.Message):
    """ Receive message about genre of the beat from user """
    all_beats = show_all_beats()
    print(all_beats)
    for i in all_beats:
        await message.answer(f'<i>{i["genre"]}</i>', parse_mode='html')
        await DataInput.genre_state.set()


@dp.message_handler(state=DataInput.genre_state)
async def concrete_genre_handler(message: types.Message, state: FSMContext):
    """ Send beats by genre to user with additional information """
    await message.answer('Wait a second...')
    r = message.text
    beats_by_genre = filter_by_genre_from_db(r)
    print(beats_by_genre)
    for i in beats_by_genre:
        print(i)
        await bot.send_audio(message.from_user.id,
                             audio=types.InputFile(i['url']))
        await message.answer(f'Leasing: {i["leasing"]}\n'
                             f'Exclusive: {i["exclusive"]}')
    await state.finish()


@dp.message_handler(commands=['reqs'])
async def reqs_handler(message: types.Message):
    """ Send reqs to user with additional information """
    x = '\n'.join(REQUISITES)
    await message.answer(f"{message.from_user.full_name}, "
                         f"here is my payments details to purchase beats or "
                         f"donates: "
                         f"{x}",
                         parse_mode='html')


@dp.message_handler(commands=['links'])
async def links_handler(message: types.Message):
    """ Send beat stores from web to user with additional information """
    x = '\n'.join(STORES)
    await message.answer(f"{message.from_user.full_name}, "
                         f"here is links to my stores on web:\n{x}",
                         parse_mode='html')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
