import sys
from PyQt4 import QtCore, QtGui, uic
import recipe as rcp

qtCreatorFile = "pymurgui.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

target = rcp.Target()

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

	def updateVitals(self):
		self.lblABV.setText('%.1f' % target.abv)
		self.lblBoiloff.setText('%.2f' % target.boiloff)
		self.lblFG.setText('%.3f' % target.fg)
		self.lblMashLiquor.setText('%.2f' % target.mashliquor)
		self.lblOG.setText('%.3f' % target.og)
		self.lblSRM.setText('%d' % target.srm)
		self.lblSpargeLiquor.setText('%.2f' % target.spargeliquor)
		self.lblStrikeTemp.setText('%.2f' % target.strike)
		self.lblTotalLiquor.setText('%.2f' % target.totalliquor)

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())