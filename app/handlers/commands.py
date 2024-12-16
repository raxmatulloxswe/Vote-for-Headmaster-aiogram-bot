from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand

from app.utils.db_manager import db
from app.utils.states import VoteStateGroup
from app.keyboards.inline import inline_main_menu

router = Router()


@router.message(Command('start'))
async def start_command(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(VoteStateGroup.vote_director)
    await message.answer("""Olmaliq shaxridagi eng faol va ilgʻor maktab direktoriga OVOZ BERING!\n
    Eng koʻp ovoz toʻplagan maktab direktori Yangi yil bayrami arafasida “ENG NAMUNALI MAKTAB DIREKTORI - 2024” nominatsiyasi boʻyicha taqdirlanadi.\n
    Soʻrovnoma 2024-yil xx-dekabr soat xx:xxga qadar davom etadi.""", reply_markup=await inline_main_menu())


@router.message(Command('help'))
async def help_command(message: types.Message):
    await message.answer("Kerakli buyruqlar!\n/start - Start the bot\n/help - Get help\n /rank - Shows the scores")


@router.message(Command('check_state'))
async def check_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await message.answer(f"State: {current_state}")


@router.message(Command('rank'))
async def rank_command(message: types.Message):
    directors = await db.get_all_directors()

    ranking_message = "Direktorlarning reytingi:\n\n"
    for director in directors:
        print(director,)
        director_name = director['name']
        director_score = director['score']
        director_shool_num = director['school_number']
        ranking_message += f"{director_name}({director_shool_num}): {director_score} ball\n"

    await message.answer(ranking_message)


@router.message(Command('build'))
async def help_command(message: types.Message):
    await message.answer("https://t.me/raxmatulllox")


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish!"),
        BotCommand(command="help", description="Yordam haqida ma'lumot!"),
        BotCommand(command="rank", description="Reytingni ko'rsatuvchi command!"),
        # BotCommand(command="check_state", description="Qaysi stateda ekanligini ko'rsatadi!"),
    ]
    await bot.set_my_commands(commands)