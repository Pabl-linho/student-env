from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
#from core.config_leader import settings

SQLALCHEMY_DATABASE_URI =""
engine = create_async_engine(
    str(SQLALCHEMY_DATABASE_URI ),                    #settings.
    echo=True, 
    future=True,
    pool_size=5, # t3 open conn
    max_overflow= 10 # 3nd pression
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False # bah matro7ch data after Asycn
)
Base = declarative_base()

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()