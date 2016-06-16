import pandas as p 
import math as m

gpath = 'C:/Users/McNutty/PyScripts/Data/gristlist.csv'
hpath = 'C:/Users/McNutty/PyScripts/Data/hoplist.csv'

grist = p.read_csv(gpath, header = 0)
hops = p.read_csv(hpath, header = 0)


def potential_sg(malt, weight):
	index = grist[grist['D_NAME'] == malt].index.tolist()[0]
	ppg = grist.POT_SG.iloc[index] - 1.0
	return ppg * weight

def mash_sg(mash):
	sg = 0.0
	for malt, weight in mash.items():
		sg += potential_sg(malt, weight)
	return sg

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

def hop_aa(name, pct_aa):
	if pct_aa == None:
		index = hops[hops['NAME'] == name].index.tolist()[0]
		return hops.PCT_AA.iloc[index]
	else:
		return pct_aa

def hop_const(hoptype):
	if hoptype == 'Pellet':
		return 1.3
	else:
		return 1.0

def hop_total(hops):
	total = 0
	for i in hops.keys():
		total += hops[i].total_ibus
	return total

class HopAddition(object):
	def __init__(self, time):
		self.hops = {} # 'hop name':%AA
		self.time = time
		self._total_ibus = 0.0

	def extract(self):
		return self._total_ibus

	def boiled(self, name, weight, pct_aa = None, hoptype = 'Pellet'):
		aa = hop_aa(name, pct_aa)
		typeconst = hop_const(hoptype)
		ibus = typeconst * aa * weight * 7490 * 1.65 * (1.0 - m.exp(-0.04 * self.time)) / 4.15
		self.hops[name] = ibus
		self._total_ibus = sum(self.hops.values())

	total_ibus = property(extract, boiled)