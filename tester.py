import pdb
import pygame

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5

    def move_towards_player(self, player_x, player_y):
        if self.x < player_x:
            self.x += self.speed
        elif self.x > player_x:
            self.x -= self.speed

        if self.y < player_y:
            self.y += self.speed
        elif self.y > player_y:
            self.y -= self.speed

enemy = Enemy(100, 100)

# Основной цикл игры
running = True
clock = pygame.time.Clock()

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Искусственный интеллект
    enemy.move_towards_player(player_x, player_y)

    # Отрисовка игровых объектов
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (enemy.x, enemy.y), 10)
    pygame.draw.circle(screen, (0, 0, 255), (player_x, player_y), 10)

    pygame.display.update()

pygame.quit()
# Основной цикл игры
running = True
clock = pygame.time.Clock()

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Искусственный интеллект
    enemy.move_towards_player(player_x, player_y)

    # Отрисовка игровых объектов
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (enemy.x, enemy.y), 10)
    pygame.draw.circle(screen, (0, 0, 255), (player_x, player_y), 10)

    pygame.display.update()

    # Отладка
    pdb.set_trace()
    print("Player x: ", player_x)
    print("Player y: ", player_y)
    print("Enemy x: ", enemy.x)
    print("Enemy y: ", enemy.y)

pygame.quit()