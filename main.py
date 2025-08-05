import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Spaceship Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
BULLET_VEL = 7
MAX_BULLETS = 3

w, h = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

CURRENT_DIFFICULTY = 1
MAX_DIFFICULTY = 5

try:
    BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Grenade+1.mp3'))
    BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Gun+Silencer.mp3'))
except:
    print("Sound files not found - continuing without sound")
    BULLET_HIT_SOUND = None
    BULLET_FIRE_SOUND = None

HEALTH_FONT = pygame.font.SysFont('sans', 40)
WINNER_FONT = pygame.font.SysFont('sans', 100)

VEL = 5
AI_VEL = 3  

try:
    yellow_spaceship = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
    yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship, (w, h)), 90)

    red_spaceship = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))
    red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_spaceship, (w, h)), 270)

    SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))
except:
    print("Image files not found - creating placeholder graphics")
    yellow_spaceship = pygame.Surface((w, h))
    yellow_spaceship.fill(YELLOW)
    red_spaceship = pygame.Surface((w, h))
    red_spaceship.fill(RED)
    SPACE = pygame.Surface((WIDTH, HEIGHT))
    SPACE.fill((0, 0, 50))  

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("AI Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Your Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(yellow_spaceship, (yellow.x, yellow.y))
    WIN.blit(red_spaceship, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  
        yellow.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            if BULLET_HIT_SOUND:
                BULLET_HIT_SOUND.play()
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            if BULLET_HIT_SOUND:
                BULLET_HIT_SOUND.play()
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)

def ai_movement(red, yellow, red_bullets, difficulty):
    current_ai_vel = AI_VEL + (difficulty * 0.5)
    
    if red.y < yellow.y and red.y + current_ai_vel + red.height < HEIGHT - 15:
        red.y += current_ai_vel
    elif red.y > yellow.y and red.y - current_ai_vel > 0:
        red.y -= current_ai_vel
    
    if random.random() < 0.01 + (0.01 * difficulty):
        red.x += random.choice([-1, 1]) * current_ai_vel
    
    if len(red_bullets) < MAX_BULLETS + difficulty and random.random() < 0.01 + (0.01 * difficulty):
        bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
        red_bullets.append(bullet)
        if BULLET_FIRE_SOUND:
            BULLET_FIRE_SOUND.play()

def video_game():
    global CURRENT_DIFFICULTY
    
    while CURRENT_DIFFICULTY <= MAX_DIFFICULTY:
        red = pygame.Rect(700, 300, w, h)
        yellow = pygame.Rect(100, 300, w, h)
        
        red_bullets = []
        yellow_bullets = []
        
        red_health = 10 + CURRENT_DIFFICULTY
        yellow_health = 10
        
        clock = pygame.time.Clock()
        run = True
        
        while run:
            clock.tick(FPS)
            
            winner_text = ""
            if red_health <= 0:
                winner_text = f"You Win! Level {CURRENT_DIFFICULTY}"
                CURRENT_DIFFICULTY += 1
            elif yellow_health <= 0:
                winner_text = "Game Over"
                CURRENT_DIFFICULTY = 1  
            
            if winner_text:
                draw_winner(winner_text)
                break
            
            keys_pressed = pygame.key.get_pressed()
            yellow_movement(keys_pressed, yellow)
            ai_movement(red, yellow, red_bullets, CURRENT_DIFFICULTY)
            
        if CURRENT_DIFFICULTY > MAX_DIFFICULTY:
            draw_winner("You Beat All Levels!")
            break

def video_game():
    global CURRENT_DIFFICULTY
    
    while CURRENT_DIFFICULTY <= MAX_DIFFICULTY:
        red = pygame.Rect(700, 300, w, h)
        yellow = pygame.Rect(100, 300, w, h)
        
        red_bullets = []
        yellow_bullets = []
        
        red_health = 10 + CURRENT_DIFFICULTY
        yellow_health = 10
        
        clock = pygame.time.Clock()
        run = True
        
        while run:
            clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                        yellow_bullets.append(bullet)
                        if BULLET_FIRE_SOUND:
                            BULLET_FIRE_SOUND.play()
                
                if event.type == RED_HIT:
                    red_health -= 1
                    if BULLET_HIT_SOUND:
                        BULLET_HIT_SOUND.play()
                
                if event.type == YELLOW_HIT:
                    yellow_health -= 1
                    if BULLET_HIT_SOUND:
                        BULLET_HIT_SOUND.play()
            
            winner_text = ""
            if red_health <= 0:
                winner_text = f"You Win! Level {CURRENT_DIFFICULTY}"
                CURRENT_DIFFICULTY += 1
            elif yellow_health <= 0:
                winner_text = "Game Over"
                CURRENT_DIFFICULTY = 1
            
            if winner_text:
                draw_winner(winner_text)
                break
            
            keys_pressed = pygame.key.get_pressed()
            yellow_movement(keys_pressed, yellow)
            ai_movement(red, yellow, red_bullets, CURRENT_DIFFICULTY)
            
            handle_bullets(yellow_bullets, red_bullets, yellow, red)
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        
        if CURRENT_DIFFICULTY > MAX_DIFFICULTY:
            draw_winner("You Beat All Levels!")
            break
    
    pygame.quit()

if __name__ == "__main__":
    video_game()
