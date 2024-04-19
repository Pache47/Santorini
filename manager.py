import copy

class GameManager:
    """
    Manages the game state moves to enable undo and redo functionalities.
    """
    def __init__(self):
        self.moves=[]
        self.current_index = -1  # Tracks the current position in moves

    def save_state(self,move):
        """
        Saves the current state of the game, truncating any forward moves if making a new move after an undo.
        """

        # Truncate the moves if the current state isn't the last one
        if self.current_index < len(self.moves) - 1:
            self.moves = self.moves[:self.current_index + 1]
        
        # Save the new state and adjust the current index
        if(move):
            self.moves.append(move)
            self.current_index += 1
        print("Saved Moves",self.moves)
        # print("Saved state, current moves length:", len(self.moves), "current index:", self.current_index)


    def undo(self):
        """
        Reverts to the previous game state if possible.
        """
        # print(f"Attempting undo from index {self.current_index}, moves length {len(self.moves)}")
        if self.current_index > 0:
            self.current_index -= 1
            # print("Undid to index:", self.current_index)
            return copy.deepcopy(self.moves[self.current_index])
        # print("Undo not possible")
        return None

    def redo(self):
        """
        Advances to the next game state if possible.
        """
        # print(f"Attempting redo from index {self.current_index}, moves length {len(self.moves)}")
        if self.current_index < len(self.moves) - 1:
            self.current_index += 1
            # print("Redid to index:", self.current_index)
            return copy.deepcopy(self.moves[self.current_index])
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
        return self.current_index < len(self.moves) - 1

