import ingredients as ing 

#Fermentable caclulation and storage
class Mash(object):
	def __init__(self):
		self.grain = {} # malt:weight
		self._mashtemp = 156.0 #Fahrenheit
		self._graintemp = 70.0
		self._strike_temp = 0.0
		self._weight = 0.0
		self._absorption = 0.0 
		self._gravity = 0.0
		self._liquor = 0.0

	def mtemp_get(self):
		return self._mashtemp

	def gtemp_get(self):
		return self._graintemp

	def stemp_get(self):
		return self._strike_temp

	def weight_get(self):
		return self._weight

	def abs_get(self):
		return self._absorption

	def sparge(self):
		return self._gravity

	def liquor_get(self):
		return self._liquor

	def temp_set(self, graint, masht):
		self._graintemp = graint
		self._mashtemp = masht
		self._strike_temp = self.mashtemp * (1.0 + (0.44 * (self.weight/(self.liquor * 8.18)) * (1.0 - (self.graintemp/self.mashtemp))))

	def mash_in(self, malt, weight):
		self.grain[malt] = weight
		self._weight = sum(self.grain.values())
		self._absorption = self.weight * 0.125
		self._gravity = ing.mash_sg(self.grain)
		self._liquor = self.weight * 3/8
		
	mashtemp = property(mtemp_get, temp_set)
	graintemp = property(gtemp_get, temp_set)
	strike_temp = property(stemp_get, temp_set)
	weight = property(weight_get, mash_in)
	absorption = property(abs_get, mash_in)
	gravity = property(sparge, mash_in)
	liquor = property(liquor_get, mash_in)


#Hopping calculation and storage
class Boil(object):
	def __init__(self):
		self.hops = {} # time:HopAddition()
		self._boiloff = 0.0
		self._total_ibu = 0.0

	def boiloff_get(self):
		return self._boiloff

	def extract(self):
		return self._total_ibu

	def boil(self, name, weight, time):
		self.hops[time] = ing.HopAddition(time)
		self.hops[time].boiled(name, weight)
		self._boiloff = (max(self.hops.keys()) / 60) * 1.25
		self._total_ibu = ing.hop_total(self.hops)

	boiloff = property(boiloff_get, boil)
	total_ibu = property(extract, boil)

#RECIPE (target, actual)
class Recipe(object):
	def __init__(self):
		self.mash = Mash()
		self.boil = Boil()
		self.attenuation = 0.80
		self.batch_size = 6.0
		self.efficiency = 0.75
		self._og = 0.0
		self._fg = 0.0
		self._ibu = 0.0
		self._srm = 0.0
		self._abv = 0.0
		self._sparge_vol = 0.0
		self._strike = 0.0
		self._total_liquor = 0.0

	def og_get(self):
		return self._og

	def fg_get(self):
		return self._fg

	def srm_get(self):
		return self._srm

	def abv_get(self):
		return self._abv

	def totliq_get(self):
		return self._total_liquor

	def spvol_get(self):
		return self._sparge_vol

	def strike_get(self):
		return self._strike

	def lauter(self, malt, weight):
		self.mash.mash_in(malt, weight)
		self._og = 1.0 + (self.mash.gravity * (self.efficiency / self.batch_size))
		self._fg = ((self.og - 1.0) * (1.0 - self.attenuation)) + 1.0
		self._srm = ing.potential_srm(self.mash.grain, self.batch_size)
		self._abv = (1.05/0.79) * ((self.og - self.fg) / self.fg) * 100.0
		self._strike = self.mash.strike_temp
		self._total_liquor = (1.04 * self.batch_size) + self.mash.absorption + self.boil.boiloff + 0.25
		self._sparge_vol = self._total_liquor - self.mash.liquor

	def ibu_get(self):
		return self._ibu

	def hop(self, name, weight, time):
		self.boil.boil(name, weight, time)
		batch_const = (0.000125 ** (self.og - 1.0)) / self.batch_size
		self._ibu = self.boil.total_ibu * batch_const

	og = property(og_get, lauter)
	fg = property(fg_get, lauter)
	ibu = property(ibu_get, hop)
	srm = property(srm_get, lauter)
	abv = property(abv_get, lauter)
	total_liquor = property(totliq_get, lauter)
	sparge_vol = property(spvol_get, lauter)
	strike = property(strike_get, lauter)


#------------TESTING--------------#

a = Recipe()

a.lauter('United Kingdom - Maris Otter Pale', 14.0)
print "Sparge Volume (Gal): %.2f" % a.sparge_vol
a.lauter('American - Roasted Barley', 0.25)
print "Sparge Volume (Gal): %.2f" % a.sparge_vol
a.lauter('Rolled Oats', 1.0)
print "Sparge Volume (Gal): %.2f" % a.sparge_vol
a.lauter('United Kingdom - Pale Chocolate', 0.5)
print "Sparge Volume (Gal): %.2f" % a.sparge_vol
a.lauter('American - Caramel / Crystal 75L', 0.5)
print "Sparge Volume (Gal): %.2f" % a.sparge_vol
a.hop('Fuggles', 1.0, 90)
a.hop('Fuggles', 0.5, 30)
a.hop('Fuggles', 0.5, 10)
print a.mash.grain
print "Gravity: %.3f, %.3f" % (a.og, a.fg)
print "SRM: %.1f" % a.srm
print "IBU: %.1f" % a.ibu
print "ABV: %.1f" % a.abv
print "Mash Liquor (Gal): %.2f" % a.mash.liquor
print "Boiloff (Gal): %.2f" % a.boil.boiloff
print "Sparge Volume (Gal): %.2f" % a.sparge_vol
print "Total Liquor (Gal): %.2f" % a.total_liquor
print "Strike Temp (F): %.1f" % a.mash.strike_temp
a.mash.temp_set(80.0, 156.0)
print "Strike Temp (F): %.1f" % a.mash.strike_temp