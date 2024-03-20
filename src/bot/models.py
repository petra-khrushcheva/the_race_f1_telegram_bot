from sqlalchemy.orm import Mapped

from src.core.basemodels import Base


class ChatID(Base):
    __tablename__ = "chat_ids"

    chat_id: Mapped[int]
