import pygame
import sys

# Inicializa o pygame
pygame.init()

# Cores
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Tamanho da tela
WIDTH, HEIGHT = 560, 620
TILE_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

clock = pygame.time.Clock()

# Mapa (20x28)
# 1 = parede, 0 = ponto, 2 = vazio
level = [
    "1111111111111111111111111111",
    "1000000000110000000000000001",
    "1011111110110111111111111101",
    "1010000010000000000010000101",
    "1010111011111111101110111101",
    "1000100000000000000000000001",
    "1110111110111110111110111111",
    "1000000010000100000010000001",
    "1011111011111111111011111101",
    "1000000000001000000000000001",
    "1111111111111111111111111111"
]

# Converte o mapa em lista de listas
grid = [list(row) for row in level]

# Personagem
pacman_x = 1
pacman_y = 1

def draw_map():
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == '1':
                pygame.draw.rect(screen, BLUE, rect)
            elif tile == '0':
                pygame.draw.circle(screen, WHITE, rect.center, 3)

def move_pacman(dx, dy):
    global pacman_x, pacman_y
    new_x = pacman_x + dx
    new_y = pacman_y + dy
    if grid[new_y][new_x] != '1':
        pacman_x = new_x
        pacman_y = new_y
        if grid[new_y][new_x] == '0':
            grid[new_y][new_x] = '2'  # comeu o ponto

running = True
while running:
    screen.fill(BLACK)
    draw_map()

    # Desenha o Pac-Man
    pygame.draw.circle(
        screen,
        YELLOW,
        (pacman_x * TILE_SIZE + TILE_SIZE // 2, pacman_y * TILE_SIZE + TILE_SIZE // 2),
        TILE_SIZE // 2 - 2
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Teclado
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        move_pacman(-1, 0)
    elif keys[pygame.K_RIGHT]:
        move_pacman(1, 0)
    elif keys[pygame.K_UP]:
        move_pacman(0, -1)
    elif keys[pygame.K_DOWN]:
        move_pacman(0, 1)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
