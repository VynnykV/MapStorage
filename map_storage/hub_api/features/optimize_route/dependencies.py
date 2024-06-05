from fastapi import Request

from map_storage.features.optimize_route.application.commands.ant_colony_optimization import \
    AntColonyOptimizationHandler


def ant_colony_optimization_handler(request: Request) -> AntColonyOptimizationHandler:
    return AntColonyOptimizationHandler()
