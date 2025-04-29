class SessionManager:
    """Store all user/session data."""
    def __init__(self):
        self.user_info = {}
        self.device_info = {}
        self.performance_data = []
        self.game_process = None