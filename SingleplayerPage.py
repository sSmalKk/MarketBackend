import sys
import os
import random
import string
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QInputDialog,
    QMessageBox,
    QDialog,
    QLineEdit,
    QLabel,
    QApplication,
)
from PyQt5.QtCore import QTimer, QTime


class SingleplayerPage(QWidget):
    def __init__(self, router, parent=None):
        super().__init__(parent)
        self.router = router
        self.setWindowTitle("Settings")
        self.parent = parent

        # Create the central widget for the settings page
        layout = QVBoxLayout()

        # Store the world buttons and selection index
        self.world_buttons = []
        self.selected_world_index = None

        for i, label in enumerate(["World 1", "World 2", "World 3"]):
            button = QPushButton(label)
            button.clicked.connect(lambda checked, index=i: self.select_world(index))
            self.world_buttons.append(button)
            layout.addWidget(button)

        # Add the hotbar
        hotbar_layout = QHBoxLayout()
        button_back = QPushButton("Back")
        button_back.clicked.connect(self.go_to_main_menu)
        hotbar_layout.addWidget(button_back)

        button_load = QPushButton("Load")
        hotbar_layout.addWidget(button_load)

        button_create = QPushButton("Create New")
        button_create.clicked.connect(self.create_new_world)
        hotbar_layout.addWidget(button_create)

        button_edit = QPushButton("Edit")
        hotbar_layout.addWidget(button_edit)

        button_delete = QPushButton("Delete")
        hotbar_layout.addWidget(button_delete)

        layout.addLayout(hotbar_layout)
        self.setLayout(layout)

    def go_to_main_menu(self):
        self.router.go_back()

    def select_world(self, index):
        # Deselect any previously selected world
        if self.selected_world_index is not None:
            self.world_buttons[self.selected_world_index].setEnabled(True)

        # Select the new world
        self.selected_world_index = index
        self.world_buttons[index].setEnabled(False)

    def create_new_world(self):
        dialog = SeedDialog(self)
        dialog.exec_()


class SeedDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New World")
        self.seed = ""
        self.seed_length = 12
        self.current_char_index = 0
        self.timer_interval = 50  # milliseconds

        layout = QVBoxLayout()

        self.name_label = QLabel("Enter world name:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.seed_label = QLabel("Generating seed:")
        self.seed_display = QLineEdit()
        self.seed_display.setReadOnly(True)
        layout.addWidget(self.seed_label)
        layout.addWidget(self.seed_display)

        self.button_generate = QPushButton("Generate Seed")
        self.button_generate.clicked.connect(self.generate_seed)
        layout.addWidget(self.button_generate)

        self.button_create = QPushButton("Create")
        self.button_create.clicked.connect(self.create_world)
        layout.addWidget(self.button_create)

        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.reject)
        layout.addWidget(self.button_cancel)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_seed_character)
        self.random_durations = []

    def generate_seed(self):
        self.seed = ""
        self.current_char_index = 0
        self.random_durations = [
            random.uniform(1, 3) for _ in range(self.seed_length)
        ]  # Random duration between 1 to 3 seconds for each character
        self.start_time = QTime.currentTime()
        self.timer.start(self.timer_interval)

    def update_seed_character(self):
        elapsed_time = (
            self.start_time.msecsTo(QTime.currentTime()) / 100
        )  # Convert to seconds

        if self.current_char_index < self.seed_length:
            if elapsed_time < self.random_durations[self.current_char_index]:
                random_char = random.choice(string.ascii_letters + string.digits)
                if self.current_char_index == len(self.seed):
                    self.seed += random_char
                else:
                    self.seed = (
                        self.seed[: self.current_char_index]
                        + random_char
                        + self.seed[self.current_char_index + 1 :]
                    )
                self.seed_display.setText(self.seed)
            else:
                self.current_char_index += 1
                self.start_time = (
                    QTime.currentTime()
                )  # Reset start time for next character
        else:
            self.timer.stop()

    def create_world(self):
        world_name = self.name_input.text()
        if world_name and len(self.seed) == self.seed_length:
            save_path = os.path.join(
                os.path.expanduser("~"), "Documents", "ProjectRoleplay", "Saves"
            )
            os.makedirs(save_path, exist_ok=True)

            world_file = os.path.join(save_path, f"{world_name}.txt")
            with open(world_file, "w") as file:
                file.write(f"World Name: {world_name}\nSeed: {self.seed}\n")

            QMessageBox.information(
                self,
                "World Created",
                f'New world "{world_name}" with seed "{self.seed}" created successfully and saved at {world_file}!',
            )
            self.accept()
        else:
            QMessageBox.warning(
                self, "Error", "Please enter a world name and generate a complete seed."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    router = None  # Replace with actual router object
    window = SingleplayerPage(router)
    window.show()
    sys.exit(app.exec_())
