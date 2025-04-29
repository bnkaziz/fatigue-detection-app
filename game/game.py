import pygame
# import pygame.gfxdraw
import math
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 150
ARC_START_ANGLE = 45  # Degrees
ARC_END_ANGLE = 90  # Degrees
# ROTATION_SPEED = 7  # Degrees per frame
BG_COLOR = (30, 30, 30)
CIRCLE_COLOR = (255, 255, 255)
ARC_COLOR = (255, 0, 0)
POINT_COLOR = (0, 255, 0)
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER_COLOR = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)

# Speed and Arc Settings
speed_levels = [2, 3, 4, 5, 6, 7]
arc_lengths = [60, 55, 50, 45, 30, 20]
level = 0
speed_index = 0  # Default speed level index
arc_index = 0  # Default arc length index

# Initial arc position
ARC_START_ANGLE = 45
ARC_LENGTH = arc_lengths[level]
ARC_END_ANGLE = ARC_START_ANGLE + ARC_LENGTH

# Score & Statistics
score = 0
hits = 0
mistakes = 0
reaction_times = [0]
# reaction_time = 0
last_hit_time = None

# Button Positions
button_size = (50, 50)
buttons = {
    "level_up": pygame.Rect(650, 100, *button_size),
    "level_down": pygame.Rect(590, 100, *button_size),
    # "speed_up": pygame.Rect(650, 100, *button_size),
    # "speed_down": pygame.Rect(590, 100, *button_size),
    # "arc_up": pygame.Rect(650, 200, *button_size),
    # "arc_down": pygame.Rect(590, 200, *button_size),
    "arc_shift": pygame.Rect(620, 200, *button_size),
}

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Object Game")

# Game variables
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
angle = 0  # Starting angle
running = True

# Hit/Miss Animation Timer
animation_color = None
animation_end_time = 0

# Function to update arc position randomly while keeping the same length
def reposition_arc():
    global ARC_START_ANGLE, ARC_END_ANGLE
    ARC_START_ANGLE = random.randint(0, 360 - ARC_LENGTH)
    ARC_END_ANGLE = ARC_START_ANGLE + ARC_LENGTH

# Function to calculate accuracy level based on angle
def get_accuracy_level(angle):
    center_of_arc = (ARC_START_ANGLE + ARC_END_ANGLE) / 2
    distance_from_center = abs(angle - center_of_arc)

    if distance_from_center < 5:  # Perfect hit
        return "Perfect", 3
    elif distance_from_center < 15:  # Good hit
        return "Good", 2
    else:  # Barely in
        return "Barely", 1

clock = pygame.time.Clock()

while running:
    screen.fill(BG_COLOR)
    
    # Draw main circle
    pygame.draw.circle(screen, CIRCLE_COLOR, CENTER, RADIUS, 10)

    circle_color = animation_color if animation_color else BG_COLOR
    pygame.draw.circle(screen, circle_color, CENTER, RADIUS - 10)

    # Remove animation color after timeout
    if animation_color and time.time() > animation_end_time:
        animation_color = None

    # pygame.draw.rect(screen, CIRCLE_COLOR, (CENTER[0] - RADIUS, CENTER[1] - RADIUS, RADIUS * 2, RADIUS * 2), 2)
    
    pygame.draw.arc(screen, ARC_COLOR, (CENTER[0] - RADIUS, CENTER[1] - RADIUS, RADIUS * 2, RADIUS * 2),
                math.radians(ARC_START_ANGLE), math.radians(ARC_END_ANGLE), 10)

    
    # # Calculate start and end points of the arc span
    # arc_start_x = CENTER[0] + RADIUS * math.cos(start_rad)
    # arc_start_y = CENTER[1] - RADIUS * math.sin(start_rad)
    
    # arc_end_x = CENTER[0] + RADIUS * math.cos(end_rad)
    # arc_end_y = CENTER[1] - RADIUS * math.sin(end_rad)

    # Update rotating object's position
    rad_angle = math.radians(angle)
    point_x = CENTER[0] + RADIUS * math.cos(rad_angle)
    point_y = CENTER[1] - RADIUS * math.sin(rad_angle)
    
    # Draw moving point
    pygame.draw.circle(screen, POINT_COLOR, (int(point_x), int(point_y)), 10)
    
    # Check if the point is inside the target arc span
    in_target_zone = ARC_START_ANGLE <= angle % 360 <= ARC_END_ANGLE
    
    # Display status message
    if in_target_zone:
        text = font.render("IN TARGET ZONE!", True, (0, 255, 0))
        screen.blit(text, (WIDTH // 2 - 80, HEIGHT - 50))
    
    # Display Score and Stats
    stats_text = font.render(f"Score: {score} | Hits: {hits} | Misses: {mistakes} | Reaction: {(sum(reaction_times) / len(reaction_times)):.2f}s", True, TEXT_COLOR)
    screen.blit(stats_text, (20, 20))
    
    # Draw buttons
    for name, rect in buttons.items():
        color = BUTTON_HOVER_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=10)

        # Draw button labels
        label = ""
        if name == "level_up":
            label = "+"
        elif name == "level_down":
            label = "-"
        # if name == "speed_up":
        #     label = "+"
        # elif name == "speed_down":
        #     label = "-"
        # elif name == "arc_up":
        #     label = ">"
        # elif name == "arc_down":
        #     label = "<"
        elif name == "arc_shift":
            label = "<>"
        
        text = font.render(label, True, TEXT_COLOR)
        screen.blit(text, (rect.x + 15, rect.y + 10))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if buttons["level_up"].collidepoint(mouse_pos) and level < len(speed_levels) - 1:
                level += 1
                ARC_LENGTH = arc_lengths[level]
                reposition_arc()  # Update arc position
            elif buttons["level_down"].collidepoint(mouse_pos) and level > 0:
                level -= 1
                ARC_LENGTH = arc_lengths[level]
                reposition_arc()  # Update arc position
            # if buttons["speed_up"].collidepoint(mouse_pos) and speed_index < len(speed_levels) - 1:
            #     speed_index += 1
            # elif buttons["speed_down"].collidepoint(mouse_pos) and speed_index > 0:
            #     speed_index -= 1
            # elif buttons["arc_up"].collidepoint(mouse_pos) and arc_index < len(arc_lengths) - 1:
            #     arc_index += 1
            #     ARC_LENGTH = arc_lengths[arc_index]
            #     reposition_arc()  # Update arc position
            # elif buttons["arc_down"].collidepoint(mouse_pos) and arc_index > 0:
            #     arc_index -= 1
            #     ARC_LENGTH = arc_lengths[arc_index]
            #     reposition_arc()  # Update arc position
            elif buttons["arc_shift"].collidepoint(mouse_pos):
                reposition_arc()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if last_hit_time is not None:
                    reaction_times.append(time.time() - last_hit_time)
                    # reaction_time = sum(reaction_times) / len(reaction_times)
                last_hit_time = time.time()

                if in_target_zone:
                    hits += 1
                    accuracy_label, accuracy_score = get_accuracy_level(angle)
                    score += (accuracy_score + level) * 10
                    animation_color = (0, 255, 0)  # Green for hit
                    # print("HIT!")
                else:
                    mistakes += 1
                    animation_color = (255, 0, 0)  # Red for miss
                    # print("MISS!")
                
                animation_end_time = time.time() + 0.1
                reposition_arc()  # Update arc position
        

    # Update angle for rotation
    angle = (angle + speed_levels[level]) % 360

    # Refresh screen
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
