import pygame
import random

# Konstanten für das Spielfeld
GRID_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15
CANVAS_WIDTH = GRID_SIZE * GRID_WIDTH
CANVAS_HEIGHT = GRID_SIZE * GRID_HEIGHT

# Farben
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BACKGROUND_COLOR_1 = (0, 0, 0)
BACKGROUND_COLOR_2 = (22, 22, 23)

# Richtungen
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialisierung
pygame.init()
screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
direction = RIGHT
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
score = 0
game_over = False

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, FOOD_COLOR, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def move_snake(snake, direction):
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])
    snake.insert(0, new_head)

def check_collision(snake):
    head = snake[0]
    if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
        return True
    if head in snake[1:]:
        return True
    return False

def generate_food(snake):
    while True:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food not in snake:
            return food

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and direction != DOWN:
                direction = UP
            elif event.key == pygame.K_s and direction != UP:
                direction = DOWN
            elif event.key == pygame.K_a and direction != RIGHT:
                direction = LEFT
            elif event.key == pygame.K_d and direction != LEFT:
                direction = RIGHT

    move_snake(snake, direction)

    if snake[0] == food:
        score += 1
        food = generate_food(snake)
    else:
        snake.pop()

    if check_collision(snake):
        game_over = True

    screen.fill(BACKGROUND_COLOR_1)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if (x + y) % 2 == 0:
                pygame.draw.rect(screen, BACKGROUND_COLOR_1, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(screen, BACKGROUND_COLOR_2, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    draw_snake(snake)
    draw_food(food)
    pygame.display.update()
    clock.tick(10)  # Geschwindigkeit der Schlange

pygame.quit()
