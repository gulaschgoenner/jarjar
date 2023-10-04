import pygame
import random
import mysql.connector

# Konstanten
GRID_WIDTH = 20
GRID_HEIGHT = 15
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BACKGROUND_COLOR_1 = (0, 0, 0)
BACKGROUND_COLOR_2 = (22, 22, 23)

# Initialisierung von Pygame
pygame.init()

pygame.display.set_caption("Snake")
WINDOW_SIZE = (GRID_WIDTH * 20, GRID_HEIGHT * 20)
screen = pygame.display.set_mode(WINDOW_SIZE)

clock = pygame.time.Clock()


class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

# Datenbankkrampf
def insert_score(name, score):
    try:
        # Verbindung zur MySQL-Datenbank herstellen
        connection = mysql.connector.connect(
            host='localhost',
            user='guest',
            password='1234',
            database='snake'
        )

        # Cursor erstellen
        cursor = connection.cursor()

        # SQL-Befehl mit Platzhaltern ausführen
        sql = "INSERT INTO Scores (name, score) VALUES (%s, %s)"
        values = (name, score)
        cursor.execute(sql, values)

        # Transaktion bestätigen
        connection.commit()

        print(f'Datensatz wurde erfolgreich eingefügt: ({name}, {score})')

    except Exception as error:
        print(f'Fehler beim Einfügen des Datensatzes: {error}')

    finally:
        # Verbindung schließen
        cursor.close()
        connection.close()



# Funktion für das Spielende
def game_over(score):
    insert_score("Beispiel Name", score)

    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    retry_font = pygame.font.Font(None, 24)
    retry_text = retry_font.render("Retry (Up)", True, (255, 255, 255))
    retry_rect = retry_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    screen.blit(retry_text, retry_rect)

    score_font = pygame.font.Font(None, 24)
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(50, 20))
    screen.blit(score_text, score_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    main()


# Hauptfunktion für das Spiel
def main():
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = Direction.RIGHT
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if direction != Direction.DOWN:
                        direction = Direction.UP
                elif event.key == pygame.K_s:
                    if direction != Direction.UP:
                        direction = Direction.DOWN
                elif event.key == pygame.K_a:
                    if direction != Direction.RIGHT:
                       direction = Direction.LEFT
                elif event.key == pygame.K_d:
                    if direction != Direction.LEFT:
                        direction = Direction.RIGHT

        # Bewegung der Schlange
        head = (snake[-1][0] + direction[0], snake[-1][1] + direction[1])

        # Kollisionen
        if not (0 <= head[0] < GRID_WIDTH) or not (0 <= head[1] < GRID_HEIGHT):
            game_over(score)

        if head in snake:
            game_over(score)

        snake.append(head)

        # Essen einverleiben
        if head == food:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            score += 1;
        else:
            snake.pop(0)

        # Zeichnen des Spielfelds
        screen.fill(BACKGROUND_COLOR_1)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = BACKGROUND_COLOR_2 if (x + y) % 2 == 0 else BACKGROUND_COLOR_1
                pygame.draw.rect(screen, color, (x * 20, y * 20, 20, 20))

        # Zeichnen der Schlange
        for segment in snake:
            pygame.draw.rect(screen, SNAKE_COLOR, (segment[0] * 20, segment[1] * 20, 20, 20))

        # Zeichnen des Essens
        pygame.draw.rect(screen, FOOD_COLOR, (food[0] * 20, food[1] * 20, 20, 20))

        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()
