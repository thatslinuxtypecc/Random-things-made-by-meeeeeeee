import pygame, random, sys

pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Uzay Savaşı Ultimate")

clock = pygame.time.Clock()

# renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 50, 50)
BLUE  = (50, 150, 255)
YELLOW= (255, 255, 0)
ORANGE= (255, 150, 0)
GREEN = (0, 255, 0)

font = pygame.font.SysFont("consolas", 25)

# oyuncu
player = pygame.Rect(WIDTH//2 - 20, HEIGHT - 60, 40, 40)
player_speed = 6
player_life = 5

# mermiler ve düşmanlar
bullets = []
enemy_bullets = []
enemies = []

import pygame, random, sys

pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Uzay Savaşı Ultimate + Boss")

clock = pygame.time.Clock()

# renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 50, 50)
BLUE  = (50, 150, 255)
YELLOW= (255, 255, 0)
ORANGE= (255, 150, 0)
GREEN = (0, 255, 0)
PURPLE= (180, 0, 180)

font = pygame.font.SysFont("consolas", 25)

# oyuncu
player = pygame.Rect(WIDTH//2 - 20, HEIGHT - 60, 40, 40)
player_speed = 6
player_life = 5

# mermiler ve düşmanlar
bullets = []
enemy_bullets = []
enemies = []
bosses = []

bullet_speed = -8
enemy_bullet_speed = 5
score = 0
spawn_timer = 0
level = 1

# patlamalar
explosions = []

running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    # level sistemi
    level = score // 10 + 1
    max_enemies = min(5 + level, 15)
    enemy_speed_increment = level // 2

    # boss çıkma koşulu
    if level % 5 == 0 and not bosses:  # her 5 levelde bir boss
        boss_rect = pygame.Rect(WIDTH//2 - 60, -120, 120, 80)
        bosses.append({"rect": boss_rect, "life": 30 + level*5, "speed": 2, "fire_timer": 50, "dir_toggle": True})

    # olaylar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:
            bullet = pygame.Rect(player.centerx - 3, player.top - 10, 6, 12)
            bullets.append(bullet)

    # mermiler hareket
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)

    for bullet in enemy_bullets[:]:
        bullet.y += enemy_bullet_speed
        if bullet.top > HEIGHT:
            enemy_bullets.remove(bullet)
        elif bullet.colliderect(player):
            enemy_bullets.remove(bullet)
            player_life -= 1
            explosions.append([player.centerx, player.centery, 20])

    # düşman oluşturma
    spawn_timer += 1
    if spawn_timer > max(50 - level*2, 20) and len(enemies) < max_enemies:
        w = random.randint(30, 50)
        h = random.randint(30, 50)
        x = random.randint(20, WIDTH - w - 20)
        speed = random.randint(2 + enemy_speed_increment, 5 + enemy_speed_increment)
        enemies.append({
            "rect": pygame.Rect(x, -h, w, h),
            "speed": speed,
            "fire_timer": random.randint(30, 90),
            "dir_toggle": random.choice([True, False])
        })
        spawn_timer = 0

    # düşman hareket ve ateş
    for enemy in enemies[:]:
        if enemy["dir_toggle"]:
            enemy["rect"].x += 1
        else:
            enemy["rect"].x -= 1
        if enemy["rect"].left <= 0 or enemy["rect"].right >= WIDTH:
            enemy["dir_toggle"] = not enemy["dir_toggle"]

        enemy["rect"].y += enemy["speed"]
        enemy["fire_timer"] -= 1
        if enemy["fire_timer"] <= 0:
            eb = pygame.Rect(enemy["rect"].centerx-3, enemy["rect"].bottom, 6, 12)
            enemy_bullets.append(eb)
            enemy["fire_timer"] = max(30, random.randint(60, 120) - level*2)

        if enemy["rect"].top > HEIGHT:
            enemies.remove(enemy)

        for bullet in bullets[:]:
            if enemy["rect"].colliderect(bullet):
                explosions.append([enemy["rect"].centerx, enemy["rect"].centery, 20])
                try:
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                except ValueError:
                    pass
                break

        if enemy["rect"].colliderect(player):
            explosions.append([player.centerx, player.centery, 20])
            player_life -= 1
            enemies.remove(enemy)

    # boss hareket ve ateş
    for boss in bosses[:]:
        if boss["dir_toggle"]:
            boss["rect"].x += boss["speed"]
        else:
            boss["rect"].x -= boss["speed"]
        if boss["rect"].left <= 0 or boss["rect"].right >= WIDTH:
            boss["dir_toggle"] = not boss["dir_toggle"]

        boss["fire_timer"] -= 1
        if boss["fire_timer"] <= 0:
            eb = pygame.Rect(boss["rect"].centerx-5, boss["rect"].bottom, 10, 15)
            enemy_bullets.append(eb)
            boss["fire_timer"] = max(30, 80 - level*2)

        # boss çarpışma ve hasar
        for bullet in bullets[:]:
            if boss["rect"].colliderect(bullet):
                bullets.remove(bullet)
                boss["life"] -= 1
                explosions.append([bullet.centerx, bullet.centery, 10])
                if boss["life"] <= 0:
                    explosions.append([boss["rect"].centerx, boss["rect"].centery, 40])
                    bosses.remove(boss)
                    score += 10
                break

        if boss["rect"].colliderect(player):
            player_life -= 2
            explosions.append([player.centerx, player.centery, 20])
            boss["rect"].y += 20  # çarpışmada player’dan biraz uzaklaş

    # patlamalar animasyon
    for explosion in explosions[:]:
        x, y, radius = explosion
        pygame.draw.circle(screen, ORANGE, (x,y), radius)
        explosion[2] += 5
        if explosion[2] > 50:
            explosions.remove(explosion)

    # çizimler
    pygame.draw.polygon(screen, BLUE, [
        (player.centerx, player.top),
        (player.left, player.bottom),
        (player.right, player.bottom)
    ])

    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, RED, bullet)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy["rect"])
        pygame.draw.rect(screen, WHITE, enemy["rect"], 2)
    for boss in bosses:
        pygame.draw.rect(screen, PURPLE, boss["rect"])
        pygame.draw.rect(screen, WHITE, boss["rect"], 2)
        # boss can barı
        pygame.draw.rect(screen, RED, (boss["rect"].x, boss["rect"].y-10, boss["rect"].width, 5))
        pygame.draw.rect(screen, GREEN, (boss["rect"].x, boss["rect"].y-10, boss["rect"].width * (boss["life"]/ (30 + level*5)), 5))

    # skor, can ve level
    score_text = font.render(f"Skor: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (WIDTH-120, 10))
    pygame.draw.rect(screen, RED, (10, 40, 100, 15))
    pygame.draw.rect(screen, GREEN, (10,40,20*player_life,15))

    pygame.display.flip()

    if player_life <= 0:
        running = False

pygame.quit()
print(f"Oyun bitti! Skorun: {score} | Level: {level}")
