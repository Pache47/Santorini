import random

from board import Board
from score import ScoringSystem
import copy

class Player:
    """
    Base class for all player types.
    """
    def __init__(self, board:Board, workers, worker_positions):
        self.board = board 
        self.workers = workers
        self.worker_positions = worker_positions

    def select_move(self):
        pass


class HumanPlayer(Player):
    """
    Human player interacts through the command line.
    """
    def select_move(self):
        pass


class RandomAI(Player):
    """
    Random AI that selects a move randomly from the available valid moves.
    """    
    def select_move(self):
        valid_moves = []
        for worker in self.workers:
            x, y = self.worker_positions[worker]
            for direction in self.board.directions:
                new_x, new_y = x + self.board.directions[direction][0], y + self.board.directions[direction][1]
                if self.board.can_move(x, y, direction) and self.board.is_within_bounds(new_x, new_y):
                    # Iterate over possible build directions after moving
                    for build_dir in self.board.directions:
                        build_x, build_y = new_x + self.board.directions[build_dir][0], new_y + self.board.directions[build_dir][1]
                        if self.board.can_build(new_x, new_y, build_dir, x, y):
                            valid_moves.append((worker, direction, build_dir))
        return random.choice(valid_moves) if valid_moves else None

    def validate_move(self, worker, x, y, direction):
        return self.board.can_move(x, y, direction)


class HeuristicAI(Player):
    """ 
    AI that selects the best move based on a heuristic scoring system.
    """
    def __init__(self, board, workers, worker_positions, opponent_workers, scoring_system:ScoringSystem):
        super().__init__(board, workers, worker_positions)
        self.opponent_workers = opponent_workers
        self.scoring_system = scoring_system

    def select_move(self):
        best_score = -float('inf')
        best_moves = []
        for worker in self.workers:
            x, y = self.worker_positions[worker]
            for move_dir in self.board.directions:
                new_x, new_y = x + self.board.directions[move_dir][0], y + self.board.directions[move_dir][1]
                if self.board.can_move(x, y, move_dir) and self.board.is_within_bounds(new_x, new_y):
                    for build_dir in self.board.directions:
                        build_x, build_y = new_x + self.board.directions[build_dir][0], new_y + self.board.directions[build_dir][1]
                        if self.board.can_build(new_x, new_y, build_dir, x, y):
                            test_board = Board()
                            test_board.grid = copy.deepcopy(self.board.grid)
                            test_worker_pos = copy.deepcopy(self.worker_positions)
                            test_board.grid[new_x][new_y]['worker'], test_board.grid[x][y]['worker'] = test_board.grid[x][y]['worker'], None
                            test_worker_pos[worker] = (new_x, new_y)
                            test_board.grid[build_x][build_y]['level'] += 1 
                            ai_score_sys = ScoringSystem(test_board,test_worker_pos)
                            height_score, center_score, distance_score =ai_score_sys.calculate_scores(self.workers, self.opponent_workers)
                            score = 3 * height_score + 2 * center_score + distance_score
                            if score > best_score:
                                best_score = score
                                best_moves = [(worker, move_dir, build_dir)]
                            elif score == best_score:
                                best_moves.append((worker, move_dir, build_dir))
        return random.choice(best_moves) if best_moves else None
