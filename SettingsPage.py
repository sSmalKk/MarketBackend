from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from settings import INPUTS, RESOLUTIONS

class SettingsPage(QWidget):
    def __init__(self, router, parent=None):
        super().__init__(parent)
        self.router = router
        self.setWindowTitle("Settings")
        self.parent = parent

        # Create the central widget for the settings page
        settings_layout = QVBoxLayout()

        # Add the available inputs
        for input_data in INPUTS:
            button = QPushButton(input_data["name"])
            settings_layout.addWidget(button)

        # Add the resolution dropdown
        combo_box = QComboBox()
        combo_box.addItems(RESOLUTIONS)
        settings_layout.addWidget(combo_box)

        # Add the hotbar
        hotbar_layout = QHBoxLayout()
        button_back = QPushButton("Back")
        button_back.clicked.connect(self.go_to_main_menu)
        hotbar_layout.addWidget(button_back)
        settings_layout.addLayout(hotbar_layout)

        self.setLayout(settings_layout)

    def go_to_main_menu(self):
        self.router.go_back()
