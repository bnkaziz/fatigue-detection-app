from config import ARC_LEVELS, SPEED_LEVELS, SCORE_LEVEL_UP, MAX_LEVEL
from circle import Circle
from utils import get_accuracy_level

class GameManager:
    def __init__(self):
        """Initialize game state with multiple circles."""
        self.circles = [
            Circle(-300, 0, 0),  # Controlled by "1"
            Circle(0, 0, 1),  # Controlled by "2"
            Circle(300, 0, 2)  # Controlled by "3"
        ]
        self.level = 0

    def update_circles(self):
        """Update all circles."""
        for circle in self.circles:
            circle.update()

    def check_hit(self, circle_index):
        """Check if a specific circle was hit correctly."""
        circle = self.circles[circle_index]
        success = circle.check_hit()

        if success:
            _, accuracy_score = get_accuracy_level(circle.angle, circle.arc_start, circle.arc_length)
            circle.score += (accuracy_score + self.level) * 10
            circle.hits += 1
            circle.show_feedback(success=True)
        else:
            circle.misses += 1  # Count a miss if hit key but not in arc
            circle.show_feedback(success=False)

        circle.reposition_arc()

    def get_total_score(self):
        """Return the sum of all individual circle scores."""
        return sum(circle.score for circle in self.circles)

    def get_total_hits(self):
        """Return total hits across all circles."""
        return sum(circle.hits for circle in self.circles)

    def get_total_misses(self):
        """Return total misses across all circles."""
        return sum(circle.misses for circle in self.circles)

    def check_level_up(self):
        """Upgrade level if total score exceeds threshold."""
        if self.get_total_score() >= SCORE_LEVEL_UP * (self.level + 1) and self.level < MAX_LEVEL:
            self.level += 1
            for circle in self.circles:
                circle.arc_length = ARC_LEVELS[self.level]
                circle.speed = SPEED_LEVELS[self.level]
