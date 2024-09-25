from typing import Optional, Sequence

from core.models.orders import Order, OrderItem, OrderStatus
from crud import products as products_crud
from core.schemas.orders import OrderCreate
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_orders(
    session: AsyncSession,
) -> Sequence[Order]:
    stmt = select(Order).order_by(Order.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_order(
    session: AsyncSession,
    order_create: OrderCreate,
) -> Order:
    order = Order(
        **order_create.model_dump(
            exclude={
                "items",
            }
        )
    )
    for item in order_create.items:
        await products_crud.update_product_stock_no_commit(
            session, item.product_id, -item.quantity
        )
        session.add(
            OrderItem(
                product_id=item.product_id,
                order=order,
                quantity=item.quantity,
            )
        )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


async def get_order_by_id(
    session: AsyncSession,
    order_id: int,
) -> Optional[Order]:
    stmt = select(Order).where(Order.id == order_id)
    result = await session.scalars(stmt)
    try:
        return result.one()
    except NoResultFound:
        return None


async def update_order_status(
    session: AsyncSession,
    order_id: int,
    status: OrderStatus,
) -> Optional[Order]:
    order = await get_order_by_id(session, order_id)
    if order is None:
        return None
    order.status = status
    await session.commit()
    await session.refresh(order)
    return order
