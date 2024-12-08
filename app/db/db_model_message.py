from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.db import User


class AnonMessage(Base):
    id: Mapped[str] = mapped_column(primary_key=True)
    to_chat_id: Mapped[str]
    message_id: Mapped[str]
    sender: Mapped[str] = mapped_column(ForeignKey("users.id"))
