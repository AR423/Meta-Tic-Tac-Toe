import tkinter as tk
from tkinter import messagebox
import random
import math

class MetaTicTacToe:
    def __init__(self, master):
        self.master = master
        master.title("Meta Tic-Tac-Toe")

        # Initialize game variables
        self.board = [[[[ ' ' for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.grid_status = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # Player is 'X'
        self.last_move = None  # Track the last move
        self.frames = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = [[[[None for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]

        self.create_widgets()

    def create_widgets(self):
        for grid_row in range(3):
            for grid_col in range(3):
                frame = tk.Frame(self.master, width=200, height=200, borderwidth=2, relief="solid", bg="white")
                frame.grid(row=grid_row, column=grid_col, padx=2, pady=2)
                self.frames[grid_row][grid_col] = frame

                for row in range(3):
                    for col in range(3):
                        btn = tk.Button(frame, text=' ', font=('Arial', 16), width=5, height=2,
                                        bg="#fffacd", activebackground="#ada988",
                                        command=lambda gr=grid_row, gc=grid_col, r=row, c=col: self.make_move(gr, gc, r, c))
                        btn.grid(row=row, column=col, padx=1, pady=1)
                        self.buttons[grid_row][grid_col][row][col] = btn

        self.update_highlight()

    def update_highlight(self):
        # Highlight the next grid
        if self.last_move:
            next_grid_row, next_grid_col = self.last_move[0] % 3, self.last_move[1] % 3
            for r in range(3):
                for c in range(3):
                    if (r, c) == (next_grid_row, next_grid_col):
                        self.frames[r][c].config(bg="yellow")
                    else:
                        self.frames[r][c].config(bg="white")
        else:
            for r in range(3):
                for c in range(3):
                    self.frames[r][c].config(bg="white")
    
    def draw_large_symbol(self, grid_row, grid_col, symbol):
        frame = self.frames[grid_row][grid_col]
        frame.config(bg="grey")  # Set background to grey for completed grid
        
        # Remove any existing labels (if any) before adding a new one
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Create a label to show the large symbol (X, O, D) in the center of the grid
        label = tk.Label(frame, text=symbol, font=('Arial', 80, 'bold'), fg='white', bg='grey')
        label.place(relx=0.5, rely=0.5, anchor="center")  # Center the label in the frame

    def make_move(self, grid_row, grid_col, row, col):
        # Ensure the move is valid
        if self.grid_status[grid_row][grid_col] is not None:
            messagebox.showinfo("Invalid Move", "This grid is closed!")
            return

        # Enforce the grid-specific move constraint
        if self.last_move:
            expected_grid_row, expected_grid_col = self.last_move[0] % 3, self.last_move[1] % 3
            if (grid_row, grid_col) != (expected_grid_row, expected_grid_col) and self.grid_status[expected_grid_row][expected_grid_col] is None:
                messagebox.showinfo("Invalid Move", "You must play in the highlighted grid!")
                return

        # Make the player's move
        if self.board[grid_row][grid_col][row][col] == ' ':
            self.board[grid_row][grid_col][row][col] = self.current_player
            self.buttons[grid_row][grid_col][row][col].config(text=self.current_player, state="disabled")

            # Check if the player won the small grid
            if self.check_small_grid_winner(grid_row, grid_col, 'X'):
                self.grid_status[grid_row][grid_col] = 'X'
                self.draw_large_symbol(grid_row, grid_col, 'X')
            elif self.check_small_grid_winner(grid_row, grid_col, 'O'):
                self.grid_status[grid_row][grid_col] = 'O'
                self.draw_large_symbol(grid_row, grid_col, 'O')

            # Check for draw in small grid
            if self.check_draw(grid_row, grid_col):
                self.grid_status[grid_row][grid_col] = 'D'
                self.draw_large_symbol(grid_row, grid_col, 'D')

            # Check if the game is over
            if self.check_large_grid_winner('X'):
                messagebox.showinfo("Game Over", "Player X wins!")
                self.reset_game()
                return
            if self.check_large_grid_winner('O'):
                messagebox.showinfo("Game Over", "AI (O) wins!")
                self.reset_game()
                return

            # Switch to the AI and make its move
            self.last_move = (row, col)
            self.current_player = 'O'
            self.update_highlight()
            self.master.after(500, self.computer_move)

    def computer_move(self):
        # Use Minimax with Alpha-Beta pruning to determine the best move
        best_move = self.minimax(self.board, 2, -math.inf, math.inf, True, self.last_move)
        grid_row, grid_col, row, col = best_move[1]

        # Make the AI's move
        self.board[grid_row][grid_col][row][col] = 'O'
        self.buttons[grid_row][grid_col][row][col].config(text='O', state="disabled")

        # Check if the AI won the small grid
        if self.check_small_grid_winner(grid_row, grid_col, 'O'):
            self.grid_status[grid_row][grid_col] = 'O'
            self.draw_large_symbol(grid_row, grid_col, 'O')  # Draw 'O' on the large grid
        
        # Check for draw in small grid
        if self.check_draw(grid_row, grid_col):
            self.grid_status[grid_row][grid_col] = 'D'
            self.draw_large_symbol(grid_row, grid_col, 'D')

        # Check if the game is over
        if self.check_large_grid_winner('O'):
            messagebox.showinfo("Game Over", "AI (O) wins!")
            self.reset_game()
            return

        # Switch back to the player
        self.last_move = (row, col)
        self.current_player = 'X'
        self.update_highlight()

    def check_small_grid_winner(self, grid_row, grid_col, player):
        grid = self.board[grid_row][grid_col]
        for i in range(3):
            if all(grid[i][j] == player for j in range(3)) or \
               all(grid[j][i] == player for j in range(3)):
                return True
        if all(grid[i][i] == player for i in range(3)) or \
           all(grid[i][2 - i] == player for i in range(3)):
            return True
        return False

    def check_large_grid_winner(self, player):
        for i in range(3):
            if all(self.grid_status[i][j] == player for j in range(3)) or \
               all(self.grid_status[j][i] == player for j in range(3)):
                return True
        if all(self.grid_status[i][i] == player for i in range(3)) or \
           all(self.grid_status[i][2 - i] == player for i in range(3)):
            return True
        return False

    def check_draw(self, grid_row, grid_col):
        # Check if the grid is full and no winner
        grid = self.board[grid_row][grid_col]
        return all(grid[i][j] != ' ' for i in range(3) for j in range(3)) and not self.check_small_grid_winner(grid_row, grid_col, 'X') and not self.check_small_grid_winner(grid_row, grid_col, 'O')

    def minimax(self, board, depth, alpha, beta, maximizing_player, last_move):
        # Evaluate the board
        if depth == 0 or self.check_large_grid_winner('X') or self.check_large_grid_winner('O'):
            return self.evaluate_board(board), last_move

        valid_moves = self.get_valid_moves(last_move)
        best_move = None

        if maximizing_player:
            max_eval = -math.inf
            for move in valid_moves:
                self.simulate_move(board, move, 'O')
                eval = self.minimax(board, depth - 1, alpha, beta, False, move)[0]
                self.undo_move(board, move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in valid_moves:
                self.simulate_move(board, move, 'X')
                eval = self.minimax(board, depth - 1, alpha, beta, True, move)[0]
                self.undo_move(board, move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def simulate_move(self, board, move, player):
        gr, gc, r, c = move
        board[gr][gc][r][c] = player

    def undo_move(self, board, move):
        gr, gc, r, c = move
        board[gr][gc][r][c] = ' '

    def get_valid_moves(self, last_move):
        valid_moves = []
        if last_move:
            next_gr, next_gc = last_move[0] % 3, last_move[1] % 3
            if self.grid_status[next_gr][next_gc] is None:
                for r in range(3):
                    for c in range(3):
                        if self.board[next_gr][next_gc][r][c] == ' ':
                            valid_moves.append((next_gr, next_gc, r, c))
        if not valid_moves:  # If the target grid is closed, play anywhere
            for gr in range(3):
                for gc in range(3):
                    if self.grid_status[gr][gc] is None:
                        for r in range(3):
                            for c in range(3):
                                if self.board[gr][gc][r][c] == ' ':
                                    valid_moves.append((gr, gc, r, c))
        return valid_moves

    def evaluate_board(self, board):
        score = 0
        # Check if AI (O) can win or block
        for gr in range(3):
            for gc in range(3):
                if self.grid_status[gr][gc] is None:
                    # Check for AI's winning move
                    if self.check_small_grid_winner(gr, gc, 'O'):
                        score += 10
                    # Check for Player's (X) winning move
                    elif self.check_small_grid_winner(gr, gc, 'X'):
                        score -= 10
        return score

    def reset_game(self):
        # Reset the game state variables
        self.board = [[[[ ' ' for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.grid_status = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.last_move = None

        # Recreate the buttons
        self.buttons = [[[[None for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        
        # Recreate the frames and buttons
        for grid_row in range(3):
            for grid_col in range(3):
                frame = tk.Frame(self.master, width=200, height=200, borderwidth=2, relief="solid", bg="white")
                frame.grid(row=grid_row, column=grid_col, padx=2, pady=2)
                self.frames[grid_row][grid_col] = frame

                for row in range(3):
                    for col in range(3):
                        btn = tk.Button(frame, text=' ', font=('Arial', 16), width=5, height=2,
                                        bg="#fffacd", activebackground="#ada988",
                                        command=lambda gr=grid_row, gc=grid_col, r=row, c=col: self.make_move(gr, gc, r, c))
                        btn.grid(row=row, column=col, padx=1, pady=1)
                        self.buttons[grid_row][grid_col][row][col] = btn

        self.update_highlight()  # Ensure highlight is reset

if __name__ == "__main__":
    root = tk.Tk()
    game = MetaTicTacToe(root)
    root.mainloop()