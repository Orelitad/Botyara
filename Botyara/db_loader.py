from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import BaseModel, create_async_engine, get_session_maker, proceed_schemas
from sqlalchemy.engine import URL
import os
from config import TOKEN_API
import tracemalloc


tracemalloc.start()

bot = Bot(token=TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot,
                storage=storage)

# async def main():
#     postgres_url = URL.create(
#         "postgressql+asyncpg",
#         username=os.getenv("db_user"),
#         host="localhost",
#         database=os.getenv("db_name"),
#         port=os.getenv("db_port")
#     )
#
#     async_engine = create_async_engine(postgres_url)
#     session_maker = get_session_maker(async_engine)
#     await proceed_schemas(async_engine, BaseModel.metadata)
#
#     await dp.start_polling(bot)

