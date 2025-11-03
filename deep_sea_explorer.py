import pygame
import random
import sys
import numpy as np  # <-- required for sound buffer arrays

# Initialize pygame and mixer for sound
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
DARK_BLUE = (0, 26, 51)
OCEAN_BLUE = (0, 51, 102)
DEEP_BLUE = (0, 77, 128)
GOLD = (255, 215, 0)
PEARL_WHITE = (255, 248, 220)
RED = (139, 0, 0)
PURPLE = (255, 0, 255)
CORAL_RED = (255, 99, 71)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
LIGHT_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Deep Sea Explorer")
clock = pygame.time.Clock()

# Font
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)
font_tiny = pygame.font.Font(None, 24)

# ---------------- SOUND FUNCTIONS ---------------- #

def create_sound_wave(frequency, duration):
    """Generate a simple sine wave sound as a NumPy array."""
    sample_rate = 22050
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # smoother than square wave
    wave = (wave * 32767).astype(np.int16)  # convert to 16-bit
    stereo_wave = np.column_stack((wave, wave))  # duplicate for stereo
    return stereo_wave

def play_collect_sound():
    sound = pygame.mixer.Sound(buffer=create_sound_wave(800, 0.1))
    sound.set_volume(0.3)
    sound.play()

def play_collision_sound():
    sound = pygame.mixer.Sound(buffer=create_sound_wave(150, 0.2))
    sound.set_volume(0.3)
    sound.play()

# ---------------- GAME CLASSES ---------------- #

class Submarine:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.width = 60
        self.height = 30
        self.velocity_y = 0
        self.gravity = 0.3
        
    def move_up(self):
        self.velocity_y = -6
    
    def update(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        if self.y < 0:
            self.y = 0
            self.velocity_y = 0
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.velocity_y = 0
    
    def draw(self, surface):
        pygame.draw.ellipse(surface, GOLD, (self.x, self.y, self.width, self.height))
        pygame.draw.circle(surface, LIGHT_BLUE, (self.x + 20, self.y + 15), 8)
        pygame.draw.rect(surface, GOLD, (self.x + 35, self.y - 5, 3, 10))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Collectible:
    def __init__(self, x, y, collectible_type):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.type = collectible_type
        
        if self.type == 'pearl':
            self.value = 10
            self.color = PEARL_WHITE
        elif self.type == 'treasure':
            self.value = 50
            self.color = GOLD
        else:
            self.value = 5
            self.color = (218, 165, 32)
    
    def update(self, speed):
        self.x -= speed
    
    def draw(self, surface):
        if self.type == 'pearl':
            pygame.draw.circle(surface, self.color, (int(self.x + 12), int(self.y + 12)), 12)
        elif self.type == 'treasure':
            pygame.draw.rect(surface, GOLD, (int(self.x), int(self.y), self.width, self.height))
            pygame.draw.rect(surface, (139, 69, 19), (int(self.x + 8), int(self.y + 8), 9, 9))
        else:
            pygame.draw.circle(surface, self.color, (int(self.x + 12), int(self.y + 12)), 10)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        return self.x < -self.width

class Obstacle:
    def __init__(self, x, y, obstacle_type):
        self.x = x
        self.y = y
        self.type = obstacle_type
        if self.type == 'coral':
            self.width = 30
            self.height = 40
        else:
            self.width = 35
            self.height = 35
    
    def update(self, speed):
        self.x -= speed
    
    def draw(self, surface):
        if self.type == 'mine':
            pygame.draw.circle(surface, RED, (int(self.x + 17), int(self.y + 17)), 17)
            for i in range(8):
                angle = (i * 3.14159 * 2) / 8
                end_x = int(self.x + 17 + 25 * pygame.math.Vector2(1, 0).rotate_rad(angle).x)
                end_y = int(self.y + 17 + 25 * pygame.math.Vector2(1, 0).rotate_rad(angle).y)
                pygame.draw.line(surface, RED, (int(self.x + 17), int(self.y + 17)), (end_x, end_y), 3)
        elif self.type == 'jellyfish':
            pygame.draw.circle(surface, PURPLE, (int(self.x + 17), int(self.y + 10)), 15)
            pygame.draw.rect(surface, PURPLE, (int(self.x), int(self.y + 10), 35, 2))
            pygame.draw.rect(surface, PURPLE, (int(self.x + 10), int(self.y + 12), 4, 20))
            pygame.draw.rect(surface, PURPLE, (int(self.x + 20), int(self.y + 12), 4, 20))
        else:
            pygame.draw.rect(surface, CORAL_RED, (int(self.x), int(self.y), self.width, self.height))
            for i in range(3):
                pygame.draw.rect(surface, (255, 69, 0), (int(self.x + i * 10), int(self.y - 5), 5, 10))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        return self.x < -self.width

# ---------------- DRAW FUNCTIONS ---------------- #

def draw_background(offset):
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(0 * (1 - ratio) + 0 * ratio)
        g = int(26 * (1 - ratio) + 77 * ratio)
        b = int(51 * (1 - ratio) + 128 * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    for i in range(20):
        x = int((offset * 0.5 + i * 40) % SCREEN_WIDTH)
        y = (i * 37) % SCREEN_HEIGHT
        pygame.draw.circle(screen, (255, 255, 255, 30), (x, y), 3)

def draw_start_screen():
    screen.fill(DARK_BLUE)
    title = font_large.render("Deep Sea Explorer", True, CYAN)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title, title_rect)
    instructions = [
        "Collect treasures, pearls, and coins!",
        "Avoid mines, jellyfish, and coral!",
        "",
        "Controls:",
        "SPACE or UP ARROW - Rise up",
        "Release - Sink naturally",
        "P - Pause game",
        "",
        "Press SPACE to Start"
    ]
    y_offset = 200
    for line in instructions:
        if line == "":
            y_offset += 10
            continue
        text = font_tiny.render(line, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(text, text_rect)
        y_offset += 30
    score_info = font_tiny.render("Pearl: 10pts | Coin: 5pts | Treasure: 50pts", True, YELLOW)
    score_rect = score_info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    screen.blit(score_info, score_rect)

def draw_game_over_screen(score, high_score):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(230)
    overlay.fill(DARK_BLUE)
    screen.blit(overlay, (0, 0))
    game_over = font_large.render("Submarine Damaged!", True, RED)
    game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(game_over, game_over_rect)
    score_text = font_medium.render(f"Final Score: {score}", True, YELLOW)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
    screen.blit(score_text, score_rect)
    if score == high_score and score > 0:
        high_score_text = font_small.render("NEW HIGH SCORE!", True, YELLOW)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        screen.blit(high_score_text, high_score_rect)
    restart = font_small.render("Press SPACE to Dive Again", True, WHITE)
    restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, 450))
    screen.blit(restart, restart_rect)

def draw_pause_screen():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(DARK_BLUE)
    screen.blit(overlay, (0, 0))
    paused = font_large.render("PAUSED", True, CYAN)
    paused_rect = paused.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(paused, paused_rect)
    continue_text = font_small.render("Press P to Continue", True, WHITE)
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(continue_text, continue_rect)

# ---------------- MAIN GAME LOOP ---------------- #

def main():
    game_state = "start"
    score = 0
    high_score = 0
    paused = False
    
    submarine = Submarine()
    collectibles = []
    obstacles = []
    
    background_offset = 0
    game_speed = 2
    spawn_timer = 0
    obstacle_timer = 0
    difficulty = 1.0
    difficulty_timer = 0
    
    running = True
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_state == "start":
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        game_state = "playing"
                        score = 0
                        submarine = Submarine()
                        collectibles = []
                        obstacles = []
                        game_speed = 2
                        difficulty = 1.0
                        spawn_timer = obstacle_timer = difficulty_timer = 0
                        paused = False
                elif game_state == "playing":
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        submarine.move_up()
                    if event.key == pygame.K_p:
                        paused = not paused
                elif game_state == "gameover":
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        game_state = "start"
        
        if game_state == "start":
            draw_start_screen()
        
        elif game_state == "playing":
            if not paused:
                submarine.update()
                background_offset += game_speed
                
                spawn_timer += 1
                if spawn_timer > 60 / difficulty:
                    collectible_type = random.choice(['pearl', 'treasure', 'coin'])
                    y_pos = random.randint(25, SCREEN_HEIGHT - 50)
                    collectibles.append(Collectible(SCREEN_WIDTH, y_pos, collectible_type))
                    spawn_timer = 0
                
                obstacle_timer += 1
                if obstacle_timer > 90 / difficulty:
                    obstacle_type = random.choice(['mine', 'jellyfish', 'coral'])
                    y_pos = random.randint(25, SCREEN_HEIGHT - 50)
                    obstacles.append(Obstacle(SCREEN_WIDTH, y_pos, obstacle_type))
                    obstacle_timer = 0
                
                for collectible in collectibles[:]:
                    collectible.update(game_speed)
                    if submarine.get_rect().colliderect(collectible.get_rect()):
                        score += collectible.value
                        play_collect_sound()
                        collectibles.remove(collectible)
                    elif collectible.is_off_screen():
                        collectibles.remove(collectible)
                
                for obstacle in obstacles[:]:
                    obstacle.update(game_speed)
                    if submarine.get_rect().colliderect(obstacle.get_rect()):
                        play_collision_sound()
                        game_state = "gameover"
                        if score > high_score:
                            high_score = score
                    if obstacle.is_off_screen():
                        obstacles.remove(obstacle)
                
                difficulty_timer += 1
                if difficulty_timer > 600:
                    difficulty += 0.1
                    game_speed += 0.2
                    difficulty_timer = 0
            
            draw_background(background_offset)
            for collectible in collectibles:
                collectible.draw(screen)
            for obstacle in obstacles:
                obstacle.draw(screen)
            submarine.draw(screen)
            
            score_text = font_small.render(f"Score: {score}", True, YELLOW)
            screen.blit(score_text, (10, 10))
            high_score_text = font_tiny.render(f"High Score: {high_score}", True, YELLOW)
            screen.blit(high_score_text, (10, 50))
            depth_text = font_tiny.render(f"Depth Level: {int(difficulty * 10)}", True, CYAN)
            screen.blit(depth_text, (SCREEN_WIDTH - 200, 10))
            
            if paused:
                draw_pause_screen()
        
        elif game_state == "gameover":
            draw_game_over_screen(score, high_score)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
