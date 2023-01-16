import sys
from dataclasses import dataclass

import pyautogui
from PyQt5 import QtTest
from PyQt5.QtCore import QEvent, QSettings, Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSizePolicy,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)
from Xlib import display


@dataclass
class MainWindow:
    emoji_grid_layout = None
    main_window = None
    emoji_grid_column_count = 7
    emoji_grid_row_count = 4
    emoji_font_size = 20
    will_exit_on_its_own = False


class KaoMojiPopulation:
    def emoji_clicked(self, emoji):
        self.will_exit_on_its_own = True
        self.main_window.close()
        QApplication.clipboard().setText(emoji)
        pyautogui.hotkey("ctrl", "v")
        QtTest.QTest.qWait(250)

    def search_kaomoji_tag(self, tag):
        pass


class Window(QWidget, MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        super(QWidget, self).__init__()
        self.installEventFilter(self)
        self.title = "Emoji Picker >,< "
        # self.check_windows()
        self.create_text_box()
        self.initUI()

    def check_windows(self):
        return False

    def get_mouse_pos(self):
        if not self.check_windows():
            # we are in linxu
            pointerData = display.Display().screen().root.query_pointer()._data
            return pointerData["root_x"], pointerData["root_y"]

    def create_text_box(self):
        self.width = 270
        self.height = 250
        self.left, self.top = self.get_mouse_pos()

    def initUI(self):
        layout = QVBoxLayout()
        scroll_placement = QScrollArea()
        grid_widget = QWidget()
        self.emoji_grid_layout = QGridLayout(grid_widget)
        self.emoji_grid_layout.setAlignment(Qt.AlignHCenter)

        grid_widget.setStyleSheet(
            "QLabel:hover{background-color:palette(highlight);}"
        )
        scroll_placement.setWidget(grid_widget)
        scroll_placement.setWidgetResizable(True)
        layout.addWidget(scroll_placement)
        # bottom text entry
        lineEdit = QLineEdit()
        # lineEdit.textChanged.connect()
        layout.addWidget(lineEdit)

        # align it to the bottom, so that it won't stay centered vertically
        layout.setAlignment(lineEdit, Qt.AlignBottom)

        self.setLayout(layout)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.main_window = self

        self.show()

    def keyPressEvent(self, event):
        super(Window, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    # focus handling
    global willExitOnItsOwn

    def eventFilter(self, object, event):
        if (
            event.type() == QEvent.WindowDeactivate
            or event.type() == QEvent.FocusOut
        ):
            if not willExitOnItsOwn:
                self.quitNicely()
        return False

    def on_key(self, key):
        # test for a specific key
        if key == Qt.Key_Escape:
            self.quitNicely()

    def quitNicely(self):
        self.main_window.hide()
        quit()


# clickable label
class QClickableLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit(self.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
