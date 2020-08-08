import sys
import PySide2
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QComboBox, QWidget, QCheckBox
from PySide2.QtCore import QFile, QObject, Signal, Slot
#from AnimeUnityEngine import scraper, logging_aux, res_obj_manipulator, jdownloader
import printer
import ast
search_ui = 'UIs/searchwindow.ui'
config_io = 'UIs/settingswindow.ui'
imported_config = {'crawl_path': None, 'download_path': None, 'season': None}
create_crawl = False
def import_config():
    global imported_config
    with open('config.txt') as f:
            config = (f.read())
            #converte da stringa a  dizionario
            imported_config = ast.literal_eval(config)
            f.close()
class SearchWindow(QWidget):
    import_config()
    def settings(self):
        global create_crawl
        global imported_config
        loader = QUiLoader()
        ui_file = QFile(config_io)
        self.wid = loader.load(ui_file)
        self.wid.setWindowTitle('Settings')
        self.wid.show()
        self.create_crw = self.wid.findChild(QCheckBox,'crawljob_check')
        self.save_btn = self.wid.findChild(QPushButton, 'save_button')
        self.crawl_path = self.wid.findChild(QLineEdit, 'crawl_ledit')
        self.download_path = self.wid.findChild(QLineEdit, 'download_ledit')
        self.season = self.wid.findChild(QLineEdit, 'season_ledit')
        if (imported_config['season'] is not None):
            self.season.setText(imported_config['season'])
        if (imported_config['download_path'] is not None):
            self.download_path.setText(imported_config['download_path'])
        if (imported_config['crawl_path'] is not None):
            self.crawl_path.setText(imported_config['crawl_path'])
        self.crawl_path.setEnabled(self.create_crw.isChecked())
        self.download_path.setEnabled(self.create_crw.isChecked())
        #ui_file.close()
        create_crawl = self.create_crw
        self.bind_attributes_settings()
    def bind_attributes_settings(self):
        self.create_crw.clicked.connect(self.changed_state)
        self.save_btn.clicked.connect(self.save_config)
    def changed_state(self):
        self.crawl_path = self.wid.findChild(QLineEdit, 'crawl_ledit')
        self.download_path = self.wid.findChild(QLineEdit, 'download_ledit')
        self.crawl_path.setEnabled(create_crawl.isChecked())
        self.download_path.setEnabled(create_crawl.isChecked())
    def save_config(self):
        global imported_config
        self.crawl_path = self.wid.findChild(QLineEdit, 'crawl_ledit')
        self.download_path = self.wid.findChild(QLineEdit, 'download_ledit')
        self.season = self.wid.findChild(QLineEdit, 'season_ledit')
        #save_button
        create_crawl = self.create_crw.isChecked()
        crw_path = (self.crawl_path.text())
        down_path = (self.download_path.text())
        season_sel = (self.season.text())
        # building and saving conifg
        imported_config = "{'crawl_path': '%s', 'download_path': '%s', 'season': '%s'}"%(self.crawl_path.text(),self.download_path.text(),self.season.text())
        with open('config.txt','w') as f:
            f.write(imported_config)
            f.close()
        import_config()
        #test new file
        self.wid.close()


    search_res_signal = Signal(dict)
    def __init__(self):
        super(SearchWindow, self).__init__()
        ui_file = QFile(search_ui)

        if not ui_file.open(QFile.ReadOnly):
            print("Cannot open {}: {}".format(search_ui, ui_file.errorString()))
            sys.exit(-1)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        self.window.setWindowTitle('AnimeUnity')
        self.title_ledit = self.window.findChild(QLineEdit, 'title_ledit')
        self.genre_cbox = self.window.findChild(QComboBox, 'genre_cbox')
        self.year_ledit = self.window.findChild(QLineEdit, 'year_ledit')
        self.search_btn = self.window.findChild(QPushButton, 'search_btn')
        self.settings_btn = self.window.findChild(QPushButton, 'settings_b')
        keyword = self.title_ledit
        ui_file.close()

        self.bind_attributes()
        self.window.show()

    def bind_attributes(self):
        self.search_btn.clicked.connect(self.debug_print)
        self.settings_btn.clicked.connect(self.settings)
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
