from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import status

from .schema import AddToCartRequest, CreateUserRequest, CreateUserResponse, AddToCartResponse
from .usecases import add_item_to_cart, create_user, list_items_in_cart
from ..dependencies import UserRepository, ItemRepository, CartItemRepository

user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@user_router.post("/",
                  status_code=status.HTTP_201_CREATED)
async def post_customer(user: CreateUserRequest, repository: UserRepository) -> CreateUserResponse:
    return await create_user(user, repository)


@user_router.post("/{user_id}/cart",
                  status_code=status.HTTP_201_CREATED)
async def post_cart(
        user_id: UUID,
        cart_item: AddToCartRequest,
        user_repository: UserRepository,
        item_repository: ItemRepository,
        cart_item_repository: CartItemRepository
) -> List[AddToCartResponse]:
    return await add_item_to_cart(user_id, cart_item, user_repository, item_repository, cart_item_repository)


@user_router.get("/{user_id}/cart")
async def get_cart(user_id: UUID, cart_item_repository: CartItemRepository) -> List[AddToCartResponse]:
    return await list_items_in_cart(user_id, cart_item_repository)
