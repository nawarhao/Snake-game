import pygame
import random

pygame.init()
cell_size = 20
cols, rows = 40, 30
screen_width, screen_height = cols * cell_size, rows * cell_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

APPLE_COUNT = 5

class Snake:
    def __init__(self):
        self.body = [(10, 10)]
        self.direction = (1, 0)
        self.grow = False
    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        if (new_head in self.body or
            new_head[0] < 0 or new_head[0] >= cols or
            new_head[1] < 0 or new_head[1] >= rows):
            return False
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True
    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir
    def draw(self):
        for x, y in self.body:
            pygame.draw.rect(screen, (0, 255, 0), (x * cell_size, y * cell_size, cell_size, cell_size))

class Apple:
    def __init__(self, snake_body):
        self.respawn(snake_body)
    def respawn(self, snake_body):
        while True:
            new_pos = (random.randint(0, cols - 1), random.randint(0, rows - 1))
            if new_pos not in snake_body:
                self.pos = new_pos
                break
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.pos[0] * cell_size, self.pos[1] * cell_size, cell_size, cell_size))

def spawn_apples(count, snake_body):
    apples = []
    for _ in range(count):
        apples.append(Apple(snake_body))
    return apples

def draw_grid():
    for x in range(0, screen_width, cell_size):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, screen_height))
    for y in range(0, screen_height, cell_size):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (screen_width, y))

snake = Snake()
apples = spawn_apples(APPLE_COUNT, snake.body)
score = 0
font = pygame.font.Font(None, 36)
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_UP]:
            snake.change_direction((0, -1))
        if keys[pygame.K_DOWN]:
            snake.change_direction((0, 1))
        if keys[pygame.K_LEFT]:
            snake.change_direction((-1, 0))
        if keys[pygame.K_RIGHT]:
            snake.change_direction((1, 0))

        if not snake.move():
            game_over = True

        eaten = []
        for apple in apples:
            if snake.body[0] == apple.pos:
                score += 1
                snake.grow = True
                eaten.append(apple)
        for e in eaten:
            apples.remove(e)

        if not apples:
            apples = spawn_apples(APPLE_COUNT, snake.body)

    screen.fill((0, 0, 0))
    draw_grid()
    snake.draw()
    for apple in apples:
        apple.draw()
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    if game_over:
        over_text = font.render("GAME OVER", True, (255, 50, 50))
        screen.blit(over_text, (screen_width // 2 - over_text.get_width() // 2,
                                screen_height // 2 - over_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(10)
