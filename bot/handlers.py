import os
from aiogram import Router, F
from aiogram.types import Message, WebAppInfo, ReplyKeyboardRemove,CallbackQuery,InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder,KeyboardButton,ReplyKeyboardMarkup, ReplyKeyboardBuilder, InlineKeyboardButton
from dotenv import load_dotenv
from random import randint

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

@router.message(Command("numbers"))
async def reply_builder(message:Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 21):
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(5)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
# @router.message(F.text)
# async def numb_choice(message:Message):
#         if message.text == 1:
#             await message.reply(text='Сосредоточьтесь на своих целях и поставленных задачах.',reply_markup=ReplyKeyboardRemove())
#             return 0
#         if message.text == 2:
#             await message.reply(text='Будьте терпеливы и упорны в достижении желаемого результата. ',reply_markup=ReplyKeyboardRemove())
#             return 0
#         if F.text.lower() == '3':
#             await message.reply(text=' Постарайтесь найти баланс между работой и отдыхом для сохранения энергии.',reply_markup=ReplyKeyboardRemove())
#             return 0
#         if F.text.lower() == '4':
#             await message.reply(text='. Фокусируйтесь на своих навыках и умениях, чтобы проявить свой потенциал.',reply_markup=ReplyKeyboardRemove())
#             return 0
#         if F.text.lower() == '5':
#             await message.reply(text='Ищите новые возможности для личностного роста и развития.',reply_markup=ReplyKeyboardRemove())
#             return 0
@router.message(Command("links"))
async def cmd_inline_url(message:Message):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="GitHub", url="https://github.com")
    )
    builder.row(InlineKeyboardButton(
        text="YouTube",
        url="https://www.youtube.com/")
    )
    builder.row(InlineKeyboardButton(
        text="кто-то",
        url=f"t.me/{message.chat.username}")
    )
    await message.answer(
        'Выберите ссылку',
        reply_markup=builder.as_markup(),
    )

@router.message(Command("random"))
async def cmd_random(message:Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число ",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == "random_value")
async def send_random_value(callback:CallbackQuery):
    await callback.message.answer(str(randint(1, 10000)))
    await callback.answer()

user_data = {}





def get_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="-1", callback_data="num_decr"),
            InlineKeyboardButton(text="+1", callback_data="num_incr")
        ],
        [InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
    ]
    keyboard =InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def update_num_text(message: Message, new_value: int):
    await message.edit_text(
        f"Укажите число: {new_value}",
        reply_markup=get_keyboard()
    )


@router.message(Command("numbers_count"))
async def cmd_numbers(message: Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard())


@router.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]

    if action == "incr":
        user_data[callback.from_user.id] = user_value+1
        await update_num_text(callback.message, user_value+1)
    elif action == "decr":
        user_data[callback.from_user.id] = user_value-1
        await update_num_text(callback.message, user_value-1)
    elif action == "finish":
        await callback.message.edit_text(f"Итого: {user_value}")

    await callback.answer()
@router.message()
async def hi(message:Message)->None:
    await message.answer("hi👋!")