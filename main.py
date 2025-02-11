import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Game window settings
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Extreme Dodger")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Player settings
PLAYER_SIZE = 20
PLAYER_SPEED = 8
GRAVITY = 0.8
JUMP_FORCE = -15

# Obstacle settings
MIN_OBSTACLE_SPEED = 8
MAX_OBSTACLE_SPEED = 20
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 30

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH//4, HEIGHT//2))
        self.velocity = 0
        self.on_ground = True

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Ground collision
        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.on_ground = True
            self.velocity = 0

    def jump(self):
        if self.on_ground:
            self.velocity = JUMP_FORCE
            self.on_ground = False

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed_multiplier):
        super().__init__()
        self.type = random.choice(['horizontal', 'vertical', 'diagonal', 'homing'])
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed_multiplier = speed_multiplier
        self.reset_position()

    def reset_position(self):
        if self.type == 'vertical':
            self.rect.center = (random.randint(WIDTH, WIDTH+300), random.randint(50, HEIGHT-50))
            self.speed = random.randint(MIN_OBSTACLE_SPEED, MAX_OBSTACLE_SPEED) * self.speed_multiplier
        elif self.type == 'horizontal':
            self.rect.center = (random.randint(WIDTH//2, WIDTH), random.choice([50, HEIGHT-50]))
            self.speed = random.randint(MIN_OBSTACLE_SPEED, MAX_OBSTACLE_SPEED) * self.speed_multiplier
        elif self.type == 'diagonal':
            self.rect.center = (WIDTH, random.randint(50, HEIGHT-50))
            self.speed_x = random.randint(MIN_OBSTACLE_SPEED, MAX_OBSTACLE_SPEED) * self.speed_multiplier
            self.speed_y = random.choice([-1, 1]) * self.speed_multiplier * 0.5
        elif self.type == 'homing':
            self.rect.center = (random.randint(WIDTH, WIDTH+300), random.randint(50, HEIGHT-50))
            self.speed = random.randint(MIN_OBSTACLE_SPEED, MAX_OBSTACLE_SPEED) * self.speed_multiplier

    def update(self, player_pos):
        if self.type == 'vertical':
            self.rect.x -= self.speed
        elif self.type == 'horizontal':
            self.rect.y += self.speed if self.rect.y == 50 else -self.speed
        elif self.type == 'diagonal':
            self.rect.x -= self.speed_x
            self.rect.y += self.speed_y
        elif self.type == 'homing':
            dx = player_pos[0] - self.rect.x
            dy = player_pos[1] - self.rect.y
            distance = math.hypot(dx, dy)
            if distance != 0:
                self.rect.x += (dx / distance) * self.speed
                self.rect.y += (dy / distance) * self.speed

        if self.rect.right < 0 or self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.reset_position()

def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    player = Player()
    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    speed_multiplier = 1.0
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                if event.key == pygame.K_r and game_over:
                    main()

        if not game_over:
            # Spawn obstacles
            if random.random() < 0.05 * speed_multiplier:
                obstacle = Obstacle(speed_multiplier)
                obstacles.add(obstacle)
                all_sprites.add(obstacle)

            # Update
            player.update()
            obstacles.update(player.rect.center)

            # Increase difficulty
            score += 1
            if score % 500 == 0:
                speed_multiplier *= 1.2

            # Collision detection
            if pygame.sprite.spritecollide(player, obstacles, False, pygame.sprite.collide_mask):
                game_over = True

        # Drawing
        pygame.draw.line(WIN, WHITE, (0, HEIGHT-50), (WIDTH, HEIGHT-50), 2)
        all_sprites.draw(WIN)
        
        # Score display
        score_text = font.render(f"Score: {score}", True, WHITE)
        WIN.blit(score_text, (10, 10))
        
        if game_over:
            game_over_text = font.render("Game Over! Press R to restart", True, RED)
            WIN.blit(game_over_text, (WIDTH//2 - 180, HEIGHT//2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()