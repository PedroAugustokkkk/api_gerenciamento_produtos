from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductBase, ProductOut, ProductUpdate

class ProductRepository:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductBase) -> ProductModel:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())
        return product_model

    async def get(self, id: UUID) -> ProductModel:
        result = await self.collection.find_one({"id": id})
        if not result:
            return None
        return ProductModel(**result)

    async def query(self, **filters) -> List[ProductModel]:
        return [ProductModel(**item) async for item in self.collection.find(filters)]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductModel:
        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER,
        )
        if not result:
            return None
        return ProductModel(**result)

    async def delete(self, id: UUID) -> bool:
        result = await self.collection.delete_one({"id": id})
        return result.deleted_count > 0
