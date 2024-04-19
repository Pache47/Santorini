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

    player_types = [
        "human",
        "heuristic",
        "random"
    ]


    # Assign values based on command line arguments
    if len(sys.argv) > 1:
        if(sys.argv[1].lower() in player_types):
            player1_type = sys.argv[1].lower()
        else:
            print("Invalid player type for white player")
            exit()
    if len(sys.argv) > 2:
        if(sys.argv[2].lower() in player_types):
            player2_type = sys.argv[2].lower()
        else:
            print("Invalid player type for blue player")
            exit()
    if len(sys.argv) > 3:
        if(sys.argv[3].lower() == 'on' or sys.argv[3].lower() == 'off'):
            undo_redo_enabled = sys.argv[3].lower() == 'on'
        else:
            print("Invalid value for enable undo/redo (on/off)")
            exit()
    if len(sys.argv) > 4:
        if(sys.argv[3].lower() == 'on' or sys.argv[3].lower() == 'off'):
            score_display = sys.argv[4].lower() == 'on'
        else:
            print("Invalid value for enable score display (on/off)")
            exit()

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
    restart = input("Play again (yes/no)?\n")
    if restart.lower() == 'yes':
        main()

if __name__ == "__main__":
    main()
