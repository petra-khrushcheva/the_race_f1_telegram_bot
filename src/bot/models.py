from sqlalchemy.orm import Mapped, mapped_column

from core.basemodels import Base


class ChatID(Base):
    __tablename__ = "chat_ids"

    chat_id: Mapped[int] = mapped_column(unique=True)
