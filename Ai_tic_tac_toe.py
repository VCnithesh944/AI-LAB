import math

def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

def is_moves_left(board):
    for row in board:
        if ' ' in row:
            return True
    return False

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None

def is_game_over(board):
    return check_winner(board) is not None or not is_moves_left(board)

def evaluate(board, AI_PLAYER, HUMAN_PLAYER):
    winner = check_winner(board)
    if winner == AI_PLAYER:
        return +10
    elif winner == HUMAN_PLAYER:
        return -10
    else:
        return 0

def minimax(board, depth, is_max, AI_PLAYER, HUMAN_PLAYER):
    score = evaluate(board, AI_PLAYER, HUMAN_PLAYER)

    if score == 10 or score == -10:
        return score
    if not is_moves_left(board):
        return 0

    if is_max:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = AI_PLAYER
                    best = max(best, minimax(board, depth+1, False, AI_PLAYER, HUMAN_PLAYER))
                    board[i][j] = ' '
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = HUMAN_PLAYER
                    best = min(best, minimax(board, depth+1, True, AI_PLAYER, HUMAN_PLAYER))
                    board[i][j] = ' '
        return best

def find_best_move(board, AI_PLAYER, HUMAN_PLAYER):
    best_val = -math.inf
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = AI_PLAYER
                move_val = minimax(board, 0, False, AI_PLAYER, HUMAN_PLAYER)
                board[i][j] = ' '
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move

def main():
    BOARD = [[' ' for _ in range(3)] for _ in range(3)]
    HUMAN_PLAYER = 'X'
    AI_PLAYER = 'O'
    CURRENT_PLAYER = HUMAN_PLAYER  # You can randomize this if you want

    while not is_game_over(BOARD):
        print("\nCurrent board:")
        print_board(BOARD)

        if CURRENT_PLAYER == HUMAN_PLAYER:
            try:
                move = int(input("Enter your move (0-8): "))
                if move < 0 or move > 8:
                    print("Invalid move. Choose from 0 to 8.")
                    continue
                row, col = divmod(move, 3)
                if BOARD[row][col] != ' ':
                    print("Cell already occupied. Try again.")
                    continue
                BOARD[row][col] = HUMAN_PLAYER
                CURRENT_PLAYER = AI_PLAYER
            except ValueError:
                print("Invalid input. Please enter a number from 0 to 8.")
                continue
        else:
            print("AI is thinking...")
            row, col = find_best_move(BOARD, AI_PLAYER, HUMAN_PLAYER)
            BOARD[row][col] = AI_PLAYER
            CURRENT_PLAYER = HUMAN_PLAYER

    print("\nFinal board:")
    print_board(BOARD)

    winner = check_winner(BOARD)
    if winner == HUMAN_PLAYER:
        print("Congratulations! You win!")
    elif winner == AI_PLAYER:
        print("AI wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
