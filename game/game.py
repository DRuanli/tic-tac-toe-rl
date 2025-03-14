from game.board import Board

class TicTacToe:
    """The game of Tic-Tac-Toe."""
    
    def __init__(self, board_size=3):
        """Initialize the game.
        
        Args:
            board_size (int): Size of the board (default is 3x3)
        """
        self.board = Board(board_size)
        self.current_player = 'X'  # X goes first
        self.winner = None
        self.is_draw = False
        self.move_history = []
    
    def reset(self):
        """Reset the game to initial state."""
        self.board.reset()
        self.current_player = 'X'
        self.winner = None
        self.is_draw = False
        self.move_history = []
        return self.get_state()
    
    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def get_state(self):
        """Get the current game state.
        
        Returns:
            dict: Game state information
        """
        return {
            'board': self.board,
            'current_player': self.current_player,
            'valid_moves': self.board.get_valid_moves(),
            'is_terminal': self.is_terminal(),
            'winner': self.winner,
            'is_draw': self.is_draw
        }
    
    def make_move(self, row, col):
        """Make a move at the specified position.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            dict: Updated game state
            
        Raises:
            ValueError: If the move is invalid
        """
        if self.is_terminal():
            raise ValueError("Game is already over")
        
        if not self.board.make_move(row, col, self.current_player):
            raise ValueError("Invalid move")
        
        # Record move
        self.move_history.append((row, col, self.current_player))
        
        # Check for winner
        winner = self.board.check_winner()
        if winner != ' ':
            self.winner = winner
        elif self.board.is_full():
            self.is_draw = True
        else:
            self.switch_player()
        
        return self.get_state()
    
    def is_terminal(self):
        """Check if the game is over.
        
        Returns:
            bool: True if game is over, False otherwise
        """
        return self.winner is not None or self.is_draw
    
    def get_winner(self):
        """Get the winner of the game.
        
        Returns:
            str: 'X' or 'O' if there's a winner, None if no winner or game not over
        """
        return self.winner
    
    def get_reward(self, player):
        """Get the reward for a player based on the game outcome.
        
        Args:
            player (str): 'X' or 'O'
            
        Returns:
            float: Reward value (1 for win, -1 for loss, 0 for draw or ongoing)
        """
        if not self.is_terminal():
            return 0
        
        if self.is_draw:
            return 0.5  # Small positive reward for a draw
        
        if self.winner == player:
            return 1.0  # Win
        else:
            return -1.0  # Loss