from sqlalchemy.orm import Mapped

from src.core.basemodels import Base


class Article(Base):
    __tablename__ = "articles"

    slug: Mapped[str]
