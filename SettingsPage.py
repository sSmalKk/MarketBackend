from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QApplication,
    QGroupBox,
    QMessageBox,
)
import sys
import os

from settings import INPUT, SETTINGS, RESOLUTIONS, DEFAULT_SETTINGS
class SettingsPage(QWidget):
    def __init__(self, router, parent=None):
        super().__init__(parent)
        self.router = router
        self.setWindowTitle("Settings")
        self.parent = parent
        self.settings_saved = False  # Flag to track if settings have been saved

        # Create the central widget for the settings page
        main_layout = QVBoxLayout()

        # Add available settings
        settings_group = QGroupBox("Settings")
        self.settings_layout = QVBoxLayout()  # Store settings layout as an attribute
        for setting_data in SETTINGS:
            setting_layout = QHBoxLayout()

            setting_label = QLabel(setting_data["name"])
            setting_layout.addWidget(setting_label)

            setting_combo = QComboBox()
            setting_combo.addItems(setting_data["options"])
            setting_combo.setCurrentText(setting_data["default"])  # Set default value
            setting_layout.addWidget(setting_combo)

            self.settings_layout.addLayout(
                setting_layout
            )  # Add setting layout to main settings layout

        settings_group.setLayout(
            self.settings_layout
        )  # Set settings layout as the layout of settings group
        main_layout.addWidget(settings_group)

        # Add available inputs
        inputs_group = QGroupBox("Inputs")
        inputs_layout = QVBoxLayout()
        self.input_buttons = []  # Store input buttons for later reference
        for input_data in INPUT:
            input_layout = QHBoxLayout()

            input_label = QLabel(input_data["name"])
            input_layout.addWidget(input_label)

            input_button = QPushButton(input_data["default"])  # Set default value
            input_button.clicked.connect(self.capture_key_press)
            input_layout.addWidget(input_button)

            inputs_layout.addLayout(input_layout)
            self.input_buttons.append(input_button)

        inputs_group.setLayout(inputs_layout)
        main_layout.addWidget(inputs_group)

        # Add resolution dropdown
        resolution_group = QGroupBox("Resolution")
        resolution_layout = QHBoxLayout()
        resolution_label = QLabel("Resolution")
        resolution_layout.addWidget(resolution_label)

        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(RESOLUTIONS)
        self.resolution_combo.setCurrentText(DEFAULT_SETTINGS["resolution"])  # Set default value
        resolution_layout.addWidget(self.resolution_combo)

        resolution_group.setLayout(resolution_layout)
        main_layout.addWidget(resolution_group)

        # Add navigation bar
        hotbar_layout = QHBoxLayout()
        button_save = QPushButton("Save")
        button_save.clicked.connect(self.save_settings)
        hotbar_layout.addWidget(button_save)

        button_back = QPushButton("Back")
        button_back.clicked.connect(self.go_to_main_menu)
        hotbar_layout.addWidget(button_back)
        main_layout.addLayout(hotbar_layout)

        self.setLayout(main_layout)


    def capture_key_press(self):
        sender_button = self.sender()
        sender_button.setText("Press any key")

        # Install event filter on the button
        sender_button.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            key = event.key()
            sender_button = obj
            if sender_button:
                sender_button.setText(
                    QApplication.translate("SettingsPage", "Key: ") + str(key)
                )
                obj.setEnabled(True)  # Re-enable the button
                obj.removeEventFilter(
                    self
                )  # Remove the event filter after the key is pressed
                return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.releaseKeyboard()  # Release keyboard focus if ESC key is pressed
        else:
            # Store the ID of the pressed key
            self.pressed_key_id = event.key()
            print("Key pressed:", self.pressed_key_id)

    def go_to_main_menu(self):
        if not self.settings_saved:
            reply = QMessageBox.question(
                self,
                "Message",
                "Settings not saved! Are you sure you want to go back?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                self.router.go_back()
        else:
            self.router.go_back()

    def save_settings(self):
        settings_data = {}

        # Save settings
        for index in range(len(SETTINGS)):
            setting_name = SETTINGS[index]["name"]
            setting_value = (
                self.settings_layout.itemAt(index).itemAt(1).widget().currentText()
            )
            settings_data[setting_name] = setting_value

        # Save inputs
        for index in range(len(INPUT)):
            input_name = INPUT[index]["name"]
            input_value = self.input_buttons[index].text()
            settings_data[input_name] = input_value

        # Save resolution
        selected_resolution = self.resolution_combo.currentText()
        settings_data["resolution"] = selected_resolution

        save_path = os.path.join(os.path.expanduser("~"), "Documents", "saves")
        os.makedirs(save_path, exist_ok=True)

        settings_file = os.path.join(save_path, "settings.txt")
        with open(settings_file, "w") as file:
            for key, value in settings_data.items():
                file.write(f"{key}: {value}\n")

        QMessageBox.information(
            self, "Settings Saved", f"Settings saved successfully at {settings_file}!"
        )

        # Set flag indicating settings have been saved
        self.settings_saved = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    router = None  # Substitua por um objeto router real, se necessário
    window = SettingsPage(router, parent=None)
    window.show()
    sys.exit(app.exec_())
