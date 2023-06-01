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
