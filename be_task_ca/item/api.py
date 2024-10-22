from typing import List

from fastapi import APIRouter, status

from .schema import CreateItemRequest, CreateItemResponse
from .usecases import create_item, get_all
from ..dependencies import ItemRepository

item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@item_router.post("/",
                  status_code=status.HTTP_201_CREATED)
async def post_item(
        item: CreateItemRequest,
        repository: ItemRepository
) -> CreateItemResponse:
    return await create_item(item, repository)


@item_router.get("/")
async def get_items(repository: ItemRepository) -> List[CreateItemResponse]:
    return await get_all(repository)
