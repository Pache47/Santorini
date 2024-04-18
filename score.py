# class ScoringSystem:
#     def __init__(self, board, worker_positions):
#         self.board = board
#         self.worker_positions = worker_positions

#     def calculate_scores(self, workers, opponent_workers):
#         height_score = self.calculate_height_score(workers)
#         center_score = self.calculate_center_score(workers)
#         distance_score = self.calculate_distance_score(workers, opponent_workers)
#         return height_score, center_score, distance_score

#     def calculate_height_score(self, workers):
#         return sum(self.board.grid[x][y]['level'] for worker, (x, y) in self.worker_positions.items() if worker in workers)

#     def calculate_center_score(self, workers):
#         center = (2, 2)
#         return sum(2 - (abs(center[0] - x) + abs(center[1] - y))//2 for worker, (x, y) in self.worker_positions.items() if worker in workers)

#     def calculate_distance_score(self, workers, opponent_workers):
#         score = 0
#         for worker in workers:
#             x, y = self.worker_positions[worker]
#             min_distance = min(abs(x - opp_x) + abs(y - opp_y) for opp_worker in opponent_workers for opp_x, opp_y in [self.worker_positions[opp_worker]])
#             score += min_distance
#         return 8 * len(workers) - score  # Assuming max distance for better score



class ScoringSystem:
    def __init__(self, board, worker_positions):
        self.board = board
        self.worker_positions = worker_positions

    def calculate_scores(self, workers, opponent_workers):
        height_score = self.calculate_height_score(workers)
        center_score = self.calculate_center_score(workers)
        distance_score = self.calculate_distance_score(workers, opponent_workers)
        return height_score, center_score, distance_score

    def calculate_height_score(self, workers):
        return sum(self.board.grid[x][y]['level'] for worker, (x, y) in self.worker_positions.items() if worker in workers)

    def calculate_center_score(self, workers):
        center = (2, 2)
        return sum((2 - max(abs(center[0] - x), abs(center[1] - y))) for worker, (x, y) in self.worker_positions.items() if worker in workers)

    def calculate_distance_score(self, workers, opponent_workers):
        score = 0
        for worker in workers:
            x, y = self.worker_positions[worker]
            distances = [abs(x - opp_x) + abs(y - opp_y) for opp_worker in opponent_workers for opp_x, opp_y in [self.worker_positions[opp_worker]]]
            score += min(distances)
        max_possible_distance = 8 * len(workers)  # Hypothetically the maximum distance on a 5x5 grid
        normalized_score = max_possible_distance - score  # Lower distances should increase the score
        return normalized_score


# class ScoringSystem:
#     def __init__(self, board):
#         self.board = board

#     def calculate_scores(self, worker_positions, opponent_worker_positions):
#         height_score = self.calculate_height_score(worker_positions)
#         center_score = self.calculate_center_score(worker_positions)
#         distance_score = self.calculate_distance_score(worker_positions, opponent_worker_positions)
#         return height_score, center_score, distance_score

#     def calculate_height_score(self, worker_positions):
#         return sum(self.board.grid[x][y]['level'] for x, y in worker_positions.values())

#     def calculate_center_score(self, worker_positions):
#         center = (2, 2)
#         return sum(2 - (abs(center[0] - x) + abs(center[1] - y))//2 for x, y in worker_positions.values())

#     def calculate_distance_score(self, worker_positions, opponent_worker_positions):
#         score = 0
#         for x, y in worker_positions.values():
#             min_distance = min(abs(x - opp_x) + abs(y - opp_y) for opp_x, opp_y in opponent_worker_positions.values())
#             score += min_distance
#         return 8 * len(worker_positions) - score  # Adjusting the score based on the number of workers
