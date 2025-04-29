from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import subprocess
import sys
import os

class GameDescriptionPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent
        self.session = self.main_app.session

        self.current_slide = 0
        self.slides = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.stacked_widget = QStackedWidget()
        self.setup_slides()
        layout.addWidget(self.stacked_widget)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("< Previous")
        self.prev_button.clicked.connect(self.go_previous)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next >")
        self.next_button.clicked.connect(self.go_next)
        nav_layout.addWidget(self.next_button)

        layout.addLayout(nav_layout)
        self.setLayout(layout)

        self.update_buttons()

    def setup_slides(self):
        # Slide 1
        slide1 = self.create_slide(
            image_path="front/assets/one_circle.png",
            description="In this experiment, you will control a single circle. The goal is to stop the moving indicator inside the highlighted area."
        )
        self.stacked_widget.addWidget(slide1)

        # Slide 2
        slide2 = self.create_slide(
            image_path="front/assets/three_circles.png",
            description="Later, you will control THREE circles at once! Each one is controlled with a separate button. Try to manage them simultaneously!"
        )
        self.stacked_widget.addWidget(slide2)

        # Slide 3
        slide3 = self.create_slide(
            image_path="front/assets/speed_increase.png",
            description="As time progresses, the circles will spin faster. The difficulty will gradually increase during the experiment."
        )
        self.stacked_widget.addWidget(slide3)

        # Slide 4 - Final instructions
        slide4 = self.create_slide(
            image_path=None,
            description="Important:\n- Stay still (especially the arm where ECG is measured).\n- Do not move your head.\n- Do not talk.\n- You can stop the game whenever you want.\n- Or the researcher will stop it when ready.",
            is_final=True
        )
        self.stacked_widget.addWidget(slide4)

    def create_slide(self, image_path, description, is_final=False):
        slide = QWidget()
        layout = QVBoxLayout()

        if image_path:
            image_label = QLabel()
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaledToWidth(400, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(image_label)

        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("font-size: 16px; margin: 10px;")
        layout.addWidget(desc_label)

        if is_final:
            start_button = QPushButton("Start Game")
            start_button.clicked.connect(self.start_game)
            layout.addWidget(start_button, alignment=Qt.AlignCenter)

        slide.setLayout(layout)
        return slide

    def go_next(self):
        if self.current_slide < self.stacked_widget.count() - 1:
            self.current_slide += 1
            self.stacked_widget.setCurrentIndex(self.current_slide)
            self.update_buttons()

    def go_previous(self):
        if self.current_slide > 0:
            self.current_slide -= 1
            self.stacked_widget.setCurrentIndex(self.current_slide)
            self.update_buttons()

    def update_buttons(self):
        self.prev_button.setEnabled(self.current_slide > 0)
        if self.current_slide == self.stacked_widget.count() - 1:
            self.next_button.setEnabled(False)
        else:
            self.next_button.setEnabled(True)

    def start_game(self):
        try:
            # Find the path to the game/main.py
            game_path = os.path.join(os.getcwd(), "game", "main.py")
            if not os.path.exists(game_path):
                raise FileNotFoundError("Game file not found at " + game_path)

            # Start the game using conda python
            process = subprocess.Popen(["python", game_path], shell=True)

            # Save process in SessionManager
            self.main_app.session.game_process = process

            self.main_app.next_page()

        except Exception as e:
            QMessageBox.critical(self, "Error Starting Game", str(e))
