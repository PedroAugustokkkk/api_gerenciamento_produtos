from store.models.base import CreateBaseModel
from store.schemas.product import ProductBase


class ProductModel(ProductBase, CreateBaseModel):
    ...
