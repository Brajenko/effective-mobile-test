from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class Product(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    price: Mapped[float]
    stock_quantity: Mapped[int]

    __table_args__ = (UniqueConstraint("name"),)
