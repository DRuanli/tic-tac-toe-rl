import random
import pickle
import numpy as np
from agents.agent import Agent

class QLearningAgent(Agent):
    """Q-learning agent for tic-tac-toe."""
    
    def __init__(self, player_symbol, learning_rate=0.1, discount_factor=0.9, 
                 epsilon_start=1.0, epsilon_end=0.1, epsilon_decay=0.9995):
        """Initialize the Q-learning agent.
        
        Args:
            player_symbol (str): 'X' or 'O'
            learning_rate (float): Alpha - learning rate
            discount_factor (float): Gamma - future reward discount factor
            epsilon_start (float): Initial exploration rate
            epsilon_end (float): Final exploration rate
            epsilon_decay (float): Rate of exploration decay
        """
        super().__init__(player_symbol)
        self.q_table = {}  # State-action values
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.episode_count = 0
    
    def get_q_value(self, state_key, action):
        """Get Q-value for a state-action pair.
        
        Args:
            state_key (str): State representation
            action (tuple): (row, col) position
            
        Returns:
            float: Q-value
        """
        # If state not in Q-table, initialize it with zeros for all actions
        if state_key not in self.q_table:
            # Initialize Q-values for all possible actions in this state
            self.q_table[state_key] = {}
        
        # If action not in state's actions, initialize to 0
        row, col = action
        action_key = f"{row},{col}"
        if action_key not in self.q_table[state_key]:
            self.q_table[state_key][action_key] = 0.0
            
        return self.q_table[state_key][action_key]
    
    def choose_action(self, state):
        """Choose an action using epsilon-greedy policy.
        
        Args:
            state (dict): Current game state
            
        Returns:
            tuple: (row, col) position to play
        """
        valid_moves = state['valid_moves']
        if not valid_moves:
            raise ValueError("No valid moves available")
        
        # Exploration: random move
        if random.random() < self.epsilon:
            return random.choice(valid_moves)
        
        # Exploitation: best known move
        state_key = state['board'].get_state_key()
        q_values = [self.get_q_value(state_key, move) for move in valid_moves]
        
        # Find indices of moves with the highest Q-value
        max_q = max(q_values)
        best_indices = [i for i, q in enumerate(q_values) if q == max_q]
        
        # Randomly select among the best moves
        best_idx = random.choice(best_indices)
        return valid_moves[best_idx]
    
    def learn(self, state, action, reward, next_state):
        """Update Q-values based on experience.
        
        Args:
            state (dict): State before action
            action (tuple): (row, col) position played
            reward (float): Reward received
            next_state (dict): State after action
        """
        state_key = state['board'].get_state_key()
        row, col = action
        action_key = f"{row},{col}"
        
        # Get current Q-value
        current_q = self.get_q_value(state_key, action)
        
        # Calculate max Q-value for next state
        next_state_key = next_state['board'].get_state_key()
        next_valid_moves = next_state['valid_moves']
        
        if next_valid_moves and not next_state['is_terminal']:
            next_q_values = [self.get_q_value(next_state_key, move) for move in next_valid_moves]
            max_next_q = max(next_q_values) if next_q_values else 0.0
        else:
            max_next_q = 0.0
        
        # Q-learning update
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        
        # Update Q-table
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        self.q_table[state_key][action_key] = new_q
        
        # Decay exploration rate
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)
    
    def save(self, filepath):
        """Save the Q-table to a file.
        
        Args:
            filepath (str): Path to save the file
        """
        with open(filepath, 'wb') as f:
            pickle.dump({
                'q_table': self.q_table,
                'epsilon': self.epsilon,
                'episode_count': self.episode_count
            }, f)
    
    def load(self, filepath):
        """Load the Q-table from a file.
        
        Args:
            filepath (str): Path to the file
        """
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.q_table = data['q_table']
                self.epsilon = data['epsilon']
                self.episode_count = data['episode_count']
            print(f"Loaded agent {self.player_symbol} with {len(self.q_table)} states")
        except (FileNotFoundError, KeyError):
            print(f"No saved model found for agent {self.player_symbol} or invalid format")
            
    def increment_episode(self):
        """Increment the episode counter."""
        self.episode_count += 1