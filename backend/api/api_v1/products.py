from core.models import db_helper
from core.schemas.products import ProductCreate, ProductRead
from crud import products as products_crud
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["products"])


@router.get("/", response_model=list[ProductRead])
async def read_products(session: AsyncSession = Depends(db_helper.session_getter)):
    products = await products_crud.get_all_products(session)
    return products


@router.post("/", response_model=ProductRead, status_code=201)
async def create_product(
    *,
    session: AsyncSession = Depends(db_helper.session_getter),
    product: ProductCreate,
):
    same_name_product = await products_crud.get_product_by_name(session, product.name)
    if same_name_product is not None:
        raise HTTPException(
            status_code=400, detail="Product with this name already exists"
        )
    return await products_crud.create_product(session, product)


@router.put("/{id}", response_model=ProductRead)
async def update_product(
    *,
    session: AsyncSession = Depends(db_helper.session_getter),
    id: int,
    product: ProductCreate,
):
    db_product = await products_crud.get_product_by_id(session, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product = await products_crud.update_product(session, id, product)
    return db_product


@router.get("/{id}", response_model=ProductRead)
async def read_product(
    *,
    session: AsyncSession = Depends(db_helper.session_getter),
    id: int,
):
    product = await products_crud.get_product_by_id(session, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{id}", status_code=204)
async def delete_product(
    *,
    session: AsyncSession = Depends(db_helper.session_getter),
    id: int,
):
    product = await products_crud.get_product_by_id(session, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = await products_crud.delete_product(session, id)
