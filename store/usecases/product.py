from typing import List
from uuid import UUID
from fastapi import Depends
from store.db.repositories.product import ProductRepository
from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.core.exceptions import NotFoundException

class ProductUsecase:
    def __init__(self, repository: ProductRepository = Depends()) -> None:
        self.repository = repository

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = await self.repository.create(body)
        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.repository.get(id)
        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        return ProductOut(**result.model_dump())

    async def query(self, **filters) -> List[ProductOut]:
        return [ProductOut(**item.model_dump()) for item in await self.repository.query(**filters)]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductOut:
        product = await self.repository.get(id)
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        updated_product = await self.repository.update(id, body)
        return ProductOut(**updated_product.model_dump())

    async def delete(self, id: UUID) -> None:
        deleted = await self.repository.delete(id)
        if not deleted:
            raise NotFoundException(message=f"Product not found with filter: {id}")
