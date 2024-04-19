from board import Board
from player import RandomAI, HeuristicAI

class Game:
    def __init__(self, player1_type='human', player2_type='human', undo_redo_enabled=False, score_display=False):
        self.board = Board()
        self.current_player = 'white'
        self.turn_count = 1
        self.game_over = False
        self.players = {'white': ['A', 'B'], 'blue': ['Y', 'Z']}
        self.worker_positions = {'A': (3, 1), 'B': (1, 3), 'Y': (1, 1), 'Z': (3, 3)}
        self.player_types = {'white': player1_type, 'blue': player2_type}
        self.initialize_players()

    def initialize_players(self):
        # Initialize AI based on the type of player
        self.player_ai = {
            'blue': RandomAI(self.board, self.players['blue'], self.worker_positions) if self.player_types['blue'] == 'random'
            else HeuristicAI(self.board, self.players['blue'], self.worker_positions) if self.player_types['blue'] == 'heuristic'
            else None,
            'white': RandomAI(self.board, self.players['white'], self.worker_positions) if self.player_types['white'] == 'random'
            else HeuristicAI(self.board, self.players['white'], self.worker_positions) if self.player_types['white'] == 'heuristic'
            else None
        }

    def switch_player(self):
        self.current_player = 'blue' if self.current_player == 'white' else 'white'

    def play_turn(self):
        self.board.display()
        workers = ''.join(self.players[self.current_player])
        print(f"Turn: {self.turn_count}, {self.current_player} ({workers})")

        if self.player_types[self.current_player] == 'human':
            worker, move_direction, build_direction = self.handle_human_turn()
            print(f"{worker},{move_direction},{build_direction}")
        else:
            self.ai_play_turn()

        if self.check_win_condition():
            return

        self.switch_player()
        self.turn_count += 1

    def handle_human_turn(self):
        while True:
            worker = self.get_worker_input()
            x, y = self.worker_positions[worker]
            [move_direction,new_x, new_y] = self.get_move_direction(worker,x,y)
           
            if new_x is not None:
                build_direction = self.get_build_direction(new_x, new_y, x, y)
                if build_direction:
                    return worker, move_direction, build_direction

    def get_worker_input(self):
        while True:
            worker = input("Select a worker to move\n").upper()
            if worker in self.players[self.current_player]:
                return worker
            print("Not a valid worker" if worker not in 'ABYZ' else "That is not your worker")

    def get_move_direction(self,worker,x,y):
        while True:
            direction = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n").lower()
            if direction in self.board.directions:
                new_x, new_y = self.execute_move(worker, direction, x, y)
                if(new_x is not None):
                    return [direction,new_x,new_y]
            else:
                print("Not a valid direction")

    def execute_move(self, worker, direction, x, y):
        new_x, new_y = x + self.board.directions[direction][0], y + self.board.directions[direction][1]
        if self.board.can_move(x, y, direction):
            self.board.move_worker(x, y, direction)
            self.worker_positions[worker] = (new_x, new_y)
            return new_x, new_y
        print(f"Cannot move {direction}")
        return None, None

    def get_build_direction(self, new_x, new_y, old_x, old_y):
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

    # def ai_play_turn(self):
    #     ai = self.player_ai[self.current_player]
    #     if ai:
    #         move = ai.select_move()
    #         if move:
    #             worker, move_direction, build_direction = move
    #             x, y = self.worker_positions[worker]
    #             self.execute_move(worker, move_direction, x, y)
    #             print(f"{worker},{move_direction},{build_direction}")

    def ai_play_turn(self):
        ai = self.player_ai[self.current_player]
        if ai:
            move = ai.select_move()
            if move:
                worker, move_direction, build_direction = move
                x, y = self.worker_positions[worker]
                # Execute the move if valid
                if self.board.move_worker(x, y, move_direction):
                    new_x, new_y = x + self.board.directions[move_direction][0], y + self.board.directions[move_direction][1]
                    self.worker_positions[worker] = (new_x, new_y)
                    # Execute the build if possible
                    if self.board.build(new_x, new_y, build_direction, x, y):
                        print(f"{worker},{move_direction},{build_direction}")

    def check_win_condition(self):
        # Check if any worker is on level 3
        for worker, (x, y) in self.worker_positions.items():
            if self.board.grid[x][y]['level'] == 3:
                self.game_over = True
                print(f"{self.current_player} has won")
                return True
        return False
