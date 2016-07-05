#import ingredients as ing
import pandas as p 
import math as m

gpath = 'Data/gristlist.csv'
hpath = 'Data/hoplist.csv'

grist = p.read_csv(gpath, header = 0)
hops = p.read_csv(hpath, header = 0)

#Strike temp functions
def strike_temp(x):
	scalar = (1.0 + (0.44 * (x.maltweight/(x.mashliquor * 8.18)) * (1.0 - (x.graintemp/x.mashtemp))))
	return x.mashtemp * scalar

#SG functions
def potential_sg(malt, weight):
	index = grist[grist['D_NAME'] == malt].index.tolist()[0]
	ppg = grist.POT_SG.iloc[index] - 1.0
	return ppg * weight

def mash_sg(mash):
	sg = 0.0
	for malt, weight in mash.items():
		sg += potential_sg(malt, weight)
	return sg

#SRM functions
def potential_srm(mash, batchsize):
	mcu = 0.0
	for malt, weight in mash.items():
		index = grist[grist['D_NAME'] == malt].index.tolist()[0]
		color = grist.LOV.iloc[index]
		mcu += ((color * weight) / batchsize)
	if mcu < 10.5:
		return mcu
	else:
		return 1.4922 * (mcu ** 0.6859)

def get_srm(malt):
	index = grist[grist['D_NAME'] == malt].index.tolist()[0]
	srm = grist.LOV.iloc[index]
	return srm

#Recipe target
class Target(object):
	def __init__(self):
		self.grist = {} 			#'malt' : weight
		self.hops = {}				#'hop' : weight
		self.attenuation = 0.80		#percent, use setattr(object, 'attribute', value) to change
		self.batchsize = 6.0		#Gallons, use setattr(object, 'attribute', value) to change
		self.boiltime = 60			#Minutes, use setattr(object, 'attribute', value) to change
		self.efficiency = 0.75		#percent, use setattr(object, 'attribute', value) to change
		self.graintemp = 78.0 		#Fahrenheit, use setattr(object, 'attribute', value) to change
		self.mashtemp = 152.0 		#Fahrenheit, use setattr(object, 'attribute', value) to change
		Target.maltweight = property(lambda self: sum(self.grist.values()))
		Target.absorption = property(lambda self: self.maltweight * 1/8) #For 0.5 qt/lb use 1/8, +/- 1/16 increments by 0.25 qt/lb
		Target.mashliquor = property(lambda self: self.maltweight * 5/16) #For 1.5 qt/lb use 3/8, +/- 1/16 increments by 0.25 qt/lb
		Target.strike = property(lambda self: 0.0 if not any(self.grist) else strike_temp(self))
		Target.og = property(lambda self: 1.0 + (mash_sg(self.grist) * self.efficiency / self.batchsize))
		Target.fg = property(lambda self: 1.0 + ((self.og - 1.0) * (1.0 - self.attenuation)))
		Target.srm = property(lambda self: potential_srm(self.grist, self.batchsize))
		Target.abv = property(lambda self: (1.05/0.79) * ((self.og - self.fg) / self.fg) * 100.0)
		Target.boiloff = property(lambda self: (self.boiltime / 60) * 1.5) #1.25 gal/hr evaporation
		Target.totalliquor = property(lambda self: (1.04 * self.batchsize) + self.absorption + self.boiloff + 1.0) #0.25 gal trub loss, 0.75 gal dead space
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
	b.mash_in('American - Pale Ale', 10.0)
	b.mash_in('American - Caramel / Crystal 40L', 0.75)
	b.mash_in('American - Caramel / Crystal 15L', 0.75)
	b.mash_in('Rice Hulls', 1.0)
	printtest(b)

if __name__ == '__main__':
	main()