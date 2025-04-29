from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QMessageBox, QCheckBox
from PyQt5.QtCore import Qt

class DeviceSelectionPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent
        self.session = self.main_app.session

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        textfields_layout = QVBoxLayout()

        # Title
        title = QLabel("Device Selection")
        title.setProperty("role", "title")
        # title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title)

        # Device Dropdown
        self.device_dropdown = QComboBox()
        self.device_dropdown.addItems(["Select a device", "BioRadio"])
        textfields_layout.addWidget(self.device_dropdown)

        # Next Button
        next_button = QPushButton("Next")
        next_button.setObjectName("primary_button")
        next_button.clicked.connect(self.validate_selection)
        textfields_layout.addWidget(next_button)

        textfields_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(title_layout)
        layout.addStretch(1)
        layout.addLayout(textfields_layout)
        layout.addStretch(1)

        self.setLayout(layout)

    def validate_selection(self):
        selected_device = self.device_dropdown.currentText()
        
        # Check if the user selected something valid
        if selected_device == "Select a device":
            QMessageBox.warning(self, "Device Selection", "Please select a device before proceeding.")
            return

        # Save selected device to session for later use
        self.session.device_info["name"] = selected_device
        
        # Go to next page
        self.main_app.next_page()
