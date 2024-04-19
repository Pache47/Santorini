import sys
from game import Game
import copy

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


#stable main: undo and redo doesn't work, next works and print is consistent
def main():
    player1_type, player2_type, undo_redo_enabled, score_display = parse_arguments()
    game = Game(player1_type, player2_type, undo_redo_enabled, score_display)

    if undo_redo_enabled:
        game.game_manager.save_state(copy.deepcopy(game))  # Save initial state    

    while not game.game_over:
        # Check win condition at the very start of each turn
        if game.check_win_condition():
            continue  # If the game has ended, skip further processing


        game.board.display()  # Display board state at the start of each full turn
        game.show_turn_info()

        if undo_redo_enabled:
            while True:
                user_input = input("undo, redo, or next\n").lower()
                if user_input == 'redo':
                    if game.redo():
                        continue  # Successfully redid, show updated state
                # elif user_input == 'undo':
                #     if game.undo():
                #         continue  # Successfully undid, show updated state
                #     else:
                #         print("No more moves to undo")
                elif user_input == 'next':
                    break
                else:
                    # print("Invalid input. Please enter 'undo', 'redo', or 'next'.")
                    continue

        if game.player_types[game.current_player] == 'human':
            game.handle_human_turn()
        else:
            game.ai_play_turn()

        if not game.game_over:
            game.switch_player()
            game.turn_count += 1

    restart = input("Play again?\n")
    if restart.lower() == 'yes':
        main()

if __name__ == "__main__":
    main()



# undo skips a turn when appling multiple times
#next works and print is consistent
#redo not working
# unstable --> infintly loops when ai vs ai with undo_redo set to off and score set to on 

# def main():
#     player1_type, player2_type, undo_redo_enabled, score_display = parse_arguments()
#     game = Game(player1_type, player2_type, undo_redo_enabled, score_display)

#     if undo_redo_enabled:
#         game.game_manager.save_state(copy.deepcopy(game))  # Save initial state

#     while not game.game_over:
#         game.board.display()  # Display board state at the start of each full turn
#         game.show_turn_info()

#         action = 'next' # Default action to take if undo/redo is not enabled
#         if undo_redo_enabled:
#             action = None
#             while action not in ['next', 'undo', 'redo']:
#                 action = input("undo, redo, or next\n").lower()
#                 if action == 'undo':
#                     if not game.undo():
#                         print("No more moves to undo")
#                 elif action == 'redo': # redo not working
#                     if not game.redo():
#                         print("No further state to redo") # we don't need to print
                        
#                 # elif action == 'next':
#                 #     break
        
#         if action == 'next':
#             if game.player_types[game.current_player] == 'human':
#                 game.handle_human_turn()
#             else:
#                 game.ai_play_turn()

#             if not game.game_over:
#                 game.switch_player()
#                 game.turn_count += 1

#             if undo_redo_enabled and not game.game_over:
#                 game.game_manager.save_state(copy.deepcopy(game))  # Save state at the end of turn

#     restart = input("Play again?\n")
#     if restart.lower() == 'yes':
#         main()

# if __name__ == "__main__":
#     main()



# #undo skips steps, 
#redo does not work, just prints again 
#next prints turn and board twice
#stable v2

# def main():
#     """
#     Main function to set up and start the game.
#     """
#     player1_type, player2_type, undo_redo_enabled, score_display = parse_arguments()
#     game = Game(player1_type, player2_type, undo_redo_enabled, score_display)

#     while not game.game_over:
#         game.board.display()  # Display board state at the start of the turn
#         game.show_turn_info()  # Display current turn info and scores if enabled

#         if undo_redo_enabled:
#             # Handle undo/redo/next input from user
#             while True:
#                 user_input = input("undo, redo, or next\n").lower()
#                 if user_input == 'undo':
#                     if game.undo():
#                         game.board.display()
#                         game.show_turn_info()
#                     else:
#                         # No undo available, just display the current state again
#                         print("No more moves to undo.")
#                         game.board.display()
#                         game.show_turn_info()
#                     continue
#                 elif user_input == 'redo':
#                     if game.redo():
#                         game.board.display()
#                         game.show_turn_info()
#                     else:
#                         # No redo available, just display the current state again
#                         game.board.display()
#                         game.show_turn_info()
#                     continue
#                 elif user_input == 'next':
#                     break
#                 else:
#                     print("Invalid input. Please enter 'undo', 'redo', or 'next'.")
#                     continue

#         game.play_turn()
        
#     # Option to restart the game based on user input
#     restart = input("Play again?\n")
#     if restart.lower() == 'yes':
#         main()

# if __name__ == "__main__":
#     main()




# next works but undo/redo does not
# def main():
#     player1_type, player2_type, undo_redo_enabled, score_display = parse_arguments()
#     game = Game(player1_type, player2_type, undo_redo_enabled, score_display)

#     while not game.game_over:
#         # Display the board state and turn info at the start of each full turn only
#         game.board.display()  
#         game.show_turn_info()  

#         if undo_redo_enabled:
#             action_taken = False  # This will track if an action (move, undo, redo) was taken
#             while not action_taken:
#                 user_input = input("undo, redo, or next\n").lower()
#                 if user_input == 'undo':
#                     if game.undo():
#                         game.board.display()
#                         game.show_turn_info()
#                     # else:
#                     #     print("No more moves to undo.")
#                     continue
#                 elif user_input == 'redo':
#                     if game.redo():
#                         game.board.display()
#                         game.show_turn_info()
#                     # else:
#                     #     print("No changes to redo.")  # Redo with no change will not reprint the board
#                     continue
#                 elif user_input == 'next':
#                     action_taken = True  # Breaks the loop without additional display
#                 else:
#                     print("Invalid input. Please enter 'undo', 'redo', or 'next'.")
#                     continue

#         if game.player_types[game.current_player] == 'human':
#             game.handle_human_turn()  # Handle human player's turn
#         else:
#             game.ai_play_turn()  # AI takes a turn

#         if not game.game_over:
#             game.switch_player()
#             game.turn_count += 1

#     # Option to restart the game based on user input
#     restart = input("Play again? (yes/no)\n")
#     if restart.lower() == 'yes':
#         main()

# if __name__ == "__main__":
#     main()
