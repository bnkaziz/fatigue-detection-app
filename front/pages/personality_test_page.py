from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import webbrowser

class PersonalityTestPage(QWidget):
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
        title = QLabel("Оценка личности")
        title.setProperty("role", "title")
        # title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)

        # Description
        description = QLabel("Пожалуйста, пройдите личностный тест. Вы можете отсканировать QR-код ниже или перейти по ссылке, чтобы открыть тест в вашем браузере.\nПосле завершения теста, пожалуйста, введите свой результат ниже")
        description.setWordWrap(False)
        info_layout.addWidget(description)

        # QR Code
        qr_label = QLabel()
        pixmap = QPixmap("front/assets/qr_personality.webp")
        qr_label.setPixmap(pixmap.scaledToWidth(200))
        qr_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(qr_label)

        # Link
        link_label = QLabel('<a href="https://www.eskal.ru/link_t.php?link=gH3UdDca">Открыть тест в браузере</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(link_label)

        # Personality Result
        self.personality = QComboBox()
        self.personality.addItems(["Выберите свой тип личности", "Координирующий тип", "Стимулирующий тип", "Содействующий тип", "Контролирующий тип"])
        info_layout.addWidget(self.personality)

        # Next Button
        next_button = QPushButton("Продолжить")
        next_button.setObjectName("primary_button")
        next_button.clicked.connect(self.validate_and_continue)
        info_layout.addWidget(next_button)

        info_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(title_layout)
        layout.addStretch(1)
        layout.addLayout(info_layout)
        layout.addStretch(1)

        self.setLayout(layout)

    def validate_and_continue(self):
        personality = self.personality.currentText()

        if personality == "SВыберите свой тип личности":
            QMessageBox.warning(self, "Incomplete", "Please fill all fields to continue.")
            return
        
        # Save info into session
        self.session.user_info = {
            "personality": personality
        }

        self.main_app.next_page()
