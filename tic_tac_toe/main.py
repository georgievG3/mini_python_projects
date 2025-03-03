def print_board(board):
    return "\n".join(" ".join(row) for row in board)


def check_inputs():
    while True:
        valid_inputs = ['x', 'o']
        player_one = input('PLayer 1 please choose "x" or "o" -->')
        if player_one not in valid_inputs:
            print("Please enter valid input!")
            continue
        player_two = 'o' if player_one == 'x' else 'x'
        print(f'Player 1 is with the "{player_one}" and Player 2 is with the "{player_two}"')
        return player_one, player_two


def check_moves(move, board, used_spots, moves, player_one, player_two):
    if move in used_spots:
        print('Please choose a spot that has not been used!')
        return False
    move_map = {
        "1": (0, 0), "2": (0, 1), "3": (0, 2),
        "4": (1, 0), "5": (1, 1), "6": (1, 2),
        "7": (2, 0), "8": (2, 1), "9": (2, 2)
    }
    if move in move_map:
        row, col = move_map[move]
        board[row][col] = player_one if moves % 2 == 0 else player_two
        return True
    return False


def check_win(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "_":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "_":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "_":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "_":
        return board[0][2]
    return None


def check_draw(board):
    if not check_win(board):
        for row in board:
            if "_" in row:
                return False
        return True
    return False


def game():
    global stats
    used_spots = set()
    moves = 0
    board = [["_" for _ in range(3)] for _ in range(3)]
    player_one, player_two = check_inputs()

    print("Let's begin!")
    while True:
        print(print_board(board))
        move = input("Please choose a spot:")
        if check_moves(move, board, used_spots, moves, player_one, player_two):
            used_spots.add(move)
            moves += 1
            winner = check_win(board)
            if winner:
                if winner == player_one:
                    stats['player_one'] += 1
                else:
                    stats['player_two'] += 1
                print(print_board(board))
                print(f"Congratulations, '{winner}' won!")
                break
            if check_draw(board):
                print("Draw!")
                stats['draws'] += 1
                break

    command = input("Do you want to play again? (y/n)")
    if command == 'y':
        game()
    else:
        print("Thank you for playing!")
        print(f"Player 1 wins: {stats['player_one']}")
        print(f"Player 2 wins: {stats['player_two']}")
        print(f"Draws: {stats['draws']}")


print('Welcome to Tic-Tac-Toe!')
stats = {'player_one': 0, 'player_two': 0, 'draws': 0}
game()