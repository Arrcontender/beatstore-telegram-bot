import time
import logging

from aiogram import Bot, Dispatcher, executor, types
from beats.beats_list import beats_dict
from details.details import REQUISITES, STORES, TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from db.db_commands import register_user, show_all_beats
from db.db_beats_init import init_beats
from aiogram.dispatcher import FSMContext


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class DataInput(StatesGroup):
    genre_state = State()


@dp.message_handler(commands=['init'])
async def admin_init_all_beats(message: types.Message):
    init = init_beats()
    if init:
        await message.answer('All beats were initialized!')
    else:
        await message.answer('Oops... beats were not initialized')


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
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


@dp.message_handler(commands=['genres'])
async def genres_handler(message: types.Message):
    for x in beats_dict.keys():
        await message.answer(f'<i>{x}</i>', parse_mode='html')
        await DataInput.genre_state.set()


@dp.message_handler(state=DataInput.genre_state)
async def concrete_genre_handler(message: types.Message, state: FSMContext):
    await message.answer('Wait a second...')
    r = message.text
    if r in beats_dict.keys():
        await bot.send_audio(message.from_user.id,
                             audio=types.InputFile(beats_dict[r]))
    await state.finish()


# FIXME: need to fix uploading file from URL
@dp.message_handler(commands=['beats'])
async def beats_handler(message: types.Message):
    all_beats = show_all_beats()
    for i in all_beats:
        await bot.send_audio(message.from_user.id, audio=types.InputFile(i[1]), caption=i[0])


@dp.message_handler(commands=['reqs'])
async def reqs_handler(message: types.Message):
    x = '\n'.join(REQUISITES)
    await message.answer(f"{message.from_user.full_name}, "
                         f"here is my payments details to purchase beats or "
                         f"donates: "
                         f"{x}",
                         parse_mode='html')


@dp.message_handler(commands=['links'])
async def links_handler(message: types.Message):
    x = '\n'.join(STORES)
    await message.answer(f"{message.from_user.full_name}, "
                         f"here is link to my stores on web:\n{x}",
                         parse_mode='html')


if __name__ == '__main__':
    executor.start_polling(dp)
