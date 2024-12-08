import asyncio
import logging

from aiogram import Dispatcher, types, Bot, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from app.settings import settings
from app.handlers import router as handlers_router

router = Router(name=__name__)
router.include_router(handlers_router)


async def main():
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


asyncio.run(main())
