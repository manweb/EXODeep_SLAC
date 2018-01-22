import numpy as np
from numpy import genfromtxt
import csv
import matplotlib.pyplot as plt

inputFile = 'FlattenedNormalizedData/APDWFSignalsEnergyThreshold_5003_5020_Mean_Flattened.csv'

data = genfromtxt(inputFile, delimiter=',')

image = data.reshape((74,350))

fig = plt.figure(figsize=(5,5))

plt.imshow(image, interpolation='nearest', aspect='auto', cmap='summer')
plt.show()

