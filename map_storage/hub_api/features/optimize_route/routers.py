from typing import Callable, Any

from fastapi import FastAPI, APIRouter, Depends

import hub_api.features.optimize_route.dependencies as dep
from map_storage.features.optimize_route.application.commands.ant_colony_optimization.command import \
    AntColonyOptimizationCommand


def add_optimize_route_router(app: FastAPI):
    router = APIRouter(prefix="/optimizeRoute", tags=["optimize_route"])

    @router.post("/antColony")
    async def ant_colony_optimization(
            request: AntColonyOptimizationCommand,
            handler: Callable[[AntColonyOptimizationCommand], Any]
            = Depends(dep.ant_colony_optimization_handler)):
        return await handler(request)

    app.include_router(router)