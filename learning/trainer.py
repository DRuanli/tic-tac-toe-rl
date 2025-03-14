import time
import pygame
import csv
import random
import numpy as np
from learning.environment import Environment

class Trainer:
    """Manages the training process for the tic-tac-toe agents."""
    
    def __init__(self, game, agent_x, agent_o, renderer=None, stats_display=None):
        """Initialize the trainer.
        
        Args:
            game (TicTacToe): The game instance
            agent_x (Agent): Agent playing as X
            agent_o (Agent): Agent playing as O
            renderer (GameRenderer, optional): Game renderer for visualization
            stats_display (StatsDisplay, optional): Stats display for visualization
        """
        self.game = game
        self.environment = Environment(game)
        self.agent_x = agent_x
        self.agent_o = agent_o
        self.renderer = renderer
        self.stats_display = stats_display
        
        # Statistics
        self.stats = {
            'episode': [],
            'x_wins': [],
            'o_wins': [],
            'draws': [],
            'game_lengths': [],
            'x_epsilon': [],
            'o_epsilon': []
        }
        self.running_x_wins = 0
        self.running_o_wins = 0
        self.running_draws = 0
    
    def train(self, num_episodes, display_interval=100):
        """Train agents through self-play.
        
        Args:
            num_episodes (int): Number of episodes to train
            display_interval (int): Interval for visualization and stats
        """
        print(f"Starting training for {num_episodes} episodes...")
        
        for episode in range(1, num_episodes + 1):
            # Track episode start time
            start_time = time.time()
            
            # Reset the environment
            state = self.environment.reset()
            
            # Game step counter
            steps = 0
            
            # Remember states and actions for delayed learning
            x_states = []
            x_actions = []
            o_states = []
            o_actions = []
            
            # Play the game
            done = False
            while not done:
                # Current player acts
                current_player = state['current_player']
                agent = self.agent_x if current_player == 'X' else self.agent_o
                
                # Choose action
                action = agent.choose_action(state)
                
                # Remember state and action
                if current_player == 'X':
                    x_states.append(state.copy())
                    x_actions.append(action)
                else:
                    o_states.append(state.copy())
                    o_actions.append(action)
                
                # Take action
                next_state, reward, done = self.environment.step(action, current_player)
                
                # Increment step counter
                steps += 1
                
                # Update state
                state = next_state
                
                # Visualization for certain episodes
                if episode % display_interval == 0 and self.renderer:
                    # Process any Pygame events
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                    
                    # Render the game
                    self.renderer.render(self.game)
                    
                    # Add a small delay to make the visualization visible
                    pygame.time.delay(100)
            
            # Game over - determine outcome
            if self.game.winner == 'X':
                self.running_x_wins += 1
                x_reward = 1.0
                o_reward = -1.0
            elif self.game.winner == 'O':
                self.running_o_wins += 1
                x_reward = -1.0
                o_reward = 1.0
            else:  # Draw
                self.running_draws += 1
                x_reward = 0.5
                o_reward = 0.5
            
            # Learning for X
            for i in range(len(x_states)):
                state_i = x_states[i]
                action_i = x_actions[i]
                
                # Terminal state for the last action, intermediate for others
                if i == len(x_states) - 1:
                    next_state_i = self.game.get_state()
                    reward_i = x_reward
                else:
                    next_state_i = o_states[i]
                    reward_i = 0  # Intermediate steps have zero reward
                
                self.agent_x.learn(state_i, action_i, reward_i, next_state_i)
            
            # Learning for O
            for i in range(len(o_states)):
                state_i = o_states[i]
                action_i = o_actions[i]
                
                # Terminal state for the last action, intermediate for others
                if i == len(o_states) - 1:
                    next_state_i = self.game.get_state()
                    reward_i = o_reward
                else:
                    next_state_i = x_states[i+1]
                    reward_i = 0  # Intermediate steps have zero reward
                
                self.agent_o.learn(state_i, action_i, reward_i, next_state_i)
            
            # Increment episode counters
            self.agent_x.increment_episode()
            self.agent_o.increment_episode()
            
            # Record statistics periodically
            if episode % 100 == 0:
                self.stats['episode'].append(episode)
                self.stats['x_wins'].append(self.running_x_wins)
                self.stats['o_wins'].append(self.running_o_wins)
                self.stats['draws'].append(self.running_draws)
                self.stats['game_lengths'].append(steps)
                self.stats['x_epsilon'].append(self.agent_x.epsilon)
                self.stats['o_epsilon'].append(self.agent_o.epsilon)
                
                # Reset running counters
                self.running_x_wins = 0
                self.running_o_wins = 0
                self.running_draws = 0
                
                # Display progress and statistics
                end_time = time.time()
                elapsed = end_time - start_time
                print(f"Episode {episode}/{num_episodes} ({episode/num_episodes*100:.1f}%) - " +
                      f"X: {self.stats['x_wins'][-1]}, O: {self.stats['o_wins'][-1]}, " +
                      f"Draw: {self.stats['draws'][-1]}, Steps: {steps}, " +
                      f"X ε: {self.agent_x.epsilon:.3f}, O ε: {self.agent_o.epsilon:.3f}, " +
                      f"Time: {elapsed:.3f}s")
                
                # Update stats display
                if self.stats_display:
                    self.stats_display.update(self.stats)
                    self.stats_display.render()
                    pygame.display.flip()
    
    def play_demo_game(self, delay=500):
        """Play a demonstration game between the trained agents.
        
        Args:
            delay (int): Delay between moves in milliseconds for visualization
        """
        if not self.renderer:
            print("Renderer is required for demo game")
            return
        
        print("Playing demo game...")
        
        # Reset the environment
        state = self.environment.reset()
        
        # Render initial state
        self.renderer.render(self.game)
        pygame.display.flip()
        pygame.time.delay(delay)
        
        # Play the game
        done = False
        while not done:
            # Process any Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            # Current player acts
            current_player = state['current_player']
            agent = self.agent_x if current_player == 'X' else self.agent_o
            
            # Choose action (always exploit during demo)
            # Save and restore epsilon to ensure exploitation
            original_epsilon = agent.epsilon
            agent.epsilon = 0
            action = agent.choose_action(state)
            agent.epsilon = original_epsilon
            
            # Take action
            next_state, reward, done = self.environment.step(action, current_player)
            
            # Update state
            state = next_state
            
            # Render
            self.renderer.render(self.game)
            pygame.display.flip()
            pygame.time.delay(delay)
        
        # Display final result
        if self.game.winner:
            print(f"Game over! {self.game.winner} wins!")
        else:
            print("Game over! It's a draw!")
        
        # Keep rendering the final state for a while
        pygame.time.delay(delay * 2)
    
    def save_stats(self, filepath):
        """Save training statistics to a CSV file.
        
        Args:
            filepath (str): Path to save the file
        """
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Episode', 'X Wins', 'O Wins', 'Draws', 'Game Length', 'X Epsilon', 'O Epsilon'])
            for i in range(len(self.stats['episode'])):
                writer.writerow([
                    self.stats['episode'][i],
                    self.stats['x_wins'][i],
                    self.stats['o_wins'][i],
                    self.stats['draws'][i],
                    self.stats['game_lengths'][i],
                    self.stats['x_epsilon'][i],
                    self.stats['o_epsilon'][i]
                ])
        
        print(f"Statistics saved to {filepath}")