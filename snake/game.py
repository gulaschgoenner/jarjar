import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_WIDTH = 20
GRID_HEIGHT = 15
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BACKGROUND_COLOR_1 = (0, 0, 0)
BACKGROUND_COLOR_2 = (22, 22, 23)
GRID_SIZE = 20
SCREEN_WIDTH = GRID_WIDTH * GRID_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * GRID_SIZE

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling the game loop speed
clock = pygame.time.Clock()

# Initialize fonts
font = pygame.font.Font(None, 36)
game_over_text = font.render("Game Over", True, (255, 255, 255))
retry_text = font.render("Retry (Up)", True, (255, 255, 255))

# Define directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = RIGHT

    def move(self):
        head = self.body[-1]
        x, y = head
        dx, dy = self.direction
        new_head = (x + dx, y + dy)
        self.body.append(new_head)
        self.body.pop(0)

    def grow(self):
        tail = self.body[0]
        x, y = tail
        dx, dy = self.direction
        new_tail = (x - dx, y - dy)
        self.body.insert(0, new_tail)

    def check_collision(self):
        head = self.body[-1]
        return head in self.body[:-1]

    def check_boundaries(self):
        x, y = head = self.body[-1]
        return not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT)

    def draw(self):
        for segment in self.body:
            x, y = segment
            pygame.draw.rect(screen, SNAKE_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

    def respawn(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

    def draw(self):
        x, y = self.position
        pygame.draw.rect(screen, FOOD_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_background():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = BACKGROUND_COLOR_1 if (x + y) % 2 == 0 else BACKGROUND_COLOR_2
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

snake = Snake()
food = Food()
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if snake.check_collision() or snake.check_boundaries():
                    snake = Snake()  # Retry on 'w'
            if event.key == pygame.K_w and snake.direction != DOWN:
                snake.direction = UP
            elif event.key == pygame.K_s and snake.direction != UP:
                snake.direction = DOWN
            elif event.key == pygame.K_a and snake.direction != RIGHT:
                snake.direction = LEFT
            elif event.key == pygame.K_d and snake.direction != LEFT:
                snake.direction = RIGHT

    snake.move()

    game_over = snake.check_collision() or snake.check_boundaries()
    if game_over:
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
        pygame.display.flip()

    if snake.body[-1] == food.position:
        snake.grow()
        food.respawn()

    screen.fill((0, 0, 0))
    draw_background()
    snake.draw()
    food.draw()

   if game_over:
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
        pygame.display.flip()

    pygame.display.flip()
    clock.tick(10)
