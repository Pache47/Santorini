import sys
from game import Game

def parse_arguments():
    """Parses command line arguments to configure game settings."""
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
            print("Invalid player type one")
            exit()
    if len(sys.argv) > 2:
        if(sys.argv[2].lower() in player_types):
            player2_type = sys.argv[2].lower()
        else:
            print("Invalid player type two")
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
            print("Invalid value for enable score (on/off)")
            exit()

    return player1_type, player2_type, undo_redo_enabled, score_display


def main():
    """Main function to set up and start the game."""

    player1_type, player2_type, undo_redo_enabled, score_display = parse_arguments()
    game = Game(player1_type, player2_type, undo_redo_enabled, score_display)
    count = 1
        
    # Check win condition at start
    while not game.game_over:
        count +=1

        game.board.display()
        game.show_turn_info()

        if undo_redo_enabled:
            while True:
                current_index = game.game_manager.current_index
                moves = game.game_manager.moves
                prompt = "undo, redo, or next\n"
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
                        game.board.display()  
                        game.show_turn_info()
                        continue
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
                        game.board.build(x,y,move[2],reverse=True)
                        game.board.display()
                        game.show_turn_info()
                        continue
                    else:
                        game.board.display()
                        game.show_turn_info()
                        continue
                elif user_input == 'next':
                    break
                else:
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
