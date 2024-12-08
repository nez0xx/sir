from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.db.db_helper import sessionmanager
from app.settings import settings
from app.states import MessageToUser
from app.utils import create_link
from app.сrud import get_user_by_id, create_user, get_user_by_link, get_message_model_by_id, create_anon_message

HELLO_MSG = '''
🚀 Здесь можно отправить анонимное сообщение человеку, который опубликовал эту ссылку

✍️ Напишите сюда всё, что хотите ему передать, и через несколько секунд он получит ваше сообщение, но не будет знать от кого

Отправить можно фото, видео, 💬 текст, 🔊 голосовые, 📷 видеосообщения (кружки), а также ✨ стикеры'''


LINK_MSG = f"""
Начните получать анонимные вопросы прямо сейчас!

👉 t.me/{settings.BOT_LINK}?start=LINK

Разместите эту ссылку ☝️ в описании своего профиля Telegram, TikTok, Instagram (stories), чтобы вам могли написать 💬"""


router = Router(name=__name__)


@router.message(Command("start", prefix="/!%"))
async def start(message: types.Message, state: FSMContext):

    uid = str(message.from_user.id)

    async with sessionmanager.session() as session:
        user = await get_user_by_id(session=session, user_id=uid)
        if user is None:
            link = create_link()
            user = await create_user(
                session=session,
                user_id=str(message.from_user.id),
                username=message.from_user.username,
                chat_id=str(message.chat.id),
                link=link,
                name=message.from_user.full_name,
                with_commit=False
            )

        words = message.text.split()

        if len(words) > 1:
            print(1231312313)
            link = words[1].strip()

            user = await get_user_by_link(session, link=link)
            if user:
                await state.update_data(to_chat_id=user.chat_id)
                await state.update_data(to_user_id=user.id)
                await state.update_data(sender_username=message.from_user.username)
                await state.update_data(sender_name=message.from_user.full_name)

                await state.set_state(MessageToUser.text)
                await message.answer(HELLO_MSG)
                await message.answer("Напиши анонимное сообщение пользователю")
                await session.commit()
                return
            await message.answer("Похоже, ссылка недействительна")
            return

        await message.answer(LINK_MSG.replace("LINK", user.link))

        await session.commit()


@router.message(MessageToUser.text)
async def text_handler(message: types.Message, state: FSMContext):

    data = await state.get_data()

    m = None

    if message.text:
        m = await message.bot.send_message(
            chat_id=data["to_chat_id"],
            text=f"🔔 У Вас новое сообщение!\n\n<blockquote>{message.text}</blockquote>\n\n↩️ Свайпните для ответа."
        )

    if message.caption:
        caption = f"🔔 У Вас новое сообщение!\n\n<blockquote>{message.caption}</blockquote>\n\n↩️ Свайпните для ответа."
    else:
        caption = f"🔔 У Вас новое сообщение!\n\n↩️ Свайпните для ответа."

    if message.photo:
        m = await message.bot.send_photo(
            chat_id=data["to_chat_id"],
            photo=message.photo[-1].file_id,
            caption=caption
        )

    if message.sticker:
        m = await message.bot.send_sticker(
            chat_id=data["to_chat_id"],
            sticker=message.sticker.file_id
        )
        await message.bot.send_message(
            chat_id=data["to_chat_id"],
            text=caption
        )
    if message.video:
        m = await message.bot.send_video(
            chat_id=data["to_chat_id"],
            video=message.video.file_id,
            caption=caption
        )
    if message.voice:
        m = await message.bot.send_voice(
            chat_id=data["to_chat_id"],
            voice=message.voice.file_id,
            caption=caption
        )
    await message.reply("✅ Сообщение успешно отправлено.")

    async with sessionmanager.session() as session:

        await create_anon_message(
            session=session,
            sender_id=str(message.from_user.id),
            to_chat_id=data["to_chat_id"],
            message_id=str(m.message_id),
            with_commit=False
        )

        user = await get_user_by_id(session, user_id=str(message.from_user.id))

        await message.answer(LINK_MSG.replace("LINK", user.link))

        if data["to_user_id"] in settings.ADMINS:
            txt = f"^^^^^^^^^\n@{data["sender_username"]}\n{data["sender_name"]}"
            await message.bot.send_message(chat_id=data["to_chat_id"], text=txt)
        await session.commit()

    await state.clear()


@router.message(lambda message: message.reply_to_message)
async def reply_handler(message: types.Message):
    async with sessionmanager.session() as session:

        msg = await get_message_model_by_id(
            session=session,
            to_chat_id=str(message.chat.id),
            message_id=str(message.reply_to_message.message_id)
        )

        user = await get_user_by_id(session=session, user_id=str(message.from_user.id))

        if msg:
            sender = await get_user_by_id(session=session, user_id=msg.sender)

            btn1 = InlineKeyboardButton(text='Написать ещё', url=f'https://t.me/{settings.BOT_LINK}?start={user.link}')

            kb = InlineKeyboardMarkup(inline_keyboard=[[btn1,]])


            await message.bot.send_message(
                chat_id=sender.chat_id,
                text=f"🔔 Новый ответ:\n\n<blockquote>{message.text}</blockquote>",
                reply_markup=kb
            )

            await message.reply("✅ Ваш ответ успешно отправлен")



