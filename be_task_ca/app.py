from fastapi import FastAPI, Request, Response

from .database.session import init_session, init_models
from .user.api import user_router
from .item.api import item_router

app = FastAPI()
app.include_router(user_router)
app.include_router(item_router)


@app.on_event("startup")
async def setup_db():
    await init_session()
    await init_models()


@app.get("/")
async def root():
    return {
        "message": "Thanks for shopping at Nile!"
    }  # the Nile is 250km longer than the Amazon
