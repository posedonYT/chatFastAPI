from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import DataBase_URL

engine = create_async_engine(DataBase_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False) 

class Base(DeclarativeBase):
    pass

async def get_session():
    async with new_session() as session:
        yield session 

class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    age: Mapped[int]
    password: Mapped[str]

async def setup_database():
    print("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully")
