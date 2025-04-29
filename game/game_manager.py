from config import ARC_LEVELS, SPEED_LEVELS, SCORE_LEVEL_UP, MAX_LEVEL, DETERMINATION_TIME_MINUTES
from circle import Circle
from utils import get_accuracy_level
import time

class GameManager:
    def __init__(self):
        """Initialize game state with multiple circles."""
        self.circles = [
            Circle(-300, 0, 0),  # Controlled by "1"
            Circle(0, 0, 1),     # Controlled by "2"
            Circle(300, 0, 2)    # Controlled by "3"
        ]
        self.level = 0

        # Level Determination Phase
        self.determination_phase = True
        self.determination_start_time = time.time()
        self.determination_level_logs = []  # Store performance at each trial
        self.current_level_performance = []  # Store mini samples per level
        self.internal_hits = 0
        self.internal_misses = 0

        # Record last total misses (previous 10 seconds), it is used to calculate missed arc as a mistake
        self.last_total_misses = 0

        # Global performance tracking (never reset)
        self.global_performance_log = []

        # Timing inside each level trial
        self.last_performance_record_time = time.time()
        self.performance_record_interval = 10  # seconds

        # Record last good level
        self.last_good_level = 0

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
            self.internal_hits += 1  # INTERNAL TRACKING
            circle.show_feedback(success=True)
        else:
            circle.misses += 1
            self.internal_misses += 1  # INTERNAL TRACKING
            circle.show_feedback(success=False)

        circle.reposition_arc()

    def get_total_score(self):
        """Return the sum of all individual circle scores."""
        return sum(circle.score for circle in self.circles)

    def get_total_hits(self):
        """Return total hits across all circles (for UI)."""
        return sum(circle.hits for circle in self.circles)

    def get_total_misses(self):
        """Return total misses across all circles (for UI)."""
        return sum(circle.misses for circle in self.circles)

    def check_level_up(self):
        """Handle level updates based on internal performance (during determination phase)."""

        # Phase 2 (After Determination) -> just skip
        if not self.determination_phase:
            return

        current_time = time.time()

        # 1- Record mini performance every X seconds
        if current_time - self.last_performance_record_time >= self.performance_record_interval:
            self.record_mini_performance()
            self.last_performance_record_time = current_time

        # 2- Check if determination phase ended by timeout
        if current_time - self.determination_start_time >= DETERMINATION_TIME_MINUTES * 60:
            self.end_determination_phase()
            return

        # 3- Check if need to evaluate current level
        # For now: Assume evaluate after a fixed trial time per level
        TRIAL_DURATION = 60  # seconds for each level trial
        if current_time - self.determination_start_time >= TRIAL_DURATION * (self.level + 1):
            self.evaluate_level_performance()

    def record_mini_performance(self):
        """Record small period success ratio."""
        self.internal_misses = self.get_total_misses() - self.last_total_misses
        self.last_total_misses = self.get_total_misses()

        total = self.internal_hits + self.internal_misses
        if total == 0:
            success_ratio = 0
        else:
            success_ratio = self.internal_hits / total
        self.current_level_performance.append(success_ratio)

        # Save globally too
        self.global_performance_log.append({
            "level": self.level,
            "success_ratio": self.get_total_hits() / (self.get_total_hits() + self.get_total_misses())
        })

        # Reset mini counters for next record
        self.internal_hits = 0
        self.internal_misses = 0

    def evaluate_level_performance(self):
        """Evaluate whether to upgrade/downgrade."""
        if not self.current_level_performance:
            return  # Avoid division by zero

        avg_success = sum(self.current_level_performance) / len(self.current_level_performance)
        self.determination_level_logs.append({
            "level": self.level,
            "success_ratios": self.current_level_performance.copy(),
            "average_success": avg_success
        })

        # Upgrade/Downgrade decision
        SUCCESS_THRESHOLD = 0.60  # 60% success considered "good"
        if avg_success >= SUCCESS_THRESHOLD:
            self.last_good_level = self.level
            self.level += 1
            self.increase_speed()
        else:
            self.level = self.last_good_level
            self.end_determination_phase()

        # Reset level tracking
        print("performance:", self.current_level_performance)
        self.current_level_performance.clear()
        # self.current_level_performance = [0]
        self.internal_hits = 0
        self.internal_misses = 0

    def increase_speed(self):
        """Increase only the speed, keeping arc size constant."""
        if self.level <= MAX_LEVEL:
            for circle in self.circles:
                circle.speed = SPEED_LEVELS[self.level]
                # arc_length remains constant after starting!

    def end_determination_phase(self):
        """End level determination and lock experiment level."""
        self.determination_phase = False
        print(f"Level determination ended at level {self.level}")
