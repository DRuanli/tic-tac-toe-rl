class Environment:
    """Reinforcement learning environment for tic-tac-toe."""
    
    def __init__(self, game):
        """Initialize the environment.
        
        Args:
            game (TicTacToe): The game instance
        """
        self.game = game
    
    def reset(self):
        """Reset the environment.
        
        Returns:
            dict: Initial state
        """
        return self.game.reset()
    
    def step(self, action, player):
        """Take an action in the environment.
        
        Args:
            action (tuple): (row, col) position to play
            player (str): 'X' or 'O'
            
        Returns:
            tuple: (next_state, reward, done)
        """
        # Store the state before the action
        state_before = self.game.get_state()
        
        # Check if it's the correct player's turn
        if self.game.current_player != player:
            raise ValueError(f"It's {self.game.current_player}'s turn, not {player}'s")
        
        # Make the move
        try:
            next_state = self.game.make_move(action[0], action[1])
        except ValueError as e:
            # Invalid move
            return state_before, -1.0, False
        
        # Check if game is over
        done = self.game.is_terminal()
        
        # Calculate reward
        reward = self.game.get_reward(player)
        
        return next_state, reward, done