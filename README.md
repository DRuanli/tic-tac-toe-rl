# Tic-Tac-Toe with Reinforcement Learning

This project implements a Tic-Tac-Toe game where two AI agents learn to play through reinforcement learning (specifically Q-learning).

## Features

- Standard 3×3 Tic-Tac-Toe game implementation
- Q-learning agents that improve over time
- Self-play training with configurable parameters
- Pygame visualization of gameplay and learning statistics
- Save/load functionality for trained agents

## Requirements

- Python 3.6+
- Pygame
- NumPy

Install dependencies with:

```bash
pip install pygame numpy
```

## Project Structure

```
tic-tac-toe-rl/
│
├── main.py                    # Entry point that runs the game and learning process
│
├── game/                      # Core game mechanics
│   ├── __init__.py
│   ├── board.py               # Board implementation
│   ├── game.py                # Game logic and rules
│
├── agents/                    # AI players
│   ├── __init__.py
│   ├── agent.py               # Base agent class
│   ├── q_learning_agent.py    # Q-learning implementation
│
├── learning/                  # Learning framework
│   ├── __init__.py
│   ├── environment.py         # RL environment
│   ├── trainer.py             # Self-play training
│   ├── experience.py          # Experience storage
│
├── ui/                        # User interface
│   ├── __init__.py
│   ├── renderer.py            # Game visualization
│   ├── stats_display.py       # Learning statistics visualization
│
└── data/                      # Saved data (created automatically)
    ├── models/                # Trained agent models
    └── stats/                 # Training statistics
```

## Usage

### Basic Training

```bash
python main.py
```

This will start training with default parameters and visualization.

### Custom Training

```bash
python main.py --episodes 5000 --display_interval 500 --learning_rate 0.2
```

### Available Options

- `--episodes`: Number of training episodes (default: 10000)
- `--display_interval`: Display game every N episodes (default: 100)
- `--learning_rate`: Learning rate for Q-learning (default: 0.1)
- `--discount_factor`: Discount factor for Q-learning (default: 0.9)
- `--epsilon_start`: Starting exploration rate (default: 1.0)
- `--epsilon_end`: Ending exploration rate (default: 0.1)
- `--epsilon_decay`: Exploration rate decay per episode (default: 0.9995)
- `--headless`: Run without visualization (for faster training)

## How It Works

### Q-Learning Algorithm

The agents use Q-learning, a reinforcement learning algorithm that learns the value of an action in a particular state. The key formula is:

Q(s,a) ← Q(s,a) + α[r + γ·max_a'Q(s',a') - Q(s,a)]

Where:
- Q(s,a) is the value of taking action a in state s
- α is the learning rate
- r is the reward received
- γ is the discount factor for future rewards
- s' is the new state after taking action a
- max_a'Q(s',a') is the best possible value from the new state

### Training Process

1. Agents play games against each other
2. After each move, the agent that made the move receives feedback
3. At the end of the game, rewards are given (win: +1, loss: -1, draw: +0.5)
4. Agents update their Q-tables based on received rewards
5. Over time, agents learn optimal play strategies

## License

MIT