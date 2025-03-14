import random
from collections import deque

class ExperienceBuffer:
    """Buffer to store and sample experiences for reinforcement learning."""
    
    def __init__(self, max_size=10000):
        """Initialize the experience buffer.
        
        Args:
            max_size (int): Maximum number of experiences to store
        """
        self.buffer = deque(maxlen=max_size)
    
    def add(self, state, action, reward, next_state):
        """Add an experience to the buffer.
        
        Args:
            state (dict): State before action
            action (tuple): (row, col) position played
            reward (float): Reward received
            next_state (dict): State after action
        """
        # Create a shallow copy of relevant state information
        state_copy = {
            'board_state': state['board'].get_state_key(),
            'current_player': state['current_player'],
            'valid_moves': state['valid_moves'].copy() if state['valid_moves'] else []
        }
        
        next_state_copy = {
            'board_state': next_state['board'].get_state_key(),
            'current_player': next_state['current_player'],
            'valid_moves': next_state['valid_moves'].copy() if next_state['valid_moves'] else [],
            'is_terminal': next_state['is_terminal']
        }
        
        self.buffer.append((state_copy, action, reward, next_state_copy))
    
    def sample(self, batch_size):
        """Sample a batch of experiences from the buffer.
        
        Args:
            batch_size (int): Number of experiences to sample
            
        Returns:
            list: List of (state, action, reward, next_state) tuples
        """
        return random.sample(self.buffer, min(batch_size, len(self.buffer)))
    
    def __len__(self):
        """Get the current size of the buffer."""
        return len(self.buffer)