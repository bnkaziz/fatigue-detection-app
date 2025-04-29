import math
import random
from config import ARC_LEVELS

def degrees_to_radians(degrees):
    """Convert degrees to radians."""
    return math.radians(degrees)

def calculate_arc_center(start_angle, arc_length):
    """Calculate the center of the arc for accuracy scoring."""
    return start_angle + (arc_length / 2)

def get_accuracy_level(angle, arc_start, arc_length):
    """
    Determines the accuracy level based on how close the point is to 
    the center of the arc.
    """
    center_of_arc = calculate_arc_center(arc_start, arc_length)
    distance = abs(angle - center_of_arc)

    if distance < 5:  # Perfect hit
        return "Perfect", 3
    elif distance < 15:  # Good hit
        return "Good", 2
    else:  # Barely in
        return "Barely", 1

def randomize_arc(arc_length):
    """Generate a new random arc position while keeping the same arc length."""
    return random.randint(0, 360 - arc_length)
