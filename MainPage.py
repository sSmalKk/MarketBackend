from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

class MainPage(QMainWindow):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.setWindowTitle("Main Menu")
        self.central_widget = QWidget()

        # Define a layout for the central widget
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Define a layout for the buttons
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignCenter)

        # Add the buttons
        for label in ["Singleplayer", "Multiplayer", "Settings", "Character", "Quit"]:
            button = QPushButton(label)
            button.setMaximumWidth(200)
            button.setMinimumWidth(50)
            button.setMinimumHeight(30)
            self.buttons_layout.addWidget(button)
            self.buttons_layout.setSpacing(20)
            button.clicked.connect(self.on_button_clicked)

        # Add the title "LOREM" at the top
        self.label_title = QLabel("LOREM")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 150px;")
        self.main_layout.addWidget(self.label_title)

        # Add the buttons to the main layout
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.buttons_layout)

        # Define the layout for the central widget
        self.central_widget.setLayout(self.main_layout)

        # Set the central widget of the main window
        self.setCentralWidget(self.central_widget)

    def on_button_clicked(self):
        sender = self.sender()
        if sender.text() == "Singleplayer":
            self.openSingleplayerPage()
        elif sender.text() == "Settings":
            self.openSettingsPage()

    def openSingleplayerPage(self):
        from SingleplayerPage import SingleplayerPage
        self.router.set_singleplayer_page(SingleplayerPage(self.router))

    def openSettingsPage(self):
        from SettingsPage import SettingsPage
        self.router.set_settings_page(SettingsPage(self.router))
