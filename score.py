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





from board import Board


class ScoringSystem:
    def __init__(self, board:Board, worker_positions):
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
        normalized_score = 8 - score  # Lower distances should increase the score
        return normalized_score


class AIScoreWeighing(ScoringSystem):
    def __init__(self, board, worker_positions):
        self.board = board
        self.worker_positions = worker_positions
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
#         score = 0
#         for worker, (x, y) in self.worker_positions.items():
#             if worker in workers:
#                 distance_from_center = max(abs(center[0] - x), abs(center[1] - y))
#                 if distance_from_center == 0:
#                     score += 2  # Center cell
#                 elif distance_from_center == 1:
#                     score += 1  # Middle ring
#                 # Edge cells implicitly have a score of 0
#         return score

#     def calculate_distance_score(self, workers, opponent_workers):
#         total_min_distance = 0
#         for worker in workers:
#             x, y = self.worker_positions[worker]
#             min_distance = min(abs(x - ox) + abs(y - oy) for opp_worker in opponent_workers for ox, oy in [self.worker_positions[opp_worker]])
#             total_min_distance += min_distance
#         # Normalize to value higher proximity scores higher
#         max_possible_distance = 8 * len(workers)  # Adjust based on board size, worker count
#         normalized_score = max_possible_distance - total_min_distance
#         return normalized_score

