from typing import List
from fastapi import APIRouter, Body, Depends, Query, status
from pydantic import UUID4
from store.schemas.product import ProductBase, ProductOut, ProductUpdate
from store.usecases.product import ProductUsecase
from decimal import Decimal

router = APIRouter(tags=["products"])

@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductBase = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    return await usecase.create(body=body)

@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Query(..., alias="id"), usecase: ProductUsecase = Depends()
) -> ProductOut:
    return await usecase.get(id=id)

@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(
    min_price: Decimal = Query(None, alias="min_price"),
    max_price: Decimal = Query(None, alias="max_price"),
    usecase: ProductUsecase = Depends(),
) -> List[ProductOut]:
    filters = {}
    if min_price is not None:
        filters["price"] = {"$gte": min_price}
    if max_price is not None:
        if "price" in filters:
            filters["price"]["$lte"] = max_price
        else:
            filters["price"] = {"$lte": max_price}
    return await usecase.query(**filters)

@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Query(..., alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductOut:
    return await usecase.update(id=id, body=body)

@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Query(..., alias="id"), usecase: ProductUsecase = Depends()
) -> None:
    await usecase.delete(id=id)
