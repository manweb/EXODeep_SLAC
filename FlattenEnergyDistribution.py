import numpy as np
import csv
import matplotlib.pyplot as plt
import argparse
import glob
from scipy.stats import gaussian_kde

def GetEnergyDistribution(filenames, nFeatures):
        data = []
        for inputFile in filenames:
                print("Processing file %s"%inputFile)
		nEvents = sum(1 for row in open(inputFile))
		count = 0
                with open(inputFile) as infile:
                        for line in infile:
                                x = np.fromstring(line, dtype=float, sep=',')
                                data.append(x[nFeatures+3])

				count += 1

				if count%1000 == 0:
					print("%i events processed (%.2f%%)"%(count, float(count)/float(nEvents)*100))

	return list(np.asarray(data))

def Flatten(filenames):
	reader = csv.reader(open(filenames[0]), delimiter=',')
	nFeatures = len(next(reader)) - 4
	print("Number of features: %i"%nFeatures)

	energyDistribution = GetEnergyDistribution(filenames, nFeatures)

	pdf = gaussian_kde(energyDistribution)
	pdf.covariance_factor = lambda : .02
	pdf._compute_covariance()
	x = np.linspace(500,3500,3000)
	idx = np.argmin(pdf(x[600:2100]))
	xMin = x[idx+600]
	minimum = pdf(x[idx+600])
	print("Minimum %f at: %i"%(minimum,xMin))

	flattenedData = []
	for inputFile in filenames:
		print("Processing file: %s"%inputFile)
		outFile = inputFile.replace(".csv", "_Flattened.csv")
		nEvents = sum(1 for row in open(inputFile))
		count = 0
		nDropped = 0
		with open(inputFile) as infile:
			for line in infile:
				x = np.fromstring(line, dtype=float, sep=',')
				energy = x[nFeatures+3]
				prob = minimum/pdf(energy)
				if prob > 1.0:
					prob = 1.0
				rand_sample = np.random.uniform(0,1,1)

				if rand_sample > prob:
					nDropped += 1
					continue

				option = 'a'
				if count == 0:
					option = 'w'

				f = open(outFile, option)
				f.write(",".join(np.char.mod('%f', x))+'\n')
				f.close()

				flattenedData.append(energy)

				count += 1

				if count%1000 == 0:
					print("%i events processed, %i events dropped"%(count,nDropped))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputFile', type=str)

	args = parser.parse_args()

	filenames = glob.glob(args.inputFile)

	Flatten(filenames)

