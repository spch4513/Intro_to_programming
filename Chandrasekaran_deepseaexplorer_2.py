import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌊 Deep Sea Explorer - Ethical Edition v3.3")

# Colors
DARK_BLUE = (10, 20, 50)
LIGHT_BLUE = (50, 100, 150)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 100)
ORANGE = (255, 140, 0)
PURPLE = (150, 50, 200)
GRAY = (100, 100, 100)

# Game settings
FPS = 60
GRAVITY = 0.3
JUMP_STRENGTH = -6

# Exponential difficulty settings
BASE_SPEED = 3
DIFFICULTY_MULTIPLIER = 1.02
MAX_SPEED = 15
BASE_SPAWN_RATE = 0.02
SPAWN_MULTIPLIER = 1.015

# ETHICAL FEATURE 1: Fatigue System (Negative Disengagement)
FATIGUE_THRESHOLD = 90  # seconds before fatigue warnings
FATIGUE_SEVERE = 180  # seconds before severe effects
EYE_STRAIN_BLINK_INTERVAL = 120  # Remind to blink every 2 minutes

# ETHICAL FEATURE 2: Skill Progression & Achievements (Positive Engagement)
ACHIEVEMENTS = {
    'first_treasure': {'name': 'First Treasure!', 'desc': 'Collected your first treasure chest', 'unlocked': False},
    'survivor_30': {'name': '30 Second Survivor', 'desc': 'Survived for 30 seconds', 'unlocked': False},
    'survivor_60': {'name': 'Deep Sea Veteran', 'desc': 'Survived for 60 seconds', 'unlocked': False},
    'score_100': {'name': 'Century Collector', 'desc': 'Reached 100 points', 'unlocked': False},
    'score_500': {'name': 'Ocean Master', 'desc': 'Reached 500 points', 'unlocked': False},
}

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)
font_tiny = pygame.font.Font(None, 18)

class Submarine:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.width = 60
        self.height = 30
        
    def jump(self):
        self.velocity = JUMP_STRENGTH
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.velocity = 0
    
    def draw(self, surface):
        pygame.draw.ellipse(surface, YELLOW, (self.x, self.y, self.width, self.height))
        pygame.draw.circle(surface, LIGHT_BLUE, (self.x + 15, self.y + 15), 8)
        pygame.draw.rect(surface, ORANGE, (self.x + 50, self.y + 10, 15, 10))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Collectible:
    def __init__(self, x, y, type_):
        self.x = x
        self.y = y
        self.type = type_
        self.collected = False
        
        if type_ == 'pearl':
            self.value = 10
            self.color = WHITE
            self.size = 15
        elif type_ == 'coin':
            self.value = 5
            self.color = YELLOW
            self.size = 12
        else:  # treasure
            self.value = 50
            self.color = ORANGE
            self.size = 20
    
    def update(self, speed):
        self.x -= speed
    
    def draw(self, surface):
        if not self.collected:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
            if self.type == 'treasure':
                pygame.draw.rect(surface, YELLOW, (self.x - 10, self.y - 5, 20, 10))
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, 
                          self.size * 2, self.size * 2)

class Obstacle:
    def __init__(self, x, y, type_):
        self.x = x
        self.y = y
        self.type = type_
        
        if type_ == 'mine':
            self.color = RED
            self.size = 25
        elif type_ == 'jellyfish':
            self.color = PURPLE
            self.size = 30
        else:  # coral
            self.color = GREEN
            self.size = 35
    
    def update(self, speed):
        self.x -= speed
    
    def draw(self, surface):
        if self.type == 'mine':
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                x_end = self.x + math.cos(rad) * (self.size + 10)
                y_end = self.y + math.sin(rad) * (self.size + 10)
                pygame.draw.line(surface, self.color, (self.x, self.y), (x_end, y_end), 3)
        elif self.type == 'jellyfish':
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
            for i in range(5):
                pygame.draw.line(surface, self.color, 
                               (self.x - 20 + i*10, self.y + self.size),
                               (self.x - 20 + i*10, self.y + self.size + 20), 2)
        else:  # coral
            pygame.draw.polygon(surface, self.color, [
                (self.x, self.y + self.size),
                (self.x - 15, self.y),
                (self.x, self.y - self.size),
                (self.x + 15, self.y)
            ])
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size,
                          self.size * 2, self.size * 2)

# ETHICAL FEATURE FUNCTIONS

def check_fatigue_level(time_elapsed):
    """
    NEGATIVE DISENGAGEMENT FEATURE: Calculates fatigue level
    Returns: 'none', 'mild', 'moderate', 'severe'
    """
    if time_elapsed < FATIGUE_THRESHOLD:
        return 'none'
    elif time_elapsed < FATIGUE_THRESHOLD + 30:
        return 'mild'
    elif time_elapsed < FATIGUE_SEVERE:
        return 'moderate'
    else:
        return 'severe'

def get_fatigue_message(fatigue_level):
    """
    NEGATIVE DISENGAGEMENT FEATURE: Returns appropriate warning message
    """
    messages = {
        'mild': '⚠️ You\'ve been playing for a while. Consider taking a break soon.',
        'moderate': '⚠️ Eye strain alert! Take a break and rest your eyes.',
        'severe': '🛑 FATIGUE WARNING: You\'ve been playing for 3+ minutes. Time to stop!'
    }
    return messages.get(fatigue_level, '')

def apply_fatigue_effects(submarine, fatigue_level):
    """
    NEGATIVE DISENGAGEMENT FEATURE: Applies visual/gameplay effects based on fatigue
    Makes game less enjoyable to encourage breaks
    """
    effects = {
        'reaction_delay': 0,
        'visual_blur': False,
        'control_sluggish': False
    }
    
    if fatigue_level == 'moderate':
        effects['visual_blur'] = True
    elif fatigue_level == 'severe':
        effects['visual_blur'] = True
        effects['control_sluggish'] = True
        effects['reaction_delay'] = 0.2
    
    return effects

def check_achievements(score, time_elapsed, treasure_collected, achievements):
    """
    POSITIVE ENGAGEMENT FEATURE: Checks and unlocks achievements
    Returns list of newly unlocked achievements
    """
    newly_unlocked = []
    
    if treasure_collected and not achievements['first_treasure']['unlocked']:
        achievements['first_treasure']['unlocked'] = True
        newly_unlocked.append('first_treasure')
    
    if time_elapsed >= 30 and not achievements['survivor_30']['unlocked']:
        achievements['survivor_30']['unlocked'] = True
        newly_unlocked.append('survivor_30')
    
    if time_elapsed >= 60 and not achievements['survivor_60']['unlocked']:
        achievements['survivor_60']['unlocked'] = True
        newly_unlocked.append('survivor_60')
    
    if score >= 100 and not achievements['score_100']['unlocked']:
        achievements['score_100']['unlocked'] = True
        newly_unlocked.append('score_100')
    
    if score >= 500 and not achievements['score_500']['unlocked']:
        achievements['score_500']['unlocked'] = True
        newly_unlocked.append('score_500')
    
    return newly_unlocked

def calculate_skill_level(score, time_elapsed):
    """
    POSITIVE ENGAGEMENT FEATURE: Calculates player skill rating
    Encourages mastery and improvement
    """
    if time_elapsed == 0:
        return "Beginner", 0
    
    score_per_second = score / time_elapsed
    
    if score_per_second < 2:
        return "Novice Diver", 1
    elif score_per_second < 4:
        return "Skilled Navigator", 2
    elif score_per_second < 6:
        return "Expert Explorer", 3
    elif score_per_second < 8:
        return "Master of the Deep", 4
    else:
        return "Legendary Ocean Lord", 5

def draw_achievement_notification(surface, achievement_key, achievements, alpha=255):
    """
    POSITIVE ENGAGEMENT FEATURE: Draws achievement unlock notification
    """
    achievement = achievements[achievement_key]
    
    notif_width = 350
    notif_height = 80
    notif_x = WIDTH - notif_width - 20
    notif_y = 120
    
    # Semi-transparent background
    notif_surface = pygame.Surface((notif_width, notif_height))
    notif_surface.set_alpha(alpha)
    notif_surface.fill((30, 30, 30))
    pygame.draw.rect(notif_surface, YELLOW, (0, 0, notif_width, notif_height), 3)
    surface.blit(notif_surface, (notif_x, notif_y))
    
    # Achievement text
    achievement_text = font_small.render("🏆 ACHIEVEMENT UNLOCKED!", True, YELLOW)
    surface.blit(achievement_text, (notif_x + 10, notif_y + 10))
    
    name_text = font_medium.render(achievement['name'], True, WHITE)
    surface.blit(name_text, (notif_x + 10, notif_y + 35))

def draw_fatigue_overlay(surface, fatigue_level, time_elapsed):
    """
    NEGATIVE DISENGAGEMENT FEATURE: Draws fatigue warnings and visual effects
    """
    if fatigue_level == 'none':
        return
    
    # Warning message at top
    message = get_fatigue_message(fatigue_level)
    color = ORANGE if fatigue_level == 'mild' else RED
    
    warning_text = font_small.render(message, True, color)
    text_rect = warning_text.get_rect(center=(WIDTH//2, 30))
    
    # Background for text
    bg_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10)
    pygame.draw.rect(surface, (0, 0, 0), bg_rect)
    pygame.draw.rect(surface, color, bg_rect, 2)
    surface.blit(warning_text, text_rect)
    
    # Visual blur effect for severe fatigue
    if fatigue_level in ['moderate', 'severe']:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(30 if fatigue_level == 'moderate' else 60)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
    
    # Eye strain reminder
    if int(time_elapsed) % EYE_STRAIN_BLINK_INTERVAL == 0 and time_elapsed > 0:
        blink_text = font_small.render("👁️ Remember to blink!", True, LIGHT_BLUE)
        surface.blit(blink_text, (WIDTH//2 - blink_text.get_width()//2, 60))

def calculate_difficulty(time_elapsed):
    """Calculate exponential difficulty multiplier based on time"""
    return math.pow(DIFFICULTY_MULTIPLIER, time_elapsed)

def calculate_speed(time_elapsed):
    """Calculate current game speed (exponential growth with cap)"""
    speed = BASE_SPEED * calculate_difficulty(time_elapsed)
    return min(speed, MAX_SPEED)

def calculate_spawn_rate(time_elapsed):
    """Calculate spawn rate (exponential growth)"""
    return BASE_SPAWN_RATE * math.pow(SPAWN_MULTIPLIER, time_elapsed)

def draw_background(surface, scroll):
    surface.fill(DARK_BLUE)
    
    for i in range(20):
        x = (i * 50 + scroll) % WIDTH
        y = (i * 80) % HEIGHT
        pygame.draw.circle(surface, LIGHT_BLUE, (x, y), 5, 1)

def draw_hud(surface, score, high_score, time_elapsed, current_speed, difficulty_mult, skill_level, skill_rank):
    """Draw HUD with score, time, difficulty, and skill level"""
    # Score
    score_text = font_medium.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))
    
    # High score
    high_score_text = font_small.render(f"Best: {high_score}", True, YELLOW)
    surface.blit(high_score_text, (10, 50))
    
    # Time survived
    time_text = font_small.render(f"Time: {int(time_elapsed)}s", True, WHITE)
    surface.blit(time_text, (10, 80))
    
    # Skill level (POSITIVE ENGAGEMENT)
    skill_text = font_small.render(f"Skill: {skill_level}", True, GREEN)
    surface.blit(skill_text, (10, 110))
    
    # Skill stars
    for i in range(skill_rank):
        pygame.draw.polygon(surface, YELLOW, [
            (10 + i*20 + 10, 135),
            (10 + i*20 + 12, 140),
            (10 + i*20 + 18, 140),
            (10 + i*20 + 14, 143),
            (10 + i*20 + 16, 148),
            (10 + i*20 + 10, 145),
            (10 + i*20 + 4, 148),
            (10 + i*20 + 6, 143),
            (10 + i*20 + 2, 140),
            (10 + i*20 + 8, 140)
        ])
    
    # Speed indicator
    speed_text = font_small.render(f"Speed: {current_speed:.1f}x", True, ORANGE)
    surface.blit(speed_text, (WIDTH - 150, 10))
    
    # Difficulty multiplier
    diff_color = RED if difficulty_mult > 3 else ORANGE if difficulty_mult > 2 else GREEN
    diff_text = font_small.render(f"Difficulty: {difficulty_mult:.2f}x", True, diff_color)
    surface.blit(diff_text, (WIDTH - 200, 40))
    
    # Difficulty bar
    bar_width = 150
    bar_height = 10
    bar_x = WIDTH - bar_width - 10
    bar_y = 70
    pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
    fill_width = min(bar_width, int((difficulty_mult - 1) * bar_width / 5))
    pygame.draw.rect(surface, diff_color, (bar_x, bar_y, fill_width, bar_height))

def draw_start_screen(surface):
    surface.fill(DARK_BLUE)
    
    title = font_large.render("🌊 DEEP SEA EXPLORER 🌊", True, WHITE)
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 80))
    
    subtitle = font_medium.render("Ethical Gaming Edition v3.3", True, ORANGE)
    surface.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 130))
    
    instructions = [
        "Controls: SPACE/UP - Rise | P - Pause",
        "",
        "Collect: Pearls (10) | Coins (5) | Treasure (50)",
        "Avoid: Mines | Jellyfish | Coral",
        "",
        "🎯 NEW ETHICAL FEATURES:",
        "✅ Achievement System - Unlock rewards!",
        "✅ Skill Rating - Track your mastery",
        "⚠️ Fatigue Warnings - Stay healthy",
        "⚠️ Eye Strain Reminders - Protect your vision",
        "",
        "Press SPACE to start"
    ]
    
    y_offset = 190
    for line in instructions:
        color = WHITE
        if "NEW ETHICAL FEATURES:" in line:
            color = YELLOW
        elif line.startswith("✅"):
            color = GREEN
        elif line.startswith("⚠️"):
            color = ORANGE
        
        text = font_small.render(line, True, color)
        surface.blit(text, (WIDTH//2 - text.get_width()//2, y_offset))
        y_offset += 28

def draw_game_over_screen(surface, score, high_score, time_survived, skill_level, achievements):
    surface.fill(DARK_BLUE)
    
    game_over = font_large.render("GAME OVER", True, RED)
    surface.blit(game_over, (WIDTH//2 - game_over.get_width()//2, 100))
    
    score_text = font_medium.render(f"Final Score: {score}", True, WHITE)
    surface.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 170))
    
    time_text = font_small.render(f"Survived: {int(time_survived)} seconds", True, YELLOW)
    surface.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 210))
    
    skill_text = font_small.render(f"Final Skill Level: {skill_level}", True, GREEN)
    surface.blit(skill_text, (WIDTH//2 - skill_text.get_width()//2, 240))
    
    if score >= high_score:
        new_record = font_medium.render("🏆 NEW HIGH SCORE! 🏆", True, YELLOW)
        surface.blit(new_record, (WIDTH//2 - new_record.get_width()//2, 280))
    else:
        high_score_text = font_small.render(f"High Score: {high_score}", True, WHITE)
        surface.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, 280))
    
    # Show unlocked achievements
    unlocked_count = sum(1 for a in achievements.values() if a['unlocked'])
    achievement_text = font_small.render(f"Achievements: {unlocked_count}/{len(achievements)}", True, YELLOW)
    surface.blit(achievement_text, (WIDTH//2 - achievement_text.get_width()//2, 320))
    
    restart = font_small.render("Press SPACE to play again", True, WHITE)
    surface.blit(restart, (WIDTH//2 - restart.get_width()//2, 380))

def draw_pause_screen(surface, score, time_elapsed, skill_level):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))
    
    pause_text = font_large.render("PAUSED", True, WHITE)
    surface.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 80))
    
    score_text = font_medium.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
    
    time_text = font_small.render(f"Time: {int(time_elapsed)}s", True, WHITE)
    surface.blit(time_text, (WIDTH//2 - time_text.get_width()//2, HEIGHT//2 + 20))
    
    skill_text = font_small.render(f"Skill: {skill_level}", True, GREEN)
    surface.blit(skill_text, (WIDTH//2 - skill_text.get_width()//2, HEIGHT//2 + 50))
    
    health_text = font_small.render("💚 Great time for a stretch break!", True, LIGHT_BLUE)
    surface.blit(health_text, (WIDTH//2 - health_text.get_width()//2, HEIGHT//2 + 90))
    
    continue_text = font_small.render("Press P to continue", True, WHITE)
    surface.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 120))

# Main game loop
def main():
    clock = pygame.time.Clock()
    running = True
    
    # Game state
    state = 'start'
    
    # Game objects
    submarine = Submarine()
    collectibles = []
    obstacles = []
    
    # Game variables
    score = 0
    high_score = 0
    scroll = 0
    time_elapsed = 0
    frame_count = 0
    treasure_collected = False
    
    # Ethical feature tracking
    achievements = {key: {'name': val['name'], 'desc': val['desc'], 'unlocked': False} 
                   for key, val in ACHIEVEMENTS.items()}
    achievement_notifications = []  # List of (achievement_key, time_shown)
    skill_level = "Beginner"
    skill_rank = 0
    
    while running:
        dt = clock.tick(FPS) / 1000.0
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if state == 'start':
                    if event.key in [pygame.K_SPACE, pygame.K_UP]:
                        state = 'playing'
                        submarine = Submarine()
                        collectibles = []
                        obstacles = []
                        score = 0
                        scroll = 0
                        time_elapsed = 0
                        frame_count = 0
                        treasure_collected = False
                        achievement_notifications = []
                
                elif state == 'playing':
                    if event.key in [pygame.K_SPACE, pygame.K_UP]:
                        submarine.jump()
                    if event.key == pygame.K_p:
                        state = 'paused'
                
                elif state == 'paused':
                    if event.key == pygame.K_p:
                        state = 'playing'
                
                elif state == 'gameover':
                    if event.key == pygame.K_SPACE:
                        state = 'start'
        
        # Game logic
        if state == 'playing':
            time_elapsed += dt
            frame_count += 1
            
            # Calculate current difficulty
            difficulty_mult = calculate_difficulty(time_elapsed)
            current_speed = calculate_speed(time_elapsed)
            current_spawn_rate = calculate_spawn_rate(time_elapsed)
            
            # Check fatigue level
            fatigue_level = check_fatigue_level(time_elapsed)
            
            # Update submarine
            submarine.update()
            
            # Scroll background
            scroll += current_speed
            
            # Spawn collectibles
            if random.random() < current_spawn_rate * 0.6:
                y = random.randint(50, HEIGHT - 50)
                type_ = random.choice(['pearl', 'pearl', 'coin', 'coin', 'coin', 'treasure'])
                collectibles.append(Collectible(WIDTH, y, type_))
            
            # Spawn obstacles
            if random.random() < current_spawn_rate * difficulty_mult * 0.4:
                y = random.randint(50, HEIGHT - 50)
                type_ = random.choice(['mine', 'jellyfish', 'coral'])
                obstacles.append(Obstacle(WIDTH, y, type_))
            
            # Update collectibles
            for collectible in collectibles[:]:
                collectible.update(current_speed)
                if collectible.x < -50:
                    collectibles.remove(collectible)
                elif not collectible.collected and submarine.get_rect().colliderect(collectible.get_rect()):
                    score += collectible.value
                    if collectible.type == 'treasure':
                        treasure_collected = True
                    collectible.collected = True
                    collectibles.remove(collectible)
            
            # Update obstacles
            for obstacle in obstacles[:]:
                obstacle.update(current_speed)
                if obstacle.x < -50:
                    obstacles.remove(obstacle)
                elif submarine.get_rect().colliderect(obstacle.get_rect()):
                    state = 'gameover'
                    if score > high_score:
                        high_score = score
            
            # Check achievements
            newly_unlocked = check_achievements(score, time_elapsed, treasure_collected, achievements)
            for achievement_key in newly_unlocked:
                achievement_notifications.append((achievement_key, time_elapsed))
            
            # Calculate skill level
            skill_level, skill_rank = calculate_skill_level(score, time_elapsed)
        
        # Drawing
        if state == 'start':
            draw_start_screen(screen)
        
        elif state == 'playing':
            draw_background(screen, int(scroll))
            
            # Draw game objects
            for collectible in collectibles:
                collectible.draw(screen)
            for obstacle in obstacles:
                obstacle.draw(screen)
            submarine.draw(screen)
            
            # Draw HUD
            draw_hud(screen, score, high_score, time_elapsed, 
                    current_speed / BASE_SPEED, difficulty_mult, skill_level, skill_rank)
            
            # Draw fatigue overlay (NEGATIVE DISENGAGEMENT)
            draw_fatigue_overlay(screen, fatigue_level, time_elapsed)
            
            # Draw achievement notifications (POSITIVE ENGAGEMENT)
            for notif in achievement_notifications[:]:
                achievement_key, unlock_time = notif
                time_shown = time_elapsed - unlock_time
                if time_shown < 3:  # Show for 3 seconds
                    alpha = 255 if time_shown < 2.5 else int(255 * (3 - time_shown) / 0.5)
                    draw_achievement_notification(screen, achievement_key, achievements, alpha)
                else:
                    achievement_notifications.remove(notif)
        
        elif state == 'paused':
            draw_background(screen, int(scroll))
            for collectible in collectibles:
                collectible.draw(screen)
            for obstacle in obstacles:
                obstacle.draw(screen)
            submarine.draw(screen)
            draw_pause_screen(screen, score, time_elapsed, skill_level)
        
        elif state == 'gameover':
            draw_game_over_screen(screen, score, high_score, time_elapsed, skill_level, achievements)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
