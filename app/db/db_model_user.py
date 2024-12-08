from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from typing import TYPE_CHECKING

from app.db.db_model_message import AnonMessage


class User(Base):
    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str]
    link: Mapped[str]
    chat_id: Mapped[str]
