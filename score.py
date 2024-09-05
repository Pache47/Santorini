from board import Board

class ScoringSystem:
    """ 
    Class to calculate scores based on worker positions and board state.
    """
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
        for opponent_worker in opponent_workers:
            o_x, o_y = self.worker_positions[opponent_worker]
            distances =[]
            for worker in workers:
                x, y = self.worker_positions[worker]
                x_diff = abs(o_x-x)
                y_diff = abs(o_y-y)
                distances.append(x_diff+y_diff - min(x_diff,y_diff))
            score += min(distances)
        normalized_score = 8 - score
        return normalized_score


class AIScoreWeighing(ScoringSystem):
    def __init__(self, board, worker_positions):
        self.board = board
        self.worker_positions = worker_positions
