from sqlalchemy import create_engine, Column, Integer, String, VARCHAR, MetaData
from sqlalchemy.orm import sessionmaker
from .base import BaseModel

class user_answers(BaseModel):
    __tablename__ = 'db.sqlite'
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    user_first_name = Column(VARCHAR(32), unique=False, nullable=True)
    chat_id = Column(Integer)
    first_message = Column(VARCHAR(32))
    second_message = Column(VARCHAR(32))
    third_message = Column(VARCHAR(32))
    fourth_message = Column(VARCHAR(32))
    status = Column(String)

    def __str__(self) -> str:
        return f"<User:{self.user_id}>"