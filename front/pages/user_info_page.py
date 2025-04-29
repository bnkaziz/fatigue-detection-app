from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt

class UserInfoPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent  # to call main_app.next_page()
        self.session = self.main_app.session

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        textfields_layout = QVBoxLayout()

        # Title
        title = QLabel("Личная информация")
        title.setProperty("role", "title")
        # title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)

        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите свое имя")
        textfields_layout.addWidget(self.name_input)

        # Age
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Введите свой возраст")
        textfields_layout.addWidget(self.age_input)

        # Gender
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Выберите свой пол", "Мужской", "Женский"])
        textfields_layout.addWidget(self.gender_input)

        # Consent Checkbox
        self.consent_checkbox = QCheckBox("Я даю согласие на сбор и обработку моих данных")
        textfields_layout.addWidget(self.consent_checkbox)

        # Next Button
        next_button = QPushButton("Продолжить")
        next_button.setObjectName("primary_button")
        next_button.clicked.connect(self.validate_and_continue)
        textfields_layout.addWidget(next_button)

        textfields_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(title_layout)
        layout.addStretch(1)
        layout.addLayout(textfields_layout)
        layout.addStretch(1)

        self.setLayout(layout)

    def validate_and_continue(self):
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()
        gender = self.gender_input.currentText()
        consent = self.consent_checkbox.isChecked()

        if not name or not age or gender == "Выберите свой пол" or not consent:
            QMessageBox.warning(self, "Incomplete", "Please fill all fields and agree to continue.")
            return
        
        # Save info into session
        self.session.user_info = {
            "name": name,
            "age": age,
            "gender": gender,
            "consent": consent
        }

        self.main_app.next_page()
