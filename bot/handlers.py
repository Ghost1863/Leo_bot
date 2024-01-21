import os
from aiogram import Router, F
from aiogram.types import Message, WebAppInfo, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder,KeyboardButton,ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()
router=Router()

def webapp_builder()->InlineKeyboardBuilder:
    builder=InlineKeyboardBuilder()
    builder.button(text="Click as long as you can🦇🦇🦇",
                   web_app=WebAppInfo(url=os.getenv('REF')))
    return builder.as_markup()

@router.message(CommandStart())
async def start(message:Message) -> None:
    await message.answer(("<em><b>Challenge started💀</b></em>"),
                        reply_markup=webapp_builder(),
                         parse_mode='HTML')
    await message.delete()

@router.message(Command('help'))
async def help(message:Message)->None:
    await message.reply(os.getenv('COMMANDS'),parse_mode='HTML')

@router.message(Command('description'))
async def description(message:Message)->None:
    await message.answer(os.getenv('DESCR'))

@router.message(Command('food'))
async def cmd_food(message: Message)-> None:
    kb = [
        [KeyboardButton(text="Chicken")],
        [KeyboardButton(text="Meat")],
        [KeyboardButton(text="Fish")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                   resize_keyboard=True,
                                   input_field_placeholder = "Choose wisely")
    await message.answer("Choose the dish", reply_markup=keyboard)

@router.message(F.text.lower() == "chicken")
async def with_puree(message:Message):
    await message.reply("Let it be so🥱",reply_markup=ReplyKeyboardRemove())
    await message.answer_photo(photo='https://img.freepik.com/premium-photo/brown-hen-isolated-on-white-studio-shot_136670-3076.jpg')

@router.message(F.text.lower() == "meat")
async def without_puree(message:Message):
    await message.reply("Nice choice😊!",reply_markup=ReplyKeyboardRemove())
    await message.answer_photo(photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQj8pV6zokgWbJhdltrvc9GCNvRt_JeRFPflsktvSkgGw&s')

@router.message(F.text.lower() == "fish")
async def without_puree(message:Message):
    await message.reply("Are you serious😥?",reply_markup=ReplyKeyboardRemove())
    await message.answer_photo(photo='https://masterpiecer-images.s3.yandex.net/0a4b4a4d8c8711eea1ba3abd0be4d755:upscaled')

@router.message()
async def hi(message:Message)->None:
    await message.answer("hi👋!")