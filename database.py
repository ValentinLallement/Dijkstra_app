from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

database_url=os.getenv("DATABASE_URL")

DATABASE_URL = (
    database_url
)
engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine

)
db=SessionLocal()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class Base(DeclarativeBase):
    pass