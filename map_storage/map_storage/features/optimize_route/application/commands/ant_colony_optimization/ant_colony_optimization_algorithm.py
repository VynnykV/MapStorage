import math
import numpy as np


class AntColony:
    def __init__(self, coordinates, start, end, n_ants, n_iterations, alpha, beta, evaporation_rate):
        self.coordinates = coordinates
        self.start = start
        self.end = end
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.distance_matrix = np.array(
            [[self.haversine(*coordinates[i], *coordinates[j]) for j in range(len(coordinates))] for i in range(len(coordinates))]
        )
        self.pheromone_matrix = np.ones_like(self.distance_matrix)

    def solve(self):
        best_cost = float('inf')
        best_solution = None
        for iteration in range(self.n_iterations):
            all_tours = []
            all_costs = []
            for ant in range(self.n_ants):
                tour = self.build_tour()
                cost = self.calculate_cost(tour)
                all_tours.append(tour)
                all_costs.append(cost)
                if cost < best_cost:
                    best_cost = cost
                    best_solution = tour
            self.update_pheromone(all_tours, all_costs)
        return best_solution, best_cost

    def build_tour(self):
        tour = [self.start]
        visited = set(tour)
        current = self.start
        while len(tour) < len(self.coordinates) - 1:  # Exclude the end point from the loop
            move_probabilities = self.calculate_move_probabilities(current, visited)
            next_city = self.roulette_wheel_selection(move_probabilities)
            tour.append(next_city)
            visited.add(next_city)
            current = next_city
        tour.append(self.end)  # End at the specified end point
        return tour

    def calculate_move_probabilities(self, current, visited):
        probabilities = np.zeros(len(self.coordinates))
        for j in range(len(self.coordinates)):
            if j not in visited and j != self.end or j == self.end and len(visited) == len(self.coordinates) - 1:
                pheromone = self.pheromone_matrix[current][j] ** self.alpha
                heuristic = (1.0 / self.distance_matrix[current][j]) ** self.beta
                probabilities[j] = pheromone * heuristic
        total = np.sum(probabilities)
        if total > 0:
            probabilities /= total
        return probabilities

    def roulette_wheel_selection(self, probabilities):
        cumulative_probability = np.cumsum(probabilities)
        r = np.random.rand()
        for i, cumulative in enumerate(cumulative_probability):
            if r <= cumulative:
                return i
        return -1  # Fallback

    def calculate_cost(self, tour):
        return sum(self.distance_matrix[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))

    def update_pheromone(self, all_tours, all_costs):
        self.pheromone_matrix *= (1 - self.evaporation_rate)
        for tour, cost in zip(all_tours, all_costs):
            for i in range(len(tour) - 1):
                self.pheromone_matrix[tour[i]][tour[i + 1]] += 1.0 / cost
                self.pheromone_matrix[tour[i + 1]][tour[i]] += 1.0 / cost  # Since distance is symmetric

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)
        a = np.sin(delta_phi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(np.sqrt(a), np.sqrt(1 - a))
        distance = R * c
        return distance



