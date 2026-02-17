import pygame
import random
from enum import Enum
from collections import deque

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self, width=640, height=480, grid_size=20):
        pygame.init()
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.GRAY = (128, 128, 128)
        
        # Game variables
        self.reset_game()
        self.paused = False
    
    def reset_game(self):
        """Initialize game state"""
        start_x = self.width // (2 * self.grid_size)
        start_y = self.height // (2 * self.grid_size)
        
        self.snake = deque([(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)])
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
    
    def spawn_food(self):
        """Spawn food at a random location not occupied by snake"""
        while True:
            x = random.randint(0, (self.width // self.grid_size) - 1)
            y = random.randint(0, (self.height // self.grid_size) - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.next_direction = Direction.RIGHT
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_q:
                    return False
        
        return True
    
    def update(self):
        """Update game state"""
        if self.game_over or self.paused:
            return
        
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.width // self.grid_size or
            new_head[1] < 0 or new_head[1] >= self.height // self.grid_size):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Move snake
        self.snake.appendleft(new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()
    
    def draw(self):
        """Draw game elements"""
        self.screen.fill(self.BLACK)
        
        # Draw grid
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(self.screen, self.GRAY, (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(self.screen, self.GRAY, (0, y), (self.width, y))
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            color = self.GREEN if i == 0 else (0, 200, 0)
            pygame.draw.rect(self.screen, color, 
                           (x * self.grid_size, y * self.grid_size, 
                            self.grid_size - 2, self.grid_size - 2))
        
        # Draw food
        food_x, food_y = self.food
        pygame.draw.rect(self.screen, self.RED, 
                        (food_x * self.grid_size, food_y * self.grid_size, 
                         self.grid_size - 2, self.grid_size - 2))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw pause text
        if self.paused:
            pause_text = self.font.render("PAUSED (Press SPACE to resume)", True, self.WHITE)
            text_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(pause_text, text_rect)
        
        # Draw game over text
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, self.RED)
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 40))
            self.screen.blit(game_over_text, text_rect)
            
            restart_text = self.font.render("Press R to restart or Q to quit", True, self.WHITE)
            text_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 40))
            self.screen.blit(restart_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_events()
            
            # Handle restart
            if self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.reset_game()
                        elif event.key == pygame.K_q:
                            running = False
            
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS for snake movement
        
        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()