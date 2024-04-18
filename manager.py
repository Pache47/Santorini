import copy

class GameManager:
    """
    Manages the game state history to enable undo and redo functionalities.
    """
    def __init__(self):
        self.history = []  # List to store game states
        self.current_index = -1  # Tracks the current position in history

    def save_state(self, game_state):
        """
        Saves the current state of the game, truncating any forward history if making a new move after an undo.
        """
        # Truncate the history if the current state isn't the last one
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]
        
        # Save the new state and adjust the current index
        self.history.append(copy.deepcopy(game_state))
        self.current_index += 1
        # print("Saved state, current history length:", len(self.history), "current index:", self.current_index)


    def undo(self):
        """
        Reverts to the previous game state if possible.
        """
        # print(f"Attempting undo from index {self.current_index}, history length {len(self.history)}")
        if self.current_index > 0:
            self.current_index -= 1
            # print("Undid to index:", self.current_index)
            return copy.deepcopy(self.history[self.current_index])
        # print("Undo not possible")
        return None

    def redo(self):
        """
        Advances to the next game state if possible.
        """
        # print(f"Attempting redo from index {self.current_index}, history length {len(self.history)}")
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            # print("Redid to index:", self.current_index)
            return copy.deepcopy(self.history[self.current_index])
        # print("Redo not possible")
        return None

    def can_undo(self):
        """
        Returns True if an undo operation is possible.
        """
        return self.current_index > 0

    def can_redo(self):
        """
        Returns True if a redo operation is possible.
        """
        return self.current_index < len(self.history) - 1

