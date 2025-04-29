import pygame
import math
import random
from config import CENTER, RADIUS, ARC_LEVELS, SPEED_LEVELS, MISS_CHECK_TIME
from utils import degrees_to_radians, randomize_arc

class Circle:
    def __init__(self, offset_x=0, offset_y=0, index=0):
        """Initialize a circle with a random arc and rotating object."""
        self.center = (CENTER[0] + offset_x, CENTER[1] + offset_y)
        self.arc_length = ARC_LEVELS[0]  # Start at level 0
        self.speed = SPEED_LEVELS[0]
        self.angle = random.randint(0, 359)  # Start at a random position
        self.index = index  # Identifies which key controls this circle
        self.score = 0  # Individual score
        self.hits = 0
        self.misses = 0
        self.feedback_color = None  # No color by default
        self.feedback_timer = 0  # Timer for how long the feedback should show
        self.was_inside_arc = False  # Track if the rotating object was inside
        self.reposition_arc()

    def reposition_arc(self):
        """Randomly reposition arc while keeping its size."""
        self.arc_start = randomize_arc(self.arc_length)
        self.arc_end = self.arc_start + self.arc_length

    def update(self):
        """Rotate the object and check for misses when leaving the arc."""
        self.angle = (self.angle + self.speed) % 360

        # Miss detection: If it was inside and now it's outside
        in_arc = self.arc_start <= self.angle <= self.arc_end

        if self.was_inside_arc and not in_arc:
            self.misses += 1
            self.show_feedback(success=False)
            self.reposition_arc()

        self.was_inside_arc = in_arc
        # Update feedback timer
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
        else:
            self.feedback_color = None

    def draw(self, screen, font):
        """Draw the circle, arc, rotating point, and debug info."""
        pygame.draw.circle(screen, (255, 255, 255), self.center, RADIUS, 10)
        pygame.draw.arc(screen, (255, 0, 0), 
                        (self.center[0] - RADIUS, self.center[1] - RADIUS, RADIUS * 2, RADIUS * 2),
                        degrees_to_radians(self.arc_start), degrees_to_radians(self.arc_end), 10)
    
        # Feedback circle (inside the main circle)
        if self.feedback_color:
            pygame.draw.circle(screen, self.feedback_color, self.center, RADIUS - 30)


        # Moving point
        rad_angle = degrees_to_radians(self.angle)
        point_x = self.center[0] + RADIUS * math.cos(rad_angle)
        point_y = self.center[1] - RADIUS * math.sin(rad_angle)
        pygame.draw.circle(screen, (0, 255, 0), (int(point_x), int(point_y)), 10)

        # Display individual stats for debugging
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        hits_text = font.render(f"Hits: {self.hits}", True, (0, 255, 0))
        misses_text = font.render(f"Misses: {self.misses}", True, (255, 0, 0))
        screen.blit(score_text, (self.center[0] - 20, self.center[1] + RADIUS + 20))
        screen.blit(hits_text, (self.center[0] - 20, self.center[1] + RADIUS + 40))
        screen.blit(misses_text, (self.center[0] - 20, self.center[1] + RADIUS + 60))

    def show_feedback(self, success):
        """Set the feedback color and timer based on hit or miss."""
        self.feedback_color = (0, 255, 0) if success else (255, 0, 0)
        self.feedback_timer = 6  # frames (adjust as needed, e.g., 0.5 seconds at 60 fps)


    def check_hit(self):
        """Returns True if the point is in the arc range."""
        if self.arc_start <= self.angle % 360 <= self.arc_end:
            self.was_inside_arc = False
            return True
        else:
            return False
