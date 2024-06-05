from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import registry
import sqlalchemy

from hub_api.features.import_profiles.routers import add_import_profiles_router
from hub_api.features.map_layers.routers import add_map_layers_router
from hub_api import map_storage_hub_config
from hub_api.features.optimize_route.routers import add_optimize_route_router

from map_storage import configure_map_layers_orm, configure_import_profiles_orm, NotFoundException
import map_storage.infra as infra
from map_storage.features.shared.exceptions import MapStorageException

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = map_storage_hub_config('hub_api/.env')

db_engine = create_async_engine(config.db_url, echo=True)
async_session = async_sessionmaker(bind=db_engine)
sqlalchemy_registry = registry()

# configure sqlalchemy orm for submodules
configure_import_profiles_orm(sqlalchemy_registry)
configure_map_layers_orm(sqlalchemy_registry)

# add http endpoints and dependencies
add_import_profiles_router(app)
add_map_layers_router(app)
add_optimize_route_router(app)

# middleware
@app.middleware("http")
async def error_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except NotFoundException:
        return JSONResponse(status_code=404, content="resource not found")
    except sqlalchemy.orm.exc.NoResultFound:
        return JSONResponse(status_code=404, content="resource not found")
    except MapStorageException as ms_ex:
        return JSONResponse(status_code=400, content=str(ms_ex))

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    session = async_session()
    try:
        request.state.db = session
        response = await call_next(request)
        if response.status_code == 200:
            await request.state.db.commit()
        else:
            await request.state.db.rollback()
    except Exception as e:
        await request.state.db.rollback()
        raise e
    finally:
        await session.close()

    return response

@app.on_event("shutdown")
async def on_server_shutdown():
    await db_engine.dispose()
    await infra.http_session.close()