import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget

from components.session_manager import SessionManager

from pages.user_info_page import UserInfoPage
from pages.device_selection_page import DeviceSelectionPage
from pages.connection_schema_page import ConnectionSchemaPage
from pages.personality_test_page import PersonalityTestPage
from pages.state_test_page import StateTestPage
from pages.game_description_page import GameDescriptionPage
from pages.game_dashboard_page import GameDashboardPage

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize global session manager
        self.session = SessionManager()

        # Create pages
        self.user_info_page = UserInfoPage(self)
        self.device_selection_page = DeviceSelectionPage(self)
        self.connection_schema_page = ConnectionSchemaPage(self)
        self.personality_test_page = PersonalityTestPage(self)
        self.state_test_page = StateTestPage(self)
        self.game_description_page = GameDescriptionPage(self)
        self.game_dashboard_page = GameDashboardPage(self)

        # Add pages to the stack
        self.addWidget(self.user_info_page)             # index 0
        self.addWidget(self.device_selection_page)      # index 1
        self.addWidget(self.connection_schema_page)     # index 2
        self.addWidget(self.personality_test_page)      # index 3
        self.addWidget(self.state_test_page)            # index 4
        self.addWidget(self.game_description_page)      # index 5
        self.addWidget(self.game_dashboard_page)        # index 6

        # Start with the first page
        self.setCurrentIndex(6)

    def next_page(self):
        """Move to next page."""
        current_index = self.currentIndex()
        if current_index < self.count() - 1:
            self.setCurrentIndex(current_index + 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # with open("front/styles/main_styles.qss", "r") as f:
    #     app.setStyleSheet(f.read())

    window = MainApp()
    window.setWindowTitle("Experimental App")
    window.resize(1080, 600)
    window.show()
    sys.exit(app.exec_())
