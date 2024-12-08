from aiogram.fsm.state import StatesGroup, State


class MessageToUser(StatesGroup):
    text = State()
    to_user_id = State()
    to_chat_id = State()
    sender_name = State()
    sender_username = State()
