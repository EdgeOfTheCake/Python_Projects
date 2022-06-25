from player import HumanPlayer, RandomComputerPlayer, UnbeatableComputer
from tic_tac_toe import TicTacToe, play_tic_tac_toe


if __name__ == "__main__":
    # Human vs Random Choice Computer
    x_player = HumanPlayer("X")
    o_player = RandomComputerPlayer("O")
    game = TicTacToe()
    play_tic_tac_toe(game, x_player, o_player, print_game=True)

    # # Human vs Human
    # x_player = HumanPlayer("X")
    # o_player = HumanPlayer("O")
    # game = TicTacToe()
    # play_tic_tac_toe(game, x_player, o_player, print_game=True) 


    # # Human vs Unbeatable Computer
    # x_player = HumanPlayer("X")
    # o_player = UnbeatableComputer("O")
    # game = TicTacToe()
    # play_tic_tac_toe(game, x_player, o_player, print_game=True) 

    # # Unbeatable Computer vs Random Choice Computer (be aweare, this takes a few minutes to finish)
    # x_wins = 0
    # o_wins = 0
    # ties = 0
    # for i in range(10000):
    #     x_player = UnbeatableComputer("X")
    #     o_player = RandomComputerPlayer("O")
    #     game = TicTacToe()
    #     result = play_tic_tac_toe(game, x_player, o_player, print_game=False)
    #     if result == "X":
    #         x_wins += 1
    #     elif result == "O":
    #         o_wins += 1
    #     else:
    #         ties += 1

    # print(f"The result after 10000 iterations are: X wins: {x_wins}, O wins: {o_wins}, ties: {ties}")



