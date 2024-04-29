import tkinter as tk
import numpy as np


def check_winner(board, player):
   
    return (np.all(board == player, axis=0).any() or        
            np.all(board == player, axis=1).any() or        
            np.all(np.diag(board) == player) or            
            np.all(np.diag(np.fliplr(board)) == player))   


def game_over(board):
    return check_winner(board, 'X') or check_winner(board, 'O') or np.all(board != ' ')


def evaluate(board):
    if check_winner(board, 'X'):
        return 1
    elif check_winner(board, 'O'):
        return -1
    else:
        return 0


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


def find_best_move(board):
    best_eval = -np.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                eval = minimax(board, 6, -np.inf, np.inf, False)  
                board[i][j] = ' '
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move


def player_move(row, col):
    global board, game_over_flag
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
            ai_move()


def ai_move():
    global board, game_over_flag
    ai_move = find_best_move(board)
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


def update_board():
    for i in range(3):
        for j in range(3):
            if board[i][j] != ' ':
                buttons[i][j].config(text=board[i][j], state=tk.DISABLED)
            else:
                buttons[i][j].config(text=' ', state=tk.NORMAL)


def reset_game():
    global board, game_over_flag
    board = np.array([[' ']*3]*3)
    game_over_flag = False
    update_board()
    result_label.config(text="")



def create_ui():
    global board, buttons, result_label, game_over_flag

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

    reset_game()

    root.mainloop()


create_ui()
