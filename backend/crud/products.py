from typing import Optional, Sequence

from core.models.products import Product
from core.schemas.products import ProductCreate
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_products(
    session: AsyncSession,
) -> Sequence[Product]:
    stmt = select(Product).order_by(Product.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_product(
    session: AsyncSession,
    product_create: ProductCreate,
) -> Product:
    product = Product(**product_create.model_dump())
    session.add(product)
    await session.commit()
    return product


async def get_product_by_id(
    session: AsyncSession,
    product_id: int,
) -> Optional[Product]:
    stmt = select(Product).where(Product.id == product_id)
    result = await session.scalars(stmt)
    try:
        return result.one()
    except NoResultFound:
        return None


async def get_product_by_name(
    session: AsyncSession,
    product_name: str,
) -> Optional[Product]:
    stmt = select(Product).where(Product.name == product_name)
    result = await session.scalars(stmt)
    try:
        return result.one()
    except NoResultFound:
        return None


async def update_product(
    session: AsyncSession,
    product_id: int,
    product_update: ProductCreate,
) -> Optional[Product]:
    product = await get_product_by_id(session, product_id)
    if product is None:
        return None
    for key, value in product_update.model_dump(exclude_none=True).items():
        setattr(product, key, value)
    await session.commit()
    await session.refresh(product)
    return product


async def delete_product(
    session: AsyncSession,
    product_id: int,
) -> bool:
    product = await get_product_by_id(session, product_id)
    if product is None:
        return False
    await session.delete(product)
    await session.commit()
    return True


async def update_product_stock_no_commit(
    session: AsyncSession,
    product_id: int,
    quantity: int,
):
    product = await get_product_by_id(session, product_id)
    if product is None:
        return None
    product.stock_quantity += quantity
