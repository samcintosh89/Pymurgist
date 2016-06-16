def tester(a, b):
	a.setter(b[0], b[1])
	print a.adict
	print '%s, %s' % (a.avar, a.avar2) 


class TestClass(object):
	def __init__(self):
		self.adict = {}
		self._avar = 0
		TestClass.avar2 = property(lambda self: self.avar ** 2)

	def getter(self):
		return self._avar

	def setter(self, x, y):
		self.adict[x] = y
		self._avar =  sum(self.adict.values())

	avar = property(getter, setter)



#-------------TESTING-------------#

a = TestClass()

tester(a, ['a',1])
tester(a, ['b',2])
tester(a, ['c',3])
tester(a, ['d',4])
tester(a, ['e',5])
tester(a, ['f',6])