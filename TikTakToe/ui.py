import tkinter as tk
import numpy as np

# Function to check if a player has won
def check_winner(board, player):
    # Check rows, columns, and diagonals
    return (np.all(board == player, axis=0).any() or        # Columns
            np.all(board == player, axis=1).any() or        # Rows
            np.all(np.diag(board) == player) or            # Main diagonal
            np.all(np.diag(np.fliplr(board)) == player))   # Anti-diagonal

# Function to check if the game is over
def game_over(board):
    return check_winner(board, 'X') or check_winner(board, 'O') or np.all(board != ' ')

# Function to evaluate the score of the board
def evaluate(board):
    if check_winner(board, 'X'):
        return 1
    elif check_winner(board, 'O'):
        return -1
    else:
        return 0

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if game_over(board) or depth == 0:
        return evaluate(board)
    
    if maximizing_player:
        max_eval = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth - 1, alpha, beta, False)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth - 1, alpha, beta, True)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Function to find the best move using minimax
def find_best_move(board):
    best_eval = -np.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                eval = minimax(board, 4, -np.inf, np.inf, False)
                board[i][j] = ' '
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move

# Function to handle player's move
# Function to handle player's move
def player_move(row, col):
    global board, game_over_flag, ai_loading_label
    print("Player made a move at row:", row, "column:", col)
    if board[row][col] == ' ' and not game_over_flag:
        board[row][col] = 'O'
        update_board()
        if game_over(board):
            game_over_flag = True
            if check_winner(board, 'X'):
                result_label.config(text="AI wins!")
            elif check_winner(board, 'O'):
                result_label.config(text="Player wins!")
            else:
                result_label.config(text="It's a tie!")
        else:
            ai_loading_label.config(text="AI is deciding...")
            ai_move()  # Call ai_move immediately after player's move


# Function to handle AI's move
# Function to handle AI's move
# Function to handle AI's move
def ai_move():
    global board, game_over_flag, ai_loading_label
    print("AI is making a move...")
    ai_loading_label.config(text="AI is deciding...")
    board_copy = np.copy(board)  # Create a copy of the board
    ai_move = find_best_move(board_copy)
    print("AI's move:", ai_move)
    if ai_move is None:
        print("AI couldn't find a valid move.")
        return
    board[ai_move[0]][ai_move[1]] = 'X'
    update_board()
    if game_over(board):
        game_over_flag = True
        if check_winner(board, 'X'):
            result_label.config(text="AI wins!")
        elif check_winner(board, 'O'):
            result_label.config(text="Player wins!")
        else:
            result_label.config(text="It's a tie!")
    else:
        ai_loading_label.config(text="")


# Function to update the board UI
def update_board():
    for i in range(3):
        for j in range(3):
            if board[i][j] != ' ':
                buttons[i][j].config(text=board[i][j], state=tk.DISABLED, bg='lightgray')
            else:
                buttons[i][j].config(text=' ', state=tk.NORMAL, bg='white')

# Function to reset the game
def reset_game():
    global board, game_over_flag
    board = np.array([[' ']*3]*3)
    game_over_flag = False
    update_board()
    result_label.config(text="")
    ai_loading_label.config(text="")

# Main function to create the UI
def create_ui():
    global board, buttons, result_label, game_over_flag, ai_loading_label

    root = tk.Tk()
    root.title("Tic Tac Toe")

    board = np.array([[' ']*3]*3)
    game_over_flag = False

    buttons = [[None]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(root, text=' ', font=('Arial', 20), width=6, height=3,
                                       command=lambda row=i, col=j: player_move(row, col))
            buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

    result_label = tk.Label(root, text='', font=('Arial', 16))
    result_label.grid(row=3, columnspan=3, padx=5, pady=10)

    reset_button = tk.Button(root, text='Reset', font=('Arial', 12), width=10, height=2, command=reset_game)
    reset_button.grid(row=4, columnspan=3, padx=5, pady=5)

    ai_loading_label = tk.Label(root, text='', font=('Arial', 12))
    ai_loading_label.grid(row=5, columnspan=3, padx=5, pady=5)

    reset_game()

    root.mainloop()

# Run the UI
create_ui()
