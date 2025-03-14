class Board:
    """Represents a tic-tac-toe board."""
    
    def __init__(self, size=50):
        """Initialize an empty board.
        
        Args:
            size (int): Size of the board (default is 50x50)
        """
        self.size = size
        self.reset()
    
    def reset(self):
        """Reset the board to empty state."""
        self.grid = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        
    def make_move(self, row, col, player):
        """Place a player's mark on the board.
        
        Args:
            row (int): Row index
            col (int): Column index
            player (str): Player symbol ('X' or 'O')
            
        Returns:
            bool: True if move was valid and made, False otherwise
        """
        if 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] == ' ':
            self.grid[row][col] = player
            return True
        return False
    
    def get_valid_moves(self):
        """Get all valid move positions on the board.
        
        Returns:
            list: List of (row, col) tuples for all empty spaces
        """
        valid_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == ' ':
                    valid_moves.append((row, col))
        return valid_moves
    
    def check_winner(self):
        """Check if there is a winner (5 in a row).
        
        Returns:
            str: 'X' or 'O' if there's a winner, ' ' if no winner yet
        """
        consecutive_to_win = 5
        
        # Check rows
        for row in range(self.size):
            for col in range(self.size - consecutive_to_win + 1):
                if self.grid[row][col] != ' ':
                    if all(self.grid[row][col] == self.grid[row][col+i] for i in range(consecutive_to_win)):
                        return self.grid[row][col]
        
        # Check columns
        for col in range(self.size):
            for row in range(self.size - consecutive_to_win + 1):
                if self.grid[row][col] != ' ':
                    if all(self.grid[row+i][col] == self.grid[row][col] for i in range(consecutive_to_win)):
                        return self.grid[row][col]
        
        # Check diagonals (top-left to bottom-right)
        for row in range(self.size - consecutive_to_win + 1):
            for col in range(self.size - consecutive_to_win + 1):
                if self.grid[row][col] != ' ':
                    if all(self.grid[row+i][col+i] == self.grid[row][col] for i in range(consecutive_to_win)):
                        return self.grid[row][col]
        
        # Check diagonals (top-right to bottom-left)
        for row in range(self.size - consecutive_to_win + 1):
            for col in range(consecutive_to_win - 1, self.size):
                if self.grid[row][col] != ' ':
                    if all(self.grid[row+i][col-i] == self.grid[row][col] for i in range(consecutive_to_win)):
                        return self.grid[row][col]
        
        return ' '
    
    def is_full(self):
        """Check if the board is full.
        
        Returns:
            bool: True if no empty spaces left, False otherwise
        """
        return all(self.grid[r][c] != ' ' for r in range(self.size) for c in range(self.size))
    
    def get_state_key(self):
        """Get a string representation of the board state for Q-learning.
        
        Returns:
            str: String representation of the board
        """
        return ''.join(''.join(row) for row in self.grid)
    
    def __str__(self):
        """String representation of the board for printing."""
        rows = []
        for i in range(self.size):
            row = ' | '.join(self.grid[i])
            rows.append(row)
        
        divider = '-' * (4 * self.size - 1)
        return '\n'.join([rows[0]] + [divider + '\n' + row for row in rows[1:]])