# /front/pages/game_dashboard_page.py

import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time
import datetime
import shutil

class GameDashboardPage(QWidget):
    def __init__(self, app_controller):
        super().__init__()
        self.app_controller = app_controller
        self.start_time = time.time()  # Start the internal timer
        self.game_process = None  # We'll set this from outside
        self.init_ui()
        self.start_updating()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left side: Info + Graph
        left_layout = QVBoxLayout()

        self.label_level = QLabel("Level: Loading...")
        self.label_level.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.label_score = QLabel("Score: Loading...")
        self.label_score.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.label_hits_misses = QLabel("Hits/Misses: Loading...")
        self.label_hits_misses.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.label_elapsed = QLabel("Elapsed Time: Loading...")
        self.label_elapsed.setStyleSheet("font-size: 26px; font-weight: bold;")
        self.label_status = QLabel("Status: Loading...")
        self.label_status.setStyleSheet("font-size: 26px; font-weight: bold;")

        left_layout.addWidget(self.label_level)
        left_layout.addWidget(self.label_score)
        left_layout.addWidget(self.label_hits_misses)
        left_layout.addWidget(self.label_elapsed)
        left_layout.addWidget(self.label_status)

        # Graph
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        left_layout.addWidget(self.canvas)

        # STOP button
        self.stop_button = QPushButton("STOP GAME")
        self.stop_button.clicked.connect(self.stop_game)
        left_layout.addWidget(self.stop_button)

        # Right side: BioRadio placeholder image
        right_layout = QVBoxLayout()

        title = QLabel("Real-Time BioSignals")
        title.setProperty("role", "title")
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        # Load placeholder image
        image_path = os.path.join("front", "assets", "bioradio_placeholder.png")  # Adjust filename if needed
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("BioRadio plot will appear here.")

        right_layout.addWidget(self.image_label)

        # Add left and right layouts to the main layout
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=1)

        self.setLayout(main_layout)

    def start_updating(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(1000)  # update every 2 seconds

    def update_dashboard(self):
        try:
            # Update internal timer
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.label_elapsed.setText(f"Elapsed Time: {minutes:02d}:{seconds:02d}")

            with open(os.path.join("data", "performance_new", "performance_live.json"), "r") as f:
                data = json.load(f)

            self.label_level.setText(f"Level: {data['level']}")
            self.label_score.setText(f"Score: {data['score']}")
            self.label_hits_misses.setText(f"Hits/Misses: {data['hits']} / {data['misses']}")
            self.label_status.setText(f"Status: {data['status']}")

            # Update graph
            performance = data.get('performance_history', [])
            self.ax.clear()
            if performance:
                x = list(range(1, len(performance)+1))
                y = [item["success_ratio"] for item in performance]
                self.ax.plot(x, y, marker='o')
                self.ax.set_title("Performance Over Time")
                self.ax.set_xlabel("Checkpoint")
                self.ax.set_ylabel("Success Ratio")
                self.ax.set_ylim(0, 1.2)
            self.canvas.draw()

        except Exception as e:
            print(f"Dashboard Update Error: {e}")
        
    def stop_game(self):
        print("Stopping game and dashboard updates...")
        self.timer.stop()

        if self.app_controller and hasattr(self.app_controller, "session"):
            process = self.app_controller.session.game_process
            if process:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print("Game process terminated.")
                except Exception as e:
                    print(f"Error stopping game: {e}")
        
            # Move the final performance file
        try:
            new_path = os.path.join("data", "performance_new", "performance_live.json")
            if os.path.exists(new_path):
                # Create destination filename
                user_info = self.app_controller.session.user_info
                username = user_info.get('name')
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{username}_{timestamp}.json"
                old_path = os.path.join("data", "performance_old", filename)

                shutil.move(new_path, old_path)
                print(f"Performance data saved to {old_path}")
            else:
                print("No performance_live.json file found to move.")

        except Exception as e:
            print(f"Error moving performance file: {e}")

        self.stop_button.setEnabled(False)


