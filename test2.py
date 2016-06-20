import sys
from PyQt4 import QtCore, QtGui

class ChildWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle("Child Window!")


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = ChildWindow()
    myapp.show()
    sys.exit(app.exec_())