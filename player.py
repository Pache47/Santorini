import random

class Player:
    """
    Base class for all player types.
    """
    def __init__(self, board, workers, worker_positions):
        self.board = board
        self.workers = workers
        self.worker_positions = worker_positions

    def select_move(self):
        raise NotImplementedError("Each player must implement a move selection method.")


class HumanPlayer(Player):
    """
    Human player interacts through the command line.
    """
    def select_move(self):
        # Interaction logic would be handled in the Game class, not here
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
    Heuristic AI that evaluates moves based on a simple scoring system.
    """
    def select_move(self):
        best_score = -float('inf')
        best_move = None
        for worker in self.workers:
            x, y = self.worker_positions[worker]
            for move_dir in self.board.directions:
                new_x, new_y = x + self.board.directions[move_dir][0], y + self.board.directions[move_dir][1]
                if self.board.can_move(x, y, move_dir) and self.board.is_within_bounds(new_x, new_y):
                    for build_dir in self.board.directions:
                        build_x, build_y = new_x + self.board.directions[build_dir][0], new_y + self.board.directions[build_dir][1]
                        if self.board.can_build(new_x, new_y, build_dir, x, y):
                            score = self.evaluate_move(new_x, new_y, build_dir)
                            if score > best_score:
                                best_score = score
                                best_move = (worker, move_dir, build_dir)
        return best_move


    def evaluate_move(self, x, y, build_dir):
        # A simple scoring example: higher levels and central positions score higher
        level_score = self.board.grid[x][y]['level']
        center_score = 2 if (x == 2 and y == 2) else 1 if (1 <= x <= 3 and 1 <= y <= 3) else 0
        return level_score + center_score
