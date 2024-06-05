from map_storage.features.optimize_route.application.commands.ant_colony_optimization.ant_colony_optimization_algorithm import \
    AntColony
from map_storage.features.optimize_route.application.commands.ant_colony_optimization.command import \
    AntColonyOptimizationCommand


class AntColonyOptimizationHandler:
    async def __call__(self, command: AntColonyOptimizationCommand):
        coordinates = command.polyline_points

        ant_colony = AntColony(coordinates, 0, len(coordinates) - 1, n_ants=10, n_iterations=100, alpha=1.0, beta=2.0, evaporation_rate=0.5)
        solution, cost = ant_colony.solve()

        return [coordinates[index] for index in solution]
