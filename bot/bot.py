import asyncio
import os
import handlers
from aiogram import Bot,Dispatcher
from aiogram.enums import ParseMode

async def main()->None:
    bot=Bot(os.getenv('TOKEN'),parse_mode=ParseMode.HTML)
    dp=Dispatcher()
    dp.include_router(handlers.router)
    await bot.delete_webhook(True)
    await dp.start_polling(bot)

if __name__ == "__main__":
   asyncio.run(main())