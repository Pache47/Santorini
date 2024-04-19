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
    count = 1
    # if undo_redo_enabled:
    #     game.game_manager.save_state(None)  # Save initial state

    while not game.game_over:
        count +=1
        print("Count ,",count, "Turn :",game.turn_count)
        # Check win condition at the very start of each turn
         # If the game has ended, skip further processing


        game.board.display()  # Display board state at the start of each full turn
        game.show_turn_info()

        if undo_redo_enabled:
            while True:
                current_index = game.game_manager.current_index
                moves = game.game_manager.moves
                if len(moves) < 1:
                    break
                prompt = ""
                if(current_index > -1 and current_index < len(moves)-1):
                    prompt = "undo, redo, or next\n"
                elif(current_index > -1):
                    prompt = "undo, or next\n"
                else:
                    prompt = "redo, or next\n"
                user_input = input(prompt).lower() 
                if user_input == 'redo':
                    if current_index < len(moves)-1:
                        last_move = moves[current_index+1]
                        game.turn_count += 1
                        game.game_manager.current_index +=1
                        game.current_player = last_move[1]
                        move = last_move[0]
                        # execute move
                        x,y = game.worker_positions[move[0]]
                        game.execute_move(move[0],move[1],x,y)
                        x,y = game.worker_positions[move[0]]
                        game.board.build(x,y,move[2])
                        game.board.display()  
                        game.show_turn_info()
                        continue  
                    else:
                        print("No more moves to redo")
                elif user_input == 'undo':
                    if current_index > -1:
                        last_move = moves[current_index]
                        game.turn_count -= 1
                        game.game_manager.current_index -=1
                        game.current_player = last_move[1]
                        move = last_move[0]
                        # execute move
                        x,y = game.worker_positions[move[0]]
                        game.execute_move(move[0],move[1],x,y,reverse=True)
                        # game.board.move_worker(x,y,move[1],True)
                        game.board.build(x,y,move[2],reverse=True)
                        game.board.display()  # Display board state at the start of each full turn
                        game.show_turn_info()
                        continue  # Successfully undid, show updated state
                    else:
                        print("No more moves to undo")
                elif user_input == 'next':
                    break
                else:
                    # print("Invalid input. Please enter 'undo', 'redo', or 'next'.")
                    continue
        move = None

        if game.player_types[game.current_player] == 'human':
            move = game.handle_human_turn()
        else:
            move = game.ai_play_turn()

        if undo_redo_enabled:
            game.game_manager.save_state((move,game.current_player))
    
        if game.check_win_condition():
            break 
        
        game.switch_player()
        game.turn_count += 1

    restart = input("Play again?\n")
    if restart.lower() == 'yes':
        main()

if __name__ == "__main__":
    main()







# next works but not undo and redo


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





#undo works, redo does not work and print not consistent,

# import sys
# from game import Game

# def parse_arguments():
#     """
#     Parses command line arguments to configure game settings.
#     """
#     # Default settings
#     player1_type = 'human'
#     player2_type = 'human'
#     undo_redo_enabled = False
#     score_display = False

#     # Assign values based on command line arguments
#     if len(sys.argv) > 1:
#         player1_type = sys.argv[1].lower()
#     if len(sys.argv) > 2:
#         player2_type = sys.argv[2].lower()
#     if len(sys.argv) > 3:
#         undo_redo_enabled = sys.argv[3].lower() == 'on'
#     if len(sys.argv) > 4:
#         score_display = sys.argv[4].lower() == 'on'

#     return player1_type, player2_type, undo_redo_enabled, score_display

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
