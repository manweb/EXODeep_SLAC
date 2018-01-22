import numpy as np
from testPlot import APDDisplay
import pickle
import csv

#data = pickle.load(open('APDmaxSignalsNormalized_5003.p','rb'))
data = csv.reader(open('APDmaxSignalsNormalized_5003.csv'), delimiter=',')

dsp = APDDisplay()

for row in data:
	sample = map(float, row)
	dsp.DisplayAPDSignal(np.array(sample[0:74]))
	dsp.DisplayPosition(np.array(sample[74:77]),np.array(sample[74:77]))

	print("True position: x = %f, y = %f, z = %f"%(sample[74],sample[75],sample[76]))

	raw_input("Press enter to continue")

