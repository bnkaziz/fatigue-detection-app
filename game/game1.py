import pygame
import math
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 150
BG_COLOR = (30, 30, 30)
CIRCLE_COLOR = (255, 255, 255)
ARC_COLOR = (255, 0, 0)
POINT_COLOR = (0, 255, 0)
TEXT_COLOR = (255, 255, 255)

# Speed and Arc Settings
speed_levels = [2, 3, 4, 5, 6, 7]
arc_lengths = [60, 55, 50, 45, 30, 20]
level = 0

# Score & Statistics
score = 0
hits = 0
mistakes = 0
reaction_times = [0]
last_hit_time = None

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Object Game")

# Game variables
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
angle = 0
running = True
animation_color = None
animation_end_time = 0

# Function to update arc position
def reposition_arc():
    global ARC_START_ANGLE, ARC_END_ANGLE
    ARC_START_ANGLE = random.randint(0, 360 - arc_lengths[level])
    ARC_END_ANGLE = ARC_START_ANGLE + arc_lengths[level]

def get_accuracy_level(angle):
    center_of_arc = (ARC_START_ANGLE + ARC_END_ANGLE) / 2
    distance_from_center = abs(angle - center_of_arc)
    if distance_from_center < 5:
        return 3  # Perfect hit
    elif distance_from_center < 15:
        return 2  # Good hit
    else:
        return 1  # Barely in

# Initial arc placement
reposition_arc()

while running:
    screen.fill(BG_COLOR)
    pygame.draw.circle(screen, CIRCLE_COLOR, CENTER, RADIUS, 10)
    circle_color = animation_color if animation_color else BG_COLOR
    pygame.draw.circle(screen, circle_color, CENTER, RADIUS - 10)
    
    if animation_color and time.time() > animation_end_time:
        animation_color = None
    
    pygame.draw.arc(screen, ARC_COLOR, (CENTER[0] - RADIUS, CENTER[1] - RADIUS, RADIUS * 2, RADIUS * 2),
                    math.radians(ARC_START_ANGLE), math.radians(ARC_END_ANGLE), 10)
    
    rad_angle = math.radians(angle)
    point_x = CENTER[0] + RADIUS * math.cos(rad_angle)
    point_y = CENTER[1] - RADIUS * math.sin(rad_angle)
    pygame.draw.circle(screen, POINT_COLOR, (int(point_x), int(point_y)), 10)
    
    in_target_zone = ARC_START_ANGLE <= angle % 360 <= ARC_END_ANGLE
    
    stats_text = font.render(f"Score: {score} | Hits: {hits} | Misses: {mistakes} | Reaction: {(sum(reaction_times) / len(reaction_times)):.2f}s", True, TEXT_COLOR)
    screen.blit(stats_text, (20, 20))

    level_text = font.render(f"Level: {level+1}", True, TEXT_COLOR)
    screen.blit(level_text, (WIDTH // 2 - 40, HEIGHT - 30))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if last_hit_time is not None:
                reaction_times.append(time.time() - last_hit_time)
            last_hit_time = time.time()
            
            if in_target_zone:
                hits += 1
                accuracy_score = get_accuracy_level(angle)
                score += (accuracy_score + level) * 10
                animation_color = (0, 255, 0)
            else:
                mistakes += 1
                animation_color = (255, 0, 0)
            
            animation_end_time = time.time() + 0.1
            reposition_arc()
            
            if hits >= 10 and (mistakes == 0 or hits / (hits + mistakes) >= 0.8) and level < len(speed_levels) - 1:
                level += 1
                hits, mistakes = 0, 0  # Reset for the next level

    angle = (angle + speed_levels[level]) % 360
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
