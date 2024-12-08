from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db import User
from app.db.db_model_message import AnonMessage
import uuid

async def get_user_by_id(session: AsyncSession, user_id: str) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def create_user(
        session: AsyncSession,
        user_id: str,
        name: str,
        username: str,
        chat_id: str,
        link: str,
        with_commit: bool = True
) -> User:
    model = User(id=user_id, username=username, chat_id=chat_id, link=link, name=name)
    session.add(model)
    if with_commit:
        await session.commit()
    else:
        await session.flush()
    return model


async def get_user_by_link(session: AsyncSession, link: str) -> User | None:
    stmt = select(User).where(User.link == link)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def get_message_model_by_id(session: AsyncSession, message_id: str, to_chat_id: str) -> AnonMessage | None:
    stmt = (select(AnonMessage)
            .where(AnonMessage.to_chat_id == to_chat_id)
            .where(AnonMessage.message_id == message_id))
    result = await session.execute(stmt)
    model = result.scalar_one_or_none()
    return model


async def create_anon_message(
        session: AsyncSession,
        message_id: str,
        to_chat_id: str,
        sender_id: str,
        with_commit: bool = True
) -> AnonMessage:
    model = AnonMessage(message_id=message_id, to_chat_id=to_chat_id, sender=sender_id, id=str(uuid.uuid4()))
    session.add(model)

    if with_commit:
        await session.commit()
    else:
        await session.flush()

    return model
