class Board:
    def __init__(self):
        # Initialize a 5x5 grid, each cell has a dictionary with 'level' and 'worker'
        self.grid = [[{'level': 0, 'worker': None} for _ in range(5)] for _ in range(5)]
        # Directions are stored as tuples of (dx, dy)
        self.directions = {
            'n': (-1, 0), 'ne': (-1, 1), 'e': (0, 1), 'se': (1, 1),
            's': (1, 0), 'sw': (1, -1), 'w': (0, -1), 'nw': (-1, -1)
        }
        # Initial placement of workers
        self.place_workers()

    def place_workers(self):
        # Place workers on the board at the start of the game
        self.grid[1][1]['worker'] = 'Y'
        self.grid[1][3]['worker'] = 'B'
        self.grid[3][1]['worker'] = 'A'
        self.grid[3][3]['worker'] = 'Z'

    def display(self):
        # Display the board state in the console
        print("+--+--+--+--+--+")
        for row in self.grid:
            print('|' + '|'.join(f"{cell['level']}{cell['worker'] if cell['worker'] else ' '}" for cell in row) + '|')
            print("+--+--+--+--+--+")

    def is_within_bounds(self, x, y):
        # Check if coordinates are within the board limits
        return 0 <= x < 5 and 0 <= y < 5

    def can_move(self, from_x, from_y, direction):
        # Determine if a move is possible from a given position in a specific direction
        dx, dy = self.directions[direction]
        new_x, new_y = from_x + dx, from_y + dy
        if not self.is_within_bounds(new_x, new_y):
            return False
        target_cell = self.grid[new_x][new_y]
        return target_cell['worker'] is None and target_cell['level'] <= self.grid[from_x][from_y]['level'] + 1 and target_cell['level'] < 4

    def move_worker(self, from_x, from_y, direction):
        # Execute a worker move if valid
        if self.can_move(from_x, from_y, direction):
            dx, dy = self.directions[direction]
            new_x, new_y = from_x + dx, from_y + dy
            self.grid[new_x][new_y]['worker'], self.grid[from_x][from_y]['worker'] = self.grid[from_x][from_y]['worker'], None
            return True
        return False

    def can_build(self, x, y, direction, old_x, old_y):
        # Check if building is possible in a given direction from a new position
        dx, dy = self.directions[direction]
        build_x, build_y = x + dx, y + dy
        if not self.is_within_bounds(build_x, build_y):
            return False
        target_cell = self.grid[build_x][build_y]
        # Ensure no worker is on the build cell unless it's the old position of the current worker
        if target_cell['worker'] and (build_x, build_y) != (old_x, old_y):
            return False
        return target_cell['level'] < 4

    def build(self, x, y, direction, old_x, old_y):
        # Execute building if valid
        if self.can_build(x, y, direction, old_x, old_y):
            dx, dy = self.directions[direction]
            build_x, build_y = x + dx, y + dy
            self.grid[build_x][build_y]['level'] += 1
            return True
        return False
