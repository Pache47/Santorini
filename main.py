import sys
from game import Game

def parse_arguments():
    """
    Parses command line arguments to configure game settings.
    """
    # Default settings
    player1_type = 'human'
    player2_type = 'human'
    undo_redo_enabled = False
    score_display = False

    # Assign values based on command line arguments
    if len(sys.argv) > 1:
        player1_type = sys.argv[1].lower()
    if len(sys.argv) > 2:
        player2_type = sys.argv[2].lower()
    if len(sys.argv) > 3:
        undo_redo_enabled = sys.argv[3].lower() == 'on'
    if len(sys.argv) > 4:
        score_display = sys.argv[4].lower() == 'on'

    return player1_type, player2_type, undo_redo_enabled, score_display

def main():
    """
    Main function to set up and start the game.
    """
    player1_type, player2_type, undo_redo_enabled, score_display = parse_arguments()
    game = Game(player1_type, player2_type, undo_redo_enabled, score_display)
    while not game.game_over:
        game.play_turn()

    # Option to restart the game based on user input
    restart = input("Play again?\n")
    if restart.lower() == 'yes':
        main()

if __name__ == "__main__":
    main()
