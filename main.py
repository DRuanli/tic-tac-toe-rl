import pygame
import os
import argparse
from game.game import TicTacToe
from agents.q_learning_agent import QLearningAgent
from learning.trainer import Trainer
from ui.renderer import GameRenderer
from ui.stats_display import StatsDisplay

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Tic-Tac-Toe Reinforcement Learning')
    parser.add_argument('--episodes', type=int, default=100, help='Number of training episodes')
    parser.add_argument('--display_interval', type=int, default=100, help='Display game every N episodes')
    parser.add_argument('--learning_rate', type=float, default=0.1, help='Learning rate for Q-learning')
    parser.add_argument('--discount_factor', type=float, default=0.9, help='Discount factor for Q-learning')
    parser.add_argument('--epsilon_start', type=float, default=1.0, help='Starting exploration rate')
    parser.add_argument('--epsilon_end', type=float, default=0.1, help='Ending exploration rate')
    parser.add_argument('--epsilon_decay', type=float, default=0.9995, help='Exploration rate decay')
    parser.add_argument('--headless', action='store_true', help='Run without visualization')
    parser.add_argument('--demo_delay', type=int, default=100, 
                    help='Delay between moves in demo game (ms)')
    args = parser.parse_args()
    
    # Create data directories if they don't exist
    os.makedirs('data/models', exist_ok=True)
    os.makedirs('data/stats', exist_ok=True)

    # Initialize pygame
    if not args.headless:
        pygame.init()
        screen = pygame.display.set_mode((1000, 700))  # Larger window for 50x50 board
        pygame.display.set_caption("Gomoku RL (50x50 with 5-in-a-row)")
        game_renderer = GameRenderer(screen)
        stats_display = StatsDisplay(screen)
    else:
        game_renderer = None
        stats_display = None

    # Create game and agents
    game = TicTacToe()
    
    agent_x = QLearningAgent('X', 
                             learning_rate=args.learning_rate,
                             discount_factor=args.discount_factor,
                             epsilon_start=args.epsilon_start,
                             epsilon_end=args.epsilon_end,
                             epsilon_decay=args.epsilon_decay)
    
    agent_o = QLearningAgent('O', 
                             learning_rate=args.learning_rate,
                             discount_factor=args.discount_factor,
                             epsilon_start=args.epsilon_start,
                             epsilon_end=args.epsilon_end,
                             epsilon_decay=args.epsilon_decay)
    
    # Load models if they exist
    if os.path.exists('data/models/agent_x.pkl'):
        agent_x.load('data/models/agent_x.pkl')
    if os.path.exists('data/models/agent_o.pkl'):
        agent_o.load('data/models/agent_o.pkl')
    
    # Create trainer
    trainer = Trainer(game, agent_x, agent_o, game_renderer, stats_display)
    
    # Run training
    trainer.train(args.episodes, args.display_interval)
    
    # Save trained models
    agent_x.save('data/models/agent_x.pkl')
    agent_o.save('data/models/agent_o.pkl')
    
    # Save statistics
    trainer.save_stats('data/stats/training_stats.csv')
    
    # Play a final demo game with visualization
    if not args.headless:
        print("Training completed. Playing a demo game...")
        trainer.play_demo_game()
        
        # Keep the window open until user closes
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
        pygame.quit()

if __name__ == "__main__":
    main()