from typing import Annotated

from core.models import db_helper
from core.schemas.orders import OrderCreate, OrderRead, OrderStatus
from crud import orders as orders_crud
from crud import products as products_crud
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["orders"])


@router.get("/", response_model=list[OrderRead])
async def read_orders(session: AsyncSession = Depends(db_helper.session_getter)):
    orders = await orders_crud.get_all_orders(session)
    return orders


@router.get("/{id}", response_model=OrderRead)
async def read_order(
    *,
    session: AsyncSession = Depends(db_helper.session_getter),
    id: int,
):
    order = await orders_crud.get_order_by_id(session, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/", response_model=OrderRead, status_code=201)
async def create_order(
    *,
    session: AsyncSession = Depends(db_helper.session_getter),
    order: OrderCreate,
):
    for item in order.items:
        product = await products_crud.get_product_by_id(session, item.product_id)
        if not product:
            raise HTTPException(status_code=400, detail="Product not found")
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail="Not enough stock")
    return await orders_crud.create_order(session, order)


@router.patch("/{id}/status", response_model=OrderRead)
async def update_order_status(
    *,
    session: AsyncSession = Depends(db_helper.session_getter),
    id: int,
    status: Annotated[OrderStatus, Body(embed=True)],
):
    order = await orders_crud.update_order_status(session, id, status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
