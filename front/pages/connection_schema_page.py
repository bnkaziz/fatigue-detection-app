from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ConnectionSchemaPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent
        self.session = self.main_app.session

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        image_layout = QVBoxLayout()

        # Title
        title = QLabel("Device Connection Schema")
        title.setProperty("role", "title")
        # title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)

        # Image
        image_label = QLabel()
        pixmap = QPixmap("front/assets/schema_diagram.png")
        image_label.setPixmap(pixmap.scaledToWidth(1000))
        image_layout.addWidget(image_label)

        # Next Button
        next_button = QPushButton("Next")
        next_button.setObjectName("primary_button")
        next_button.clicked.connect(self.main_app.next_page)
        image_layout.addWidget(next_button)

        image_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(title_layout)
        layout.addStretch(1)
        layout.addLayout(image_layout)
        layout.addStretch(1)

        self.setLayout(layout)
