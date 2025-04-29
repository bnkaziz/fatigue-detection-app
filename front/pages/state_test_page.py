from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import webbrowser

class StateTestPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent
        self.session = self.main_app.session

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        info_layout = QVBoxLayout()

        # Title
        title = QLabel("Current State Test")
        title.setProperty("role", "title")
        # title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)

        # Description
        description = QLabel("Please complete the current state test. You can scan the QR code below or click the link to open the test in your browser.")
        description.setWordWrap(True)
        info_layout.addWidget(description)

        # QR Code
        qr_label = QLabel()
        pixmap = QPixmap("front/assets/qr_state.webp")
        qr_label.setPixmap(pixmap.scaledToWidth(200))
        qr_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(qr_label)

        # Link
        link_label = QLabel('<a href="https://www.eskal.ru/link_t.php?link=bRt7tTmx">Open Test in Browser</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(link_label)

        # Next Button
        next_button = QPushButton("Next")
        next_button.setObjectName("primary_button")
        next_button.clicked.connect(self.main_app.next_page)
        info_layout.addWidget(next_button)

        info_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(title_layout)
        layout.addStretch(1)
        layout.addLayout(info_layout)
        layout.addStretch(1)

        self.setLayout(layout)
