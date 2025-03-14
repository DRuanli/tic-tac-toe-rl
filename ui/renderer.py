import pygame

class GameRenderer:
    """Renders the tic-tac-toe game using Pygame."""
    
    def __init__(self, screen):
        """Initialize the renderer.
        
        Args:
            screen (pygame.Surface): Pygame screen surface
        """
        self.screen = screen
        self.width, self.height = screen.get_size()
        
        # Board dimensions and position
        self.board_size = 500  # Larger display area for the 50x50 board
        self.cell_size = 10    # Smaller cells to fit the 50x50 grid
        self.board_pos = (50, 50)  # Position board closer to the left edge
        self.visible_cells = 50    # Number of cells to show in the viewport
        self.scroll_x = 0
        self.scroll_y = 0      # Track scroll position for large board
        
        # Colors
        self.bg_color = (240, 240, 240)
        self.line_color = (50, 50, 50)
        self.x_color = (220, 50, 50)
        self.o_color = (50, 50, 220)
        self.highlight_color = (50, 200, 50)
        self.text_color = (20, 20, 20)
        
        # Font
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)
        self.large_font = pygame.font.SysFont('Arial', 32)
    
    def render(self, game):
        """Render the game.
        
        Args:
            game (TicTacToe): The game instance
        """
        # Clear screen
        self.screen.fill(self.bg_color)
        
        # Draw board
        self._draw_board()
        
        # Draw X's and O's
        self._draw_symbols(game)
        
        # Draw game status
        self._draw_status(game)
        
        # Update the display
        pygame.display.flip()
    
    def _draw_board(self):
        """Draw the tic-tac-toe grid for a 50x50 board."""
        # Draw board background
        board_rect = pygame.Rect(
            self.board_pos[0], self.board_pos[1], 
            self.board_size, self.board_size
        )
        pygame.draw.rect(self.screen, (255, 255, 255), board_rect)
        
        # Draw grid lines (draw thinner lines for the 50x50 grid)
        for i in range(1, self.visible_cells):
            # Vertical lines
            pygame.draw.line(
                self.screen, self.line_color,
                (self.board_pos[0] + i * self.cell_size, self.board_pos[1]),
                (self.board_pos[0] + i * self.cell_size, self.board_pos[1] + self.board_size),
                1
            )
            
            # Horizontal lines
            pygame.draw.line(
                self.screen, self.line_color,
                (self.board_pos[0], self.board_pos[1] + i * self.cell_size),
                (self.board_pos[0] + self.board_size, self.board_pos[1] + i * self.cell_size),
                1
            )
    
    def _draw_symbols(self, game):
        """Draw X's and O's on the board.
        
        Args:
            game (TicTacToe): The game instance
        """
        for row in range(50):
            for col in range(50):
                cell_value = game.board.grid[row][col]
                if cell_value != ' ':
                    center_x = self.board_pos[0] + col * self.cell_size + self.cell_size // 2
                    center_y = self.board_pos[1] + row * self.cell_size + self.cell_size // 2
                    
                    if center_x >= self.board_pos[0] and center_x < self.board_pos[0] + self.board_size and \
                       center_y >= self.board_pos[1] and center_y < self.board_pos[1] + self.board_size:
                        if cell_value == 'X':
                            self._draw_x(center_x, center_y)
                        else:  # 'O'
                            self._draw_o(center_x, center_y)
    
    def _draw_x(self, center_x, center_y):
        """Draw an X symbol.
        
        Args:
            center_x (int): X coordinate of the center
            center_y (int): Y coordinate of the center
        """
        size = self.cell_size // 3
        pygame.draw.line(
            self.screen, self.x_color,
            (center_x - size, center_y - size),
            (center_x + size, center_y + size),
            2  # Thinner line for smaller cells
        )
        pygame.draw.line(
            self.screen, self.x_color,
            (center_x + size, center_y - size),
            (center_x - size, center_y + size),
            2  # Thinner line for smaller cells
        )
    
    def _draw_o(self, center_x, center_y):
        """Draw an O symbol.
        
        Args:
            center_x (int): X coordinate of the center
            center_y (int): Y coordinate of the center
        """
        size = self.cell_size // 3
        pygame.draw.circle(
            self.screen, self.o_color,
            (center_x, center_y),
            size,
            width=2  # Thinner circle for smaller cells
        )
    
    def _draw_status(self, game):
        """Draw the game status.
        
        Args:
            game (TicTacToe): The game instance
        """
        # Draw title
        title = self.large_font.render("Tic-Tac-Toe RL", True, self.text_color)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 10))
        
        # Draw game status
        if game.winner:
            status = f"Player {game.winner} wins!"
            color = self.x_color if game.winner == 'X' else self.o_color
        elif game.is_draw:
            status = "It's a draw!"
            color = self.text_color
        else:
            status = f"Player {game.current_player}'s turn"
            color = self.x_color if game.current_player == 'X' else self.o_color
        
        status_text = self.font.render(status, True, color)
        status_pos = (self.width // 2 - status_text.get_width() // 2, 
                      self.board_pos[1] + self.board_size + 20)
        self.screen.blit(status_text, status_pos)