class Board:
    """Represents a tic-tac-toe board."""
    
    def __init__(self, size=3):
        """Initialize an empty board.
        
        Args:
            size (int): Size of the board (default is 3x3)
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
        """Check if there is a winner.
        
        Returns:
            str: 'X' or 'O' if there's a winner, ' ' if no winner yet
        """
        # Check rows
        for row in range(self.size):
            if self.grid[row][0] != ' ' and all(self.grid[row][0] == self.grid[row][c] for c in range(self.size)):
                return self.grid[row][0]
        
        # Check columns
        for col in range(self.size):
            if self.grid[0][col] != ' ' and all(self.grid[r][col] == self.grid[0][col] for r in range(self.size)):
                return self.grid[0][col]
        
        # Check main diagonal
        if self.grid[0][0] != ' ' and all(self.grid[i][i] == self.grid[0][0] for i in range(self.size)):
            return self.grid[0][0]
        
        # Check other diagonal
        if self.grid[0][self.size-1] != ' ' and all(self.grid[i][self.size-1-i] == self.grid[0][self.size-1] for i in range(self.size)):
            return self.grid[0][self.size-1]
        
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