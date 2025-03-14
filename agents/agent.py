from abc import ABC, abstractmethod

class Agent(ABC):
    """Abstract base class for tic-tac-toe playing agents."""
    
    def __init__(self, player_symbol):
        """Initialize the agent.
        
        Args:
            player_symbol (str): 'X' or 'O'
        """
        self.player_symbol = player_symbol
    
    @abstractmethod
    def choose_action(self, state):
        """Choose an action based on the current state.
        
        Args:
            state (dict): Current game state
            
        Returns:
            tuple: (row, col) position to play
        """
        pass
    
    @abstractmethod
    def learn(self, state, action, reward, next_state):
        """Update the agent's knowledge based on experience.
        
        Args:
            state (dict): State before action
            action (tuple): (row, col) position played
            reward (float): Reward received
            next_state (dict): State after action
        """
        pass
    
    @abstractmethod
    def save(self, filepath):
        """Save the agent's knowledge to a file.
        
        Args:
            filepath (str): Path to save the file
        """
        pass
    
    @abstractmethod
    def load(self, filepath):
        """Load the agent's knowledge from a file.
        
        Args:
            filepath (str): Path to the file
        """
        pass