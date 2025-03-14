import pygame
import numpy as np

class StatsDisplay:
    """Displays statistics about the training process."""
    
    def __init__(self, screen):
        """Initialize the stats display.
        
        Args:
            screen (pygame.Surface): Pygame screen surface
        """
        self.screen = screen
        self.width, self.height = screen.get_size()
        
        # Stats area position and size
        self.stats_area_pos = (400, 50)
        self.stats_area_size = (self.width - 420, self.height - 100)
        
        # Colors
        self.bg_color = (240, 240, 240)
        self.text_color = (20, 20, 20)
        self.x_color = (220, 50, 50)
        self.o_color = (50, 50, 220)
        self.draw_color = (50, 50, 50)
        self.line_color = (200, 200, 200)
        
        # Font
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 16)
        self.title_font = pygame.font.SysFont('Arial', 20)
        
        # Stats data
        self.stats = None
    
    def update(self, stats):
        """Update the statistics data.
        
        Args:
            stats (dict): Training statistics
        """
        self.stats = stats
    
    def render(self):
        """Render the statistics display."""
        if not self.stats or not self.stats['episode']:
            # No data to display yet
            return
        
        # Draw stats area background
        stats_rect = pygame.Rect(
            self.stats_area_pos[0], self.stats_area_pos[1],
            self.stats_area_size[0], self.stats_area_size[1]
        )
        pygame.draw.rect(self.screen, (255, 255, 255), stats_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), stats_rect, 1)
        
        # Draw title
        title = self.title_font.render("Training Statistics", True, self.text_color)
        self.screen.blit(title, (self.stats_area_pos[0] + 10, self.stats_area_pos[1] + 10))
        
        # Draw win rate graph
        self._draw_win_rate_graph()
        
        # Draw epsilon graph
        self._draw_epsilon_graph()
        
        # Draw latest statistics
        self._draw_latest_stats()
    
    def _draw_win_rate_graph(self):
        """Draw a graph of win rates over time."""
        graph_rect = pygame.Rect(
            self.stats_area_pos[0] + 10, self.stats_area_pos[1] + 40,
            self.stats_area_size[0] - 20, 150
        )
        
        # Draw graph background and border
        pygame.draw.rect(self.screen, (248, 248, 248), graph_rect)
        pygame.draw.rect(self.screen, self.line_color, graph_rect, 1)
        
        # Draw title
        title = self.font.render("Win Rates (last 100 games)", True, self.text_color)
        self.screen.blit(title, (graph_rect.left, graph_rect.top - 20))
        
        # Get data
        episodes = self.stats['episode']
        x_wins = self.stats['x_wins']
        o_wins = self.stats['o_wins']
        draws = self.stats['draws']
        
        if not episodes:
            return
        
        # Calculate total games and percentages
        total_games = 100  # Each data point represents 100 games
        x_percentages = [x / total_games * 100 for x in x_wins]
        o_percentages = [o / total_games * 100 for o in o_wins]
        draw_percentages = [d / total_games * 100 for d in draws]
        
        # Draw grid lines
        for i in range(0, 101, 20):
            y = graph_rect.bottom - (i / 100 * graph_rect.height)
            pygame.draw.line(
                self.screen, self.line_color,
                (graph_rect.left, y), (graph_rect.right, y),
                1
            )
            
            # Draw y-axis labels
            label = self.font.render(f"{i}%", True, self.text_color)
            self.screen.blit(label, (graph_rect.left - 30, y - 8))
        
        # Draw data points and lines
        self._draw_line(graph_rect, episodes, x_percentages, self.x_color)
        self._draw_line(graph_rect, episodes, o_percentages, self.o_color)
        self._draw_line(graph_rect, episodes, draw_percentages, self.draw_color)
        
        # Draw legend
        legend_x = graph_rect.left
        legend_y = graph_rect.bottom + 10
        
        # X wins
        pygame.draw.line(self.screen, self.x_color, (legend_x, legend_y + 6), (legend_x + 20, legend_y + 6), 3)
        x_label = self.font.render("X Wins", True, self.x_color)
        self.screen.blit(x_label, (legend_x + 25, legend_y))
        
        # O wins
        legend_x += 100
        pygame.draw.line(self.screen, self.o_color, (legend_x, legend_y + 6), (legend_x + 20, legend_y + 6), 3)
        o_label = self.font.render("O Wins", True, self.o_color)
        self.screen.blit(o_label, (legend_x + 25, legend_y))
        
        # Draws
        legend_x += 100
        pygame.draw.line(self.screen, self.draw_color, (legend_x, legend_y + 6), (legend_x + 20, legend_y + 6), 3)
        draw_label = self.font.render("Draws", True, self.draw_color)
        self.screen.blit(draw_label, (legend_x + 25, legend_y))
    
    def _draw_epsilon_graph(self):
        """Draw a graph of exploration rates over time."""
        graph_rect = pygame.Rect(
            self.stats_area_pos[0] + 10, self.stats_area_pos[1] + 230,
            self.stats_area_size[0] - 20, 120
        )
        
        # Draw graph background and border
        pygame.draw.rect(self.screen, (248, 248, 248), graph_rect)
        pygame.draw.rect(self.screen, self.line_color, graph_rect, 1)
        
        # Draw title
        title = self.font.render("Exploration Rate (ε)", True, self.text_color)
        self.screen.blit(title, (graph_rect.left, graph_rect.top - 20))
        
        # Get data
        episodes = self.stats['episode']
        x_epsilons = self.stats['x_epsilon']
        o_epsilons = self.stats['o_epsilon']
        
        if not episodes:
            return
        
        # Draw grid lines
        for i in range(0, 101, 20):
            y = graph_rect.bottom - (i / 100 * graph_rect.height)
            pygame.draw.line(
                self.screen, self.line_color,
                (graph_rect.left, y), (graph_rect.right, y),
                1
            )
            
            # Draw y-axis labels
            label = self.font.render(f"{i/100:.1f}", True, self.text_color)
            self.screen.blit(label, (graph_rect.left - 30, y - 8))
        
        # Draw data points and lines
        self._draw_line(graph_rect, episodes, [e * 100 for e in x_epsilons], self.x_color)
        self._draw_line(graph_rect, episodes, [e * 100 for e in o_epsilons], self.o_color)
        
        # Draw legend
        legend_x = graph_rect.left
        legend_y = graph_rect.bottom + 10
        
        # X epsilon
        pygame.draw.line(self.screen, self.x_color, (legend_x, legend_y + 6), (legend_x + 20, legend_y + 6), 3)
        x_label = self.font.render("X ε", True, self.x_color)
        self.screen.blit(x_label, (legend_x + 25, legend_y))
        
        # O epsilon
        legend_x += 100
        pygame.draw.line(self.screen, self.o_color, (legend_x, legend_y + 6), (legend_x + 20, legend_y + 6), 3)
        o_label = self.font.render("O ε", True, self.o_color)
        self.screen.blit(o_label, (legend_x + 25, legend_y))
    
    def _draw_line(self, rect, x_values, y_values, color):
        """Draw a line graph.
        
        Args:
            rect (pygame.Rect): Graph area rectangle
            x_values (list): X-axis values
            y_values (list): Y-axis values
            color (tuple): RGB color
        """
        if not x_values or not y_values:
            return
        
        # Scale x_values to fit in the graph
        x_min = min(x_values)
        x_max = max(x_values)
        x_range = max(1, x_max - x_min)
        
        # Convert data points to screen coordinates
        points = []
        for i in range(len(x_values)):
            x = rect.left + (x_values[i] - x_min) / x_range * rect.width
            y = rect.bottom - (y_values[i] / 100 * rect.height)
            points.append((x, y))
        
        # Draw lines between points
        if len(points) > 1:
            pygame.draw.lines(self.screen, color, False, points, 2)
        
        # Draw points
        for point in points:
            pygame.draw.circle(self.screen, color, point, 3)
    
    def _draw_latest_stats(self):
        """Draw the latest statistics values."""
        if not self.stats['episode']:
            return
        
        stats_x = self.stats_area_pos[0] + 10
        stats_y = self.stats_area_pos[1] + 380
        
        # Get the latest statistics
        latest_idx = -1
        latest_episode = self.stats['episode'][latest_idx]
        latest_x_wins = self.stats['x_wins'][latest_idx]
        latest_o_wins = self.stats['o_wins'][latest_idx]
        latest_draws = self.stats['draws'][latest_idx]
        latest_game_length = self.stats['game_lengths'][latest_idx]
        
        # Draw statistics
        title = self.title_font.render(f"Latest Stats (Episode {latest_episode})", True, self.text_color)
        self.screen.blit(title, (stats_x, stats_y))
        
        stats_y += 30
        x_text = self.font.render(f"X Wins: {latest_x_wins}/100 ({latest_x_wins}%)", True, self.x_color)
        self.screen.blit(x_text, (stats_x, stats_y))
        
        stats_y += 20
        o_text = self.font.render(f"O Wins: {latest_o_wins}/100 ({latest_o_wins}%)", True, self.o_color)
        self.screen.blit(o_text, (stats_x, stats_y))
        
        stats_y += 20
        draw_text = self.font.render(f"Draws: {latest_draws}/100 ({latest_draws}%)", True, self.draw_color)
        self.screen.blit(draw_text, (stats_x, stats_y))
        
        stats_y += 20
        length_text = self.font.render(f"Avg. Game Length: {latest_game_length:.1f} moves", True, self.text_color)
        self.screen.blit(length_text, (stats_x, stats_y))