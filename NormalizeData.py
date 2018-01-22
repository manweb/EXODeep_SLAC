import csv
import argparse
import numpy as np
import math
import glob

def GetMean(filenames, nFeatures):
	print("Calculating mean...")
	mean = np.zeros(nFeatures)

	allCount = 0
	for inputFile in filenames:
		print("Processing file %s"%inputFile)
		nEvents = sum(1 for row in open(inputFile))
		count = 0
		with open(inputFile) as infile:
			for line in infile:
				x = np.fromstring(line, dtype=float, sep=',')
				mean += x[0:nFeatures]

				count += 1
				allCount += 1

				if count%1000 == 0:
					print("%i (%.2f%%) events processed"%(count,float(count)/float(nEvents)*100))

	mean /= float(allCount)
	print mean

	return mean

def GetStd(filenames, nFeatures, mean):
	print("Calculating standard deviation...")
	std = np.zeros(nFeatures)

	allCount = 0
	for inputFile in filenames:
		print("Processing file %s"%inputFile)
		nEvents = sum(1 for row in open(inputFile))
        	count = 0
        	with open(inputFile) as infile:
        	        for line in infile:
        	                x = np.fromstring(line, dtype=float, sep=',')
        	                std += (x[0:nFeatures] - mean)*(x[0:nFeatures] - mean)

        	                count += 1
				allCount += 1

        	                if count%1000 == 0:
        	                        print("%i (%.2f%%) events processed"%(count,float(count)/float(nEvents)*100))

        std /= float(allCount)
	std = np.sqrt(std)
	print std

	return std

def GetMeanFromFile(meanFile):
	mean = np.genfromtxt(open(meanFile), delimiter=',')
	print mean

	return mean

def NormalizeData(filenames, meanFile, outputFile, noNormalize = False, subtractMean = False, mergeFiles = False):
	reader = csv.reader(open(filenames[0]), delimiter=',')
	#nFeatures = len(next(reader)) - 4
	nFeatures = 74*350
	print("Number of features: %i"%nFeatures)

	if meanFile:
		if subtractMean:
			mean = GetMeanFromFile(meanFile)
		else:
			mean = GetMean(filenames, nFeatures)

			f = open(meanFile, 'w')
        		f.write(",".join(np.char.mod('%f', mean)))
        		f.close()
	else:
		mean = np.zeros(nFeatures)

	std = np.ones(nFeatures)
	if not noNormalize:
		std = GetStd(filenames, nFeatures, mean)

	print("Normalizing data...")
	normalizedData = np.zeros(nFeatures+5)

	if mergeFiles:
		outFile = outputFile
		count = 0

	for inputFile in filenames:
		print("Processing file %s"%inputFile)
		if not mergeFiles:
			outFile = inputFile.replace(".csv", "_FeatureNormalized.csv")
        		count = 0
		nEvents = sum(1 for row in open(inputFile))
        	with open(inputFile) as infile:
        	        for line in infile:
        	                x = np.fromstring(line, dtype=float, sep=',')
        	                normalizedData[0:nFeatures] = (x[0:nFeatures] - mean) / std
				normalizedData[nFeatures:nFeatures+5] = x[nFeatures:nFeatures+5]

				option = 'a'
				if count == 0:
					option = 'w'

				f = open(outFile, option)
				f.write(",".join(np.char.mod('%f', normalizedData))+'\n')
				f.close()

        	                count += 1

        	                if count%1000 == 0:
        	                        print("%i (%.2f%%) events processed"%(count,float(count)/float(nEvents)*100))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputFile', type=str)
	parser.add_argument('--meanFile', type=str, default='')
	parser.add_argument('--noNormalize', action='store_true')
	parser.add_argument('--subtractMean', action='store_true')
	parser.add_argument('--mergeFiles', action='store_true')
	parser.add_argument('--outputFile', type=str, default='merged.csv')

	args = parser.parse_args()

	filenames = glob.glob(args.inputFile)

	NormalizeData(filenames, args.meanFile, args.outputFile, args.noNormalize, args.subtractMean, args.mergeFiles)

