# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py

from mainform import MainUI

class MainWindow(QMainWindow):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app
        self.ui = MainUI(app, self)
        self.ui.setupUi(self)

        self.ui.actionQuit.triggered.connect(self.prg_quit)



    def prg_quit(self):
        self._app.quit()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow(app)
    widget.show()
    sys.exit(app.exec())
