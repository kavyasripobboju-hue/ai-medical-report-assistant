from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)

class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    filename: Mapped[str] = mapped_column(String, nullable=False)

    filepath: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    analysis: Mapped[str] = mapped_column(String, nullable=True)


    user = relationship("User")
