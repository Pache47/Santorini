import copy

class GameManager:
    """
    Manages the game state moves to enable undo/redo functionalities.
    """
    def __init__(self):
        self.moves=[
            # (('B','sw','n'),'blue'),
            # (('Y','e','n'),'white'),
            #  (('A','n','se'),'blue'),
            # (('Y','n','sw'),'white'),
            # (('A','n','s'),'blue'),
            # (('Z','w','w'),'white'), 

        ]
        self.current_index = -1

    def save_state(self,move):
        # Truncate the moves if the current state isn't the last one
        if self.current_index < len(self.moves) - 1:
            self.moves = self.moves[:self.current_index + 1]
        
        # Save the new state and adjust the current index
        if(move):
            self.moves.append(move)
            self.current_index += 1

    def undo(self):
        """
        Reverts to the previous state if possible.
        """
        if self.current_index > 0:
            self.current_index -= 1
            return copy.deepcopy(self.moves[self.current_index])
        return None

    def redo(self):
        """
        Advances to the next state if possible.
        """
        if self.current_index < len(self.moves) - 1:
            self.current_index += 1
            return copy.deepcopy(self.moves[self.current_index])
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
