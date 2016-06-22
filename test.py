import sys
from PyQt4 import QtCore, QtGui, uic
import recipe as rcp

qtCreatorFile = "pymurgui.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyThread(QThread):
	def __init__(self):
		QThread.__init__(self)
		pass

	def __del__(self):
		self.wait()

	def mythreadfunction(self, arg):
		pass

	def run(self):
		mtf = mythreadfunction(None)
		pass

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

	def callmythread(self):
		self.mythread = MyThread()
		self.connect(self.mythread, SIGNAL('someSignal()'), self.appfunction)

	def appfunction(self):
		pass


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())