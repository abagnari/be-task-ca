import hashlib
import uuid
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from be_task_ca.database.models import CartItem, User, Item
from .schema import (
    AddToCartRequest,
    CreateUserRequest,
    CreateUserResponse, AddToCartResponse,
)
from ..dependencies import UserRepository, CartItemRepository, ItemRepository


async def create_user(create_user: CreateUserRequest, repository: UserRepository) -> CreateUserResponse:
    user_data = create_user.dict()
    user_data["hashed_password"] = hashlib.sha512(
        create_user.password.encode("UTF-8")
    ).hexdigest()
    del user_data["password"]

    try:
        return CreateUserResponse.from_orm(await repository.insert(user_data))
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, "An user with this email adress already exists")


async def add_item_to_cart(user_id: uuid.UUID,
                           cart_item: AddToCartRequest,
                           user_repository: UserRepository,
                           item_repository: ItemRepository,
                           cart_item_repository: CartItemRepository) -> List[AddToCartResponse]:
    user: User = await user_repository.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    item: Item = await item_repository.get(cart_item.item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item does not exist")
    if item.quantity < cart_item.quantity:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Not enough items in stock")

    item_ids = [o.item_id for o in user.cart_items]
    if cart_item.item_id in item_ids:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item already in cart")

    cart_data = cart_item.dict()
    cart_data["user_id"] = user_id

    new_cart_item: CartItem = await cart_item_repository.insert(cart_data)

    user: User = await user_repository.get(user_id)

    # I'd say that returning something that is not explicitly the item just created is at least unusual by REST
    # specifications. I am unsure whether to change this although I corrected some other things.
    return [AddToCartResponse.from_orm(obj) for obj in user.cart_items]


async def list_items_in_cart(user_id: uuid.UUID, repository: CartItemRepository) -> List[AddToCartResponse]:
    cart_items = await repository.filter(CartItem.user_id == user_id)
    return [AddToCartResponse.from_orm(obj) for obj in cart_items]
