import ingredients as ing

class Target(object):
	def __init__(self):
		self.grist = {} 			#'malt' : weight
		self.hops = {}				#'hop' : weight
		self.attenuation = 0.80		#percent, use setattr(object, 'attribute', value) to change
		self.batchsize = 6.0		#Gallons, use setattr(object, 'attribute', value) to change
		self.boiltime = 60			#Minutes, use setattr(object, 'attribute', value) to change
		self.efficiency = 0.75		#percent, use setattr(object, 'attribute', value) to change
		self.graintemp = 70.0 		#Fahrenheit, use setattr(object, 'attribute', value) to change
		self.mashtemp = 153.0 		#Fahrenheit, use setattr(object, 'attribute', value) to change
		Target.maltweight = property(lambda self: sum(self.grist.values()))
		Target.absorption = property(lambda self: self.maltweight * 1/8) #For 0.5 qt/lb use 1/8, +/- 1/16 increments by 0.25 qt/lb
		Target.mashliquor = property(lambda self: self.maltweight * 3/8) #For 1.5 qt/lb use 3/8, +/- 1/16 increments by 0.25 qt/lb
		Target.strike = property(lambda self: 0.0 if not any(self.grist) else ing.strike_temp(self))
		Target.og = property(lambda self: 1.0 + (ing.mash_sg(self.grist) * self.efficiency / self.batchsize))
		Target.fg = property(lambda self: 1.0 + ((self.og - 1.0) * (1.0 - self.attenuation)))
		Target.srm = property(lambda self: ing.potential_srm(self.grist, self.batchsize))
		Target.abv = property(lambda self: (1.05/0.79) * ((self.og - self.fg) / self.fg) * 100.0)
		Target.boiloff = property(lambda self: (self.boiltime / 60) * 1.25) #1.25 gal/hr evaporation
		Target.totalliquor = property(lambda self: (1.04 * self.batchsize) + self.absorption + self.boiloff + 0.25)
		Target.spargeliquor = property(lambda self: self.totalliquor - self.mashliquor)

	def mash_in(self, malt, weight):
		self.grist[malt] = weight

#-------------TESTING-------------#
def printtest(x):
	print x.grist
	print 'Malt Weight (lb): 	%.2f' % x.maltweight
	print 'Absorption (gal): 	%.2f' % x.absorption
	print 'Strike Temp (F): 	%.1f' % x.strike
	print 'Orig Gravity (SG): 	%.3f' % x.og
	print 'Final Gravity (SG): 	%.3f' % x.fg
	print 'Beer Color (SRM): 	%d' % x.srm
	print 'Alcohol by Vol (%%): 	%.1f' % x.abv
	print 'Boiloff (gal):		%.2f' % x.boiloff
	print 'Mash Liquor (gal):	%.2f' % x.mashliquor
	print 'Sparge Liquor (gal):	%.2f' % x.spargeliquor
	print 'Total Liquor (gal):	%.2f' % x.totalliquor

def main():
	b = Target()
	printtest(b)
	b.mash_in('United Kingdom - Maris Otter Pale', 10.0)
	printtest(b)
	b.mash_in('United Kingdom - Roasted Barley', 0.25)
	printtest(b)
	setattr(b, 'graintemp', 10.0)
	printtest(b)
	raw_input('main')

if __name__ == '__main__':
	main()