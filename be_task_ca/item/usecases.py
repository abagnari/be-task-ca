from typing import List

from .schema import CreateItemRequest, CreateItemResponse
from ..dependencies import ItemRepository


async def create_item(item: CreateItemRequest, repository: ItemRepository) -> CreateItemResponse:
    return CreateItemResponse.from_orm(await repository.insert(item.dict()))


async def get_all(repository: ItemRepository) -> List[CreateItemResponse]:
    return [CreateItemResponse.from_orm(obj) for obj in await repository.get()]
