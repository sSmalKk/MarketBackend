from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout

class SingleplayerPage(QWidget):
    def __init__(self, router, parent=None):
        super().__init__(parent)
        self.router = router
        self.setWindowTitle("Singleplayer")
        self.parent = parent

        # Define a layout for the central widget
        layout = QVBoxLayout()

        # Add the available worlds
        for label in ["World 1", "World 2", "World 3"]:
            button = QPushButton(label)
            layout.addWidget(button)

        # Add the hotbar
        hotbar_layout = QHBoxLayout()
        button_back = QPushButton("Back")
        button_back.clicked.connect(self.go_to_main_menu)
        hotbar_layout.addWidget(button_back)
        layout.addLayout(hotbar_layout)

        # Define the layout for the central widget
        self.setLayout(layout)

    def go_to_main_menu(self):
        self.router.go_back()
