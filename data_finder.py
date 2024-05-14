import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from database import Database

class PathList(QListWidget):
    def __init__(self):
        super(PathList, self).__init__()
        self.paths = []
        self.itemDoubleClicked.connect(self.open_folder)

    def open_folder(self, item):
        path = self.paths[self.row(item)]
        path = path.replace("/","\\")
        QtCore.QProcess.startDetached("explorer", [path])

    def update(self):
        for path in self.paths:
            self.addItem(path)


class DataFinder(QMainWindow):
    def __init__(self, addr):
        super().__init__()
        self.db = Database()
        self.addr = addr
        self._init_ui()
        self.handle_search()

    def _init_ui(self):
        self.setWindowTitle('data-finder')
        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        label_names = list(self.db.metadata.keys())[1:]
        self.labels = []
        self.lineedits = []
        self.layout = QGridLayout()
        self.pathlist = PathList()

        for i_row, name in enumerate(label_names):
            self.labels.append( QLabel(name) )
            self.lineedits.append( QLineEdit() )
            self.layout.addWidget(self.labels[-1], i_row, 0)
            self.layout.addWidget(self.lineedits[-1], i_row, 1)
            
            self.lineedits[-1].returnPressed.connect(self.handle_search)

        self.layout.addWidget(self.pathlist, i_row+1, 0)

        self.widget.setLayout(self.layout)

    @staticmethod
    def load_values(lineedit: QLineEdit) -> list:
        text = lineedit.text()
        text = text.replace(" ", "")
        return text.split(',')

    def handle_search(self):
        self.pathlist.clear()          

        self.search_list = []
        for label, lineedit in zip(self.labels, self.lineedits):
            key = label.text()
            for value in self.load_values(lineedit):
                self.search_list.append((key, value))

        data = self.db.search(self.addr, self.search_list)

        self.pathlist.paths.clear()           
        for d in data:
            self.pathlist.paths.append( d['path'] )            

        self.pathlist.update()          


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DataFinder(sys.argv[1])
    widget.show()
    sys.exit(app.exec_())
