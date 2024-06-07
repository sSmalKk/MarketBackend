from PyQt5.QtWidgets import QStackedWidget

class Router:
    def __init__(self):
        self.main_window = None
        self.stacked_widget = QStackedWidget()
        self.main_page = None
        self.settings_page = None
        self.singleplayer_page = None

    def set_main_window(self, main_window):
        self.main_window = main_window
        self.main_window.setCentralWidget(self.stacked_widget)

    def set_main_page(self, main_page):
        self.main_page = main_page
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.setCurrentWidget(self.main_page)

    def set_settings_page(self, settings_page):
        self.settings_page = settings_page
        self.stacked_widget.addWidget(self.settings_page)
        self.stacked_widget.setCurrentWidget(self.settings_page)

    def set_singleplayer_page(self, singleplayer_page):
        self.singleplayer_page = singleplayer_page
        self.stacked_widget.addWidget(self.singleplayer_page)
        self.stacked_widget.setCurrentWidget(self.singleplayer_page)

    def go_back(self):
        if self.stacked_widget.count() > 1:
            self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
