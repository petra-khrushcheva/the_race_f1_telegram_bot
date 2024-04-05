from sqlalchemy.orm import Mapped

from core import Base


class Article(Base):
    __tablename__ = "articles"

    slug: Mapped[str]
