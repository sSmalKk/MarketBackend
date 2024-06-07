import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from MainPage import MainPage
from Router import Router

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.router = Router()

        self.main_page = MainPage(self.router)
        
        self.router.set_main_window(self.main_window)
        self.router.set_main_page(self.main_page)

        self.app.lastWindowClosed.connect(self.closeEvent)

    def closeEvent(self):
        self.app.quit()

    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = App()
    app.run()
