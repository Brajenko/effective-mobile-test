from pydantic import BaseModel, ConfigDict, PositiveFloat, NonNegativeInt


class ProductBase(BaseModel):
    name: str
    description: str
    price: PositiveFloat
    stock_quantity: NonNegativeInt


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
