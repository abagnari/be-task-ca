from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from be_task_ca.database import models, repository, session
from be_task_ca.database.models import Item, User, CartItem
from be_task_ca.database.repository import DBRepository


# Now all is needed to change the persistence layer implementation is to change this single function here
def get_repository(
    model: type[models.Base],
) -> Callable[[AsyncSession], repository.DBRepository]:
    def func(session: AsyncSession = Depends(session.get_db)):
        return repository.DBRepository(model).with_session(session)

    return func


ItemRepository = Annotated[
    DBRepository[Item],
    Depends(get_repository(Item)),
]

UserRepository = Annotated[
    DBRepository[User],
    Depends(get_repository(User)),
]

CartItemRepository = Annotated[
    DBRepository[CartItem],
    Depends(get_repository(CartItem)),
]