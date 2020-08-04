import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import PySide2
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QComboBox
from PySide2.QtCore import QFile, QObject, Signal, Slot
search_ui = 'UIs/searchwindow.ui'


class SearchWindow(QObject):
    search_res_signal = Signal(dict)
    def __init__(self):
        super(SearchWindow, self).__init__()
        #self.setWindowIcon(QtGui.QIcon('AnimeUnity-logo.png'))
        ui_file = QFile(search_ui)

        if not ui_file.open(QFile.ReadOnly):
            print("Cannot open {}: {}".format(search_ui, ui_file.errorString()))
            sys.exit(-1)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        self.title_ledit = self.window.findChild(QLineEdit, 'title_ledit')
        self.genre_cbox = self.window.findChild(QComboBox, 'genre_cbox')
        self.year_ledit = self.window.findChild(QLineEdit, 'year_ledit')
        self.search_btn = self.window.findChild(QPushButton, 'search_btn')

        ui_file.close()

        self.bind_attributes()
        self.window.show()

    def bind_attributes(self):
        self.search_btn.clicked.connect(self.debug_print)

    def debug_print(self):
        title = self.title_ledit.text()
        genre = self.genre_cbox.currentText()
        year = self.year_ledit.text()
        print(f"|{title}|{genre}|{year}")
        self.search_res_signal.emit({'title': title, 'genre': genre, 'year': year})


@Slot(dict)
def print_search_res(res):
    print(res)


def bind_ui():
    search.search_res_signal.connect(print_search_res)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(PySide2.QtGui.QIcon('AnimeUnity-logo.png'))
    search = SearchWindow()
    bind_ui()
    sys.exit(app.exec_())
