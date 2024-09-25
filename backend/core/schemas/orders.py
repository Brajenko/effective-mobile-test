import datetime as dt
from typing import Optional

from pydantic import BaseModel, ConfigDict, PositiveInt

from core.models.orders import OrderStatus


class OrderItemBase(BaseModel):
    product_id: int
    quantity: PositiveInt


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    pass


class OrderBase(BaseModel):
    pass


class OrderCreate(OrderBase):
    items: list[OrderItemCreate]
    status: Optional[OrderStatus] = OrderStatus.IN_PROCESS


class OrderRead(OrderBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    items: list[OrderItemRead]
    created_at: dt.datetime
    status: OrderStatus
    id: int
