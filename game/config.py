# Window settings
WIDTH, HEIGHT = 1024, 600
CENTER = (WIDTH // 2, HEIGHT // 2)

# Circle settings
RADIUS = 120
ARC_LEVELS = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]  # Arc sizes per level
SPEED_LEVELS = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]  # Speed levels
MAX_LEVEL = len(ARC_LEVELS) - 1
SCORE_LEVEL_UP = 500  # Score needed to level up
MISS_CHECK_TIME = 0.5
DETERMINATION_TIME_MINUTES = 10

# Colors
BG_COLOR = (30, 30, 30)
CIRCLE_COLOR = (255, 255, 255)
ARC_COLOR = (255, 0, 0)
POINT_COLOR = (0, 255, 0)
TEXT_COLOR = (255, 255, 255)

# Gameplay settings
HIT_THRESHOLD = 5  # Number of hits to level up
ACCURACY_THRESHOLD = 0.8  # 80% success rate to level up
