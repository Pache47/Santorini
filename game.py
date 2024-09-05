from board import Board
from player import RandomAI, HeuristicAI
from score import ScoringSystem
from manager import GameManager

class Game:
    """Class to represent the game logic and flow."""
    def __init__(self, player1_type='human', player2_type='human', undo_redo_enabled=False, score_display=False):
        self.board = Board()
        self.game_manager = GameManager()
        self.undo_redo_enabled = undo_redo_enabled
        self.current_player = 'white'
        self.turn_count = 1
        self.game_over = False
        self.players = {'white': ['A', 'B'], 'blue': ['Y', 'Z']}
        self.worker_positions = {'A': (3, 1), 'B': (1, 3), 'Y': (1, 1), 'Z': (3, 3)}
        self.player_types = {'white': player1_type, 'blue': player2_type}
        self.score_display = score_display
        self.scoring_system = ScoringSystem(self.board, self.worker_positions)
        self.player_ai = {'white': None, 'blue': None}
        self.initialize_players()

    def initialize_players(self):
        opponent_workers = {
            'white': self.players['blue'],
            'blue': self.players['white']
        }

        for color in ['white', 'blue']:
            if self.player_types[color] == 'heuristic':
                self.player_ai[color] = HeuristicAI(self.board, self.players[color], self.worker_positions, opponent_workers[color], self.scoring_system)
            elif self.player_types[color] == 'random':
                self.player_ai[color] = RandomAI(self.board, self.players[color], self.worker_positions)
        
    def switch_player(self):
        self.current_player = 'blue' if self.current_player == 'white' else 'white'

    def handle_human_turn(self):
        while True:
            worker = self.get_worker_input()
            x, y = self.worker_positions[worker]
            [move_direction,new_x, new_y] = self.get_move_direction(worker,x,y)
           
            if new_x is not None:
                build_direction = self.get_build_direction(new_x, new_y, x, y)
                if build_direction:
                    move = (worker,move_direction,build_direction)
                    if self.score_display:
                        scores = self.scoring_system.calculate_scores(self.players[self.current_player], self.players['blue' if self.current_player == 'white' else 'white'])
                        print(f"{worker},{move_direction},{build_direction} ({scores[0]}, {scores[1]}, {scores[2]})")
                    else:
                        print(f"{worker},{move_direction},{build_direction}")
                    return move

    def get_worker_input(self):
        # Get the worker input from the user
        while True:
            worker = input("Select a worker to move\n").upper()
            if worker in self.players[self.current_player]:
                return worker
            print("Not a valid worker" if worker not in 'ABYZ' else "That is not your worker")

    def get_move_direction(self,worker,x,y):
        # Get the move direction from the user
        while True:
            direction = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n").lower()
            if direction in self.board.directions:
                new_x, new_y = self.execute_move(worker, direction, x, y)
                if(new_x is not None):
                    return [direction,new_x,new_y]
            else:
                print("Not a valid direction")

    def execute_move(self, worker, direction, x, y,reverse=False):
        # Execute a move if valid
        dx, dy = self.board.directions[direction]
        if (reverse):
            dx*=-1
            dy*=-1
        new_x, new_y = x + dx, y + dy
        if reverse or self.board.can_move(x, y, direction):
            self.board.move_worker(x, y, direction,reverse)
            self.worker_positions[worker] = (new_x, new_y)
            return new_x, new_y
        else:
            print(f"Cannot move {direction}")
            return None, None

    def get_build_direction(self, new_x, new_y, old_x, old_y):
        # Get the build direction from the user
        while True:
            direction = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n").lower()
            if direction in self.board.directions:
                if self.board.can_build(new_x, new_y, direction, old_x, old_y):
                    self.board.build(new_x, new_y, direction, old_x, old_y)
                    return direction
                else:
                    print(f"Cannot build {direction}")
            else:
                print("Not a valid direction")

    def ai_play_turn(self):
        # AI player selects a move
        ai = self.player_ai[self.current_player]
        if ai:
            move = ai.select_move()
            if move:
                worker, move_direction, build_direction = move
                x, y = self.worker_positions[worker]
                new_x, new_y = self.execute_move(worker, move_direction, x, y)
                if new_x is not None:
                    if self.board.build(new_x, new_y, build_direction, x, y):
                        if self.score_display:
                            scores = self.scoring_system.calculate_scores(self.players[self.current_player], self.players['blue' if self.current_player == 'white' else 'white'])
                            print(f"{worker},{move_direction},{build_direction} ({scores[0]}, {scores[1]}, {scores[2]})")
                        else:
                            print(f"{worker},{move_direction},{build_direction}")

                        return move
    
    def check_win_condition(self):
        # Check if any worker is on level 3
        for worker, (x, y) in self.worker_positions.items():
            if self.board.grid[x][y]['level'] == 3:
                self.game_over = True
                self.board.display()
                # Display the next turn information
                next_player = 'blue' if self.current_player == 'white' else 'white'
                workers = ''.join(self.players[next_player])
                turn_info = f"Turn: {self.turn_count + 1}, {next_player} ({workers})"
                
                # Calculate and display the score if scoring is enabled
                if self.score_display:
                    scores = self.scoring_system.calculate_scores(self.players[self.current_player],
                    self.players['blue' if self.current_player == 'white' else 'white'])
                    print(f"{turn_info}, ({scores[0]}, {scores[1]}, {scores[2]})")
                else:
                    print(turn_info)
                
                print(f"{self.current_player} has won")
                return True
        return False

    def undo(self):
        previous_state = self.game_manager.undo()
        if previous_state:
            self.__dict__.update(previous_state.__dict__)
            self.board.display()
            self.show_turn_info()
            return True
        return False

    def redo(self):
        next_state = self.game_manager.redo()
        if next_state:
            self.__dict__.update(next_state.__dict__)
            self.board.display()
            self.show_turn_info()
            return True
        else:
            self.board.display()
            self.show_turn_info()
            return False

    def show_turn_info(self):
        #helper function to display the current turn information
        workers = ''.join(self.players[self.current_player])
        if self.score_display:
            scores = self.scoring_system.calculate_scores(
                self.players[self.current_player],
                self.players['blue' if self.current_player == 'white' else 'white']
            )
            print(f"Turn: {self.turn_count}, {self.current_player} ({workers}), ({scores[0]}, {scores[1]}, {scores[2]})")
        else:
            print(f"Turn: {self.turn_count}, {self.current_player} ({workers})")
