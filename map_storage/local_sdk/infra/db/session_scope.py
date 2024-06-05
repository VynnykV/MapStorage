from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import registry
from local_sdk import local_map_storage_config
from map_storage.features.map_layers.data.sqlalchemy_config import configure_map_layers_orm

config = local_map_storage_config()

__db_engine = create_async_engine(config.db_url, echo=True)
__Session = async_sessionmaker(bind=__db_engine)
__sqlalchemy_registry = registry()

configure_map_layers_orm(__sqlalchemy_registry)


@asynccontextmanager
async def session_scope():
    session = __Session()
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()