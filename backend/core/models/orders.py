import datetime as dt
import enum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .products import Product
from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class OrderStatus(enum.Enum):
    IN_PROCESS = "In process"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"


class Order(IntIdPkMixin, Base):
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.IN_PROCESS
    )
    items: Mapped[list["OrderItem"]] = relationship(viewonly=True, lazy="selectin")


class OrderItem(IntIdPkMixin, Base):
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
    order: Mapped[Order] = relationship("Order")
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    product: Mapped["Product"] = relationship("Product")
    quantity: Mapped[int]
