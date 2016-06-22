import sys
from PyQt4 import QtCore, QtGui, uic
import recipe as rcp

qtCreatorFile = "pymurgui.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.target = rcp.Target()
		self.malt_list.addItems(rcp.grist.D_NAME)
		self.attenuationEdit.setText('%.1f' % (self.target.attenuation * 100.0))
		self.attenuationEdit.editingFinished.connect(lambda: self.paramsedit('attenuation'))
		self.batchsizeEdit.setText('%.1f' % self.target.batchsize)
		self.boiltimeEdit.setText('%d' % self.target.boiltime)
		self.efficiencyEdit.setText('%.1f' % (self.target.efficiency * 100.0))
		self.graintempEdit.setText('%.1f' % self.target.graintemp)
		self.mashtempEdit.setText('%.1f' % self.target.mashtemp)
		self.mash_button.clicked.connect(self.mash)

	def updatevitals(self):
		self.ogOut.setText('%.3f' % self.target.og)
		self.fgOut.setText('%.3f' % self.target.fg)
		self.abvOut.setText('%.1f' % self.target.abv)
		self.srmOut.setText('%d' % self.target.srm)
		self.mashliquorOut.setText('%.2f' % self.target.mashliquor)
		self.striketempOut.setText('%.1f' % self.target.strike)
		self.spargeliquorOut.setText('%.2f' % self.target.spargeliquor)
		self.boiloffOut.setText('%.2f' % self.target.boiloff)
		self.totalliquorOut.setText('%.2f' % self.target.totalliquor)

	def paramsedit(self, key):
		mapping = {	'attenuation': self.attenuationEdit, 'batchsize': self.batchsizeEdit,
					'boiltime': self.boiltimeEdit, 'efficiency': self.efficiencyEdit,
					'graintemp': self.graintempEdit, 'mashtemp': self.mashtempEdit}
		mapping[key].setModified(True)
		if key == 'boiltime':
			value = '%d'
		else: 
			value = '%.1f'
		setattr(self.target, key, value) % mapping[key].text()
		self.updatevitals()
		print 'arse'

	def mash(self):
		weight = float(self.weight_box.text())
		malt = str(self.malt_list.currentText())
		self.target.mash_in(malt, weight)
		self.mashtable.setRowCount(0)
		for key, value in self.target.grist.items():
			row = self.mashtable.rowCount()
			self.mashtable.insertRow(row)
			self.mashtable.setItem(row, 0, QtGui.QTableWidgetItem('%.2f' % value))
			self.mashtable.setItem(row, 1, QtGui.QTableWidgetItem(key))
			self.mashtable.setItem(row, 2, QtGui.QTableWidgetItem(str(rcp.potential_sg(key, value))))
			self.mashtable.setItem(row, 3, QtGui.QTableWidgetItem('%d' % rcp.get_srm(key)))
		self.mashtable.resizeColumnsToContents()
		

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MyApp()
	window.show()
	sys.exit(app.exec_())