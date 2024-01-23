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
async def with_puree(message:Message)-> None:
    await message.reply("Let it be so🥱",reply_markup=ReplyKeyboardRemove())
    await message.answer_photo(photo='https://img.freepik.com/premium-photo/brown-hen-isolated-on-white-studio-shot_136670-3076.jpg')

@router.message(F.text.lower() == "meat")
async def without_puree(message:Message)-> None:
    await message.reply("Nice choice😊!",reply_markup=ReplyKeyboardRemove())
    await message.answer_photo(photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQj8pV6zokgWbJhdltrvc9GCNvRt_JeRFPflsktvSkgGw&s')

@router.message(F.text.lower() == "fish")
async def without_puree(message:Message)-> None:
    await message.reply("Are you serious😥?",reply_markup=ReplyKeyboardRemove())
    await message.answer_photo(photo='https://masterpiecer-images.s3.yandex.net/0a4b4a4d8c8711eea1ba3abd0be4d755:upscaled')

@router.message(Command("numbers"))
async def reply_builder(message:Message)-> None:
    builder = ReplyKeyboardBuilder()
    for i in range(1, 21):
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(5)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
@router.message(lambda message: message.text.isdigit() and int(message.text) in range(1, 6))
async def reply_by_number(message: Message)-> None:
    number = int(message.text)
    if number == 1:
        await message.answer('Сосредоточьтесь на своих целях и поставленных задачах.')
    elif number == 2:
        await message.answer(' Будьте терпеливы и упорны в достижении желаемого результата')
    elif number == 3:
        await message.answer('Постарайтесь найти баланс между работой и отдыхом для сохранения энергии.')
    elif number == 4:
        await message.answer('Фокусируйтесь на своих навыках и умениях, чтобы проявить свой потенциал.')
    elif number == 5:
        await message.answer('Ищите новые возможности для личностного роста и развития.')

@router.message(Command("links"))
async def cmd_inline_url(message:Message)-> None:
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
async def cmd_random(message:Message)-> None:
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
async def send_random_value(callback:CallbackQuery)-> None:
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
async def update_num_text(message: Message, new_value: int)-> None:
    await message.edit_text(
        f"Укажите число: {new_value}",
        reply_markup=get_keyboard()
    )
@router.message(Command("numbers_count"))
async def cmd_numbers(message: Message)-> None:
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard())
@router.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: CallbackQuery)-> None:
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



@router.message(Command('alko'))
async def alko(message:Message)->None:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text= '❤️❤️❤️️❤️️❤️️❤️️❤️️❤️️❤️❤️', callback_data='like'))
    builder.add(InlineKeyboardButton(text= '👎',callback_data='dislike'))
    await message.answer_photo(photo='https://avatars.dzeninfra.ru/get-zen_doc/1131857/pub_5b66fb00b9dc1000a9eca832_5b66fb2a2ef71f00a889eb2a/scale_1200',
                               reply_markup=builder.as_markup(),
                               caption='it is obvious')
@router.callback_query()
async def alko_handler(callback:CallbackQuery):
    if callback.data=='like':
        await callback.message.answer("You are absolutely right👈👈👈")
        await callback.message.answer_photo(photo='https://i.pinimg.com/736x/3e/69/33/3e6933f1430c178465f64df11671c0e9.jpg')
    elif callback.data=='dislike':
        await callback.message.answer('.....')
        await callback.message.answer_photo(photo='https://kartinkof.club/uploads/posts/2022-03/1648360476_11-kartinkof-club-p-mem-cheshet-golovu-12.jpg')
@router.message()
async def print_ref(message:Message)->None:
    await message.answer("Unknown command\nPrint /help to see command list")