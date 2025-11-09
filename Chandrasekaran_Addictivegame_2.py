import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ethical Fruit Catcher")

# Colors (High contrast & colorblind-friendly)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (230, 25, 75)
GREEN = (60, 180, 75)
YELLOW = (255, 225, 25)
BLUE = (0, 130, 200)
ORANGE = (245, 130, 48)
PURPLE = (145, 30, 180)
CYAN = (70, 240, 240)

# Fonts
font_large = pygame.font.Font(None, 56)
font_medium = pygame.font.Font(None, 42)
font_small = pygame.font.Font(None, 32)

# Game variables
clock = pygame.time.Clock()
FPS = 60

# Player settings
player_width = 120
player_height = 30
player_speed = 8

# Fruit settings
fruit_size = 40
fruit_speed = 5

# Engagement period (60 seconds)
ENGAGEMENT_PERIOD = 60


# ========== FUNCTIONS (Called multiple times) ==========

def play_sound_effect(frequency, duration_ms):
    """Function 1: Play a simple beep sound"""
    try:
        # Create a simple beep
        sample_rate = 22050
        duration = duration_ms / 1000.0
        n_samples = int(round(duration * sample_rate))
        
        # Generate sine wave
        buf = []
        for i in range(n_samples):
            value = int(32767 * 0.3 * pygame.math.Vector2(1, 0).rotate(
                360.0 * frequency * i / sample_rate).x)
            buf.append((value, value))
        
        sound = pygame.sndarray.make_sound(buf)
        sound.play()
    except:
        pass  # Silently fail if sound doesn't work


def draw_text(text, font, color, x, y, center=True):
    """Function 2: Draw text on screen"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


def show_encouragement(message, game_state):
    """Function 3: Display encouragement message"""
    game_state['encouragement'] = message
    game_state['encouragement_time'] = time.time()


# ========== GAME CLASSES ==========

class Player:
    def __init__(self, width_size):
        self.width = width_size
        self.height = player_height
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 80
        self.speed = player_speed
        self.color = BLUE
    
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        elif direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 3)


class Fruit:
    def __init__(self, speed_multiplier=1.0):
        self.size = fruit_size
        self.x = random.randint(self.size, WIDTH - self.size)
        self.y = -self.size
        self.speed = fruit_speed * speed_multiplier
        self.colors = [RED, GREEN, YELLOW, ORANGE, PURPLE]
        self.color = random.choice(self.colors)
        self.emoji = random.choice(['🍎', '🍊', '🍋', '🍇', '🍓'])
    
    def move(self):
        self.y += self.speed
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size // 2)
        # Draw emoji
        emoji_surface = font_medium.render(self.emoji, True, WHITE)
        emoji_rect = emoji_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(emoji_surface, emoji_rect)
    
    def is_off_screen(self):
        return self.y > HEIGHT


# ========== GAME SCREENS ==========

def show_start_screen(game_state):
    """Display start screen with instructions"""
    screen.fill(BLACK)
    
    draw_text("🍎 ETHICAL FRUIT CATCHER 🍊", font_large, YELLOW, WIDTH // 2, 80)
    
    draw_text("HOW TO PLAY:", font_medium, WHITE, WIDTH // 2, 180)
    draw_text("← → Arrow keys to move basket", font_small, CYAN, WIDTH // 2, 230)
    draw_text("Catch falling fruits to score points!", font_small, CYAN, WIDTH // 2, 270)
    
    draw_text("⚠️ ETHICAL DESIGN:", font_medium, ORANGE, WIDTH // 2, 340)
    draw_text("After 60 seconds, you'll be asked to take a break", font_small, GREEN, WIDTH // 2, 390)
    
    draw_text("ACCESSIBILITY SETTINGS:", font_small, WHITE, WIDTH // 2, 460)
    draw_text(f"Basket Size: {game_state['basket_size'].upper()} (Press 1=Small, 2=Medium, 3=Large)", 
              font_small, CYAN, WIDTH // 2, 500)
    
    draw_text("Press SPACE to Start", font_medium, YELLOW, WIDTH // 2, 560)
    
    pygame.display.flip()


def show_break_prompt():
    """Display break prompt screen"""
    screen.fill(PURPLE)
    
    draw_text("⏰ TIME FOR A BREAK! ⏰", font_large, YELLOW, WIDTH // 2, 150)
    draw_text("You've been playing for 1 minute!", font_medium, WHITE, WIDTH // 2, 220)
    draw_text("Would you like to take a break?", font_medium, WHITE, WIDTH // 2, 280)
    
    draw_text("Press Y for YES (Take a Break)", font_small, GREEN, WIDTH // 2, 380)
    draw_text("Press N for NO (Continue - Answer Quiz First)", font_small, ORANGE, WIDTH // 2, 430)
    
    pygame.display.flip()


def show_quiz_screen():
    """Display quiz screen"""
    screen.fill(BLUE)
    
    draw_text("📝 QUICK QUIZ 📝", font_large, YELLOW, WIDTH // 2, 150)
    draw_text("To continue playing, answer this:", font_medium, WHITE, WIDTH // 2, 220)
    draw_text("How many MINUTES have you been playing?", font_medium, CYAN, WIDTH // 2, 280)
    draw_text("(Approximately)", font_small, WHITE, WIDTH // 2, 320)
    
    draw_text("Press 1 or 2 on your keyboard", font_small, GREEN, WIDTH // 2, 400)
    
    pygame.display.flip()


def show_game_over_screen(game_state):
    """Display game over screen with skills learned"""
    screen.fill(BLACK)
    
    draw_text("🎮 GAME OVER 🎮", font_large, RED, WIDTH // 2, 80)
    draw_text(f"Final Score: {game_state['score']}", font_large, YELLOW, WIDTH // 2, 150)
    draw_text(f"High Score: {game_state['high_score']}", font_medium, GREEN, WIDTH // 2, 200)
    
    draw_text("✨ SKILLS YOU PRACTICED ✨", font_medium, CYAN, WIDTH // 2, 280)
    draw_text("✓ Hand-eye coordination", font_small, WHITE, WIDTH // 2, 330)
    draw_text("✓ Quick reflexes", font_small, WHITE, WIDTH // 2, 365)
    draw_text("✓ Focus and concentration", font_small, WHITE, WIDTH // 2, 400)
    draw_text("✓ Decision making", font_small, WHITE, WIDTH // 2, 435)
    
    draw_text("Great job! 🌟", font_medium, YELLOW, WIDTH // 2, 490)
    draw_text("Press SPACE to Play Again or ESC to Quit", font_small, WHITE, WIDTH // 2, 550)
    
    pygame.display.flip()


# ========== MAIN GAME LOOP ==========

def main():
    # Game state dictionary
    game_state = {
        'score': 0,
        'high_score': 0,
        'time_played': 0,
        'start_time': 0,
        'basket_size': 'medium',  # small, medium, large
        'encouragement': '',
        'encouragement_time': 0,
        'fruits_caught': 0,
        'speed_multiplier': 1.0
    }
    
    # Game states
    current_screen = "start"  # start, playing, break_prompt, quiz, game_over
    
    # Player basket size options
    basket_sizes = {
        'small': 80,
        'medium': 120,
        'large': 160
    }
    
    running = True
    
    while running:
        clock.tick(FPS)
        
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # START SCREEN
            if current_screen == "start":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Initialize game
                        player = Player(basket_sizes[game_state['basket_size']])
                        fruits = []
                        game_state['score'] = 0
                        game_state['time_played'] = 0
                        game_state['start_time'] = time.time()
                        game_state['fruits_caught'] = 0
                        game_state['speed_multiplier'] = 1.0
                        current_screen = "playing"
                        play_sound_effect(600, 100)
                        show_encouragement("Let's catch some fruit! 🍎", game_state)
                    
                    # Accessibility: Change basket size
                    elif event.key == pygame.K_1:
                        game_state['basket_size'] = 'small'
                    elif event.key == pygame.K_2:
                        game_state['basket_size'] = 'medium'
                    elif event.key == pygame.K_3:
                        game_state['basket_size'] = 'large'
            
            # BREAK PROMPT SCREEN
            elif current_screen == "break_prompt":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        # Take a break
                        show_encouragement("Good choice! See you later! 👋", game_state)
                        play_sound_effect(800, 200)
                        current_screen = "game_over"
                    elif event.key == pygame.K_n:
                        # Continue with quiz
                        current_screen = "quiz"
            
            # QUIZ SCREEN
            elif current_screen == "quiz":
                if event.type == pygame.KEYDOWN:
                    correct_answer = 1  # They've played for 1 minute
                    
                    if event.key == pygame.K_1:
                        user_answer = 1
                    elif event.key == pygame.K_2:
                        user_answer = 2
                    else:
                        continue
                    
                    # Check answer
                    if user_answer == correct_answer:
                        # Correct! Continue playing with easier difficulty
                        show_encouragement("Correct! You're doing great! 🌟", game_state)
                        play_sound_effect(900, 200)
                        game_state['speed_multiplier'] = 0.6  # Make game easier
                        current_screen = "playing"
                    else:
                        # Wrong answer, time for a break
                        show_encouragement("Not quite! Time for a break! 😊", game_state)
                        play_sound_effect(400, 300)
                        current_screen = "game_over"
            
            # GAME OVER SCREEN
            elif current_screen == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        current_screen = "start"
                    elif event.key == pygame.K_ESCAPE:
                        running = False
        
        # GAME LOGIC - PLAYING STATE
        if current_screen == "playing":
            # Update time
            game_state['time_played'] = time.time() - game_state['start_time']
            
            # Check for engagement period (60 seconds)
            if game_state['time_played'] >= ENGAGEMENT_PERIOD:
                current_screen = "break_prompt"
                continue
            
            # Handle player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move("left")
            if keys[pygame.K_RIGHT]:
                player.move("right")
            
            # Spawn fruits
            if random.randint(1, 40) == 1:
                fruits.append(Fruit(game_state['speed_multiplier']))
            
            # Move and draw fruits
            for fruit in fruits[:]:
                fruit.move()
                
                # Check collision with player
                if (player.x < fruit.x < player.x + player.width and
                    player.y < fruit.y < player.y + player.height):
                    fruits.remove(fruit)
                    game_state['score'] += 10
                    game_state['fruits_caught'] += 1
                    play_sound_effect(700, 80)
                    
                    # Encouragement messages
                    if game_state['fruits_caught'] % 5 == 0:
                        show_encouragement("You're really getting it! 🎯", game_state)
                    
                    # Update high score discretely after engagement period
                    if game_state['time_played'] >= ENGAGEMENT_PERIOD:
                        if game_state['score'] > game_state['high_score']:
                            game_state['high_score'] = game_state['score']
                
                # Remove if off screen
                elif fruit.is_off_screen():
                    fruits.remove(fruit)
            
            # DRAW EVERYTHING
            screen.fill(BLACK)
            
            # Draw player
            player.draw()
            
            # Draw fruits
            for fruit in fruits:
                fruit.draw()
            
            # Draw score and time
            draw_text(f"Score: {game_state['score']}", font_medium, YELLOW, 100, 30, False)
            draw_text(f"High: {game_state['high_score']}", font_small, GREEN, 100, 70, False)
            draw_text(f"Time: {int(game_state['time_played'])}s", font_small, CYAN, 
                     WIDTH - 150, 30, False)
            
            # Draw encouragement message
            if game_state['encouragement'] and time.time() - game_state['encouragement_time'] < 2:
                draw_text(game_state['encouragement'], font_medium, YELLOW, WIDTH // 2, HEIGHT // 2)
            
            pygame.display.flip()
        
        # DRAW OTHER SCREENS
        elif current_screen == "start":
            show_start_screen(game_state)
        elif current_screen == "break_prompt":
            show_break_prompt()
        elif current_screen == "quiz":
            show_quiz_screen()
        elif current_screen == "game_over":
            show_game_over_screen(game_state)
    
    pygame.quit()


if __name__ == "__main__":
    main()