import csv
import argparse
import numpy as np
import math
import glob
import os

def CountNumberOfEvents(filenames):
        print('Counting number of training events...')

        totalEvents = 0
        for inputFile in filenames:
                nEvents = sum(1 for row in open(inputFile))

                totalEvents += nEvents

        print('    Number of events: %i'%totalEvents)

        return totalEvents

def CreateTrainTestSet(filenames, nEvents, outFile):
	totalEvents = CountNumberOfEvents(filenames)
	shuffle = np.arange(totalEvents)
	np.random.shuffle(shuffle)

	if nEvents > totalEvents:
		print('Not enough data')
		return

	trainSetName = outFile.replace('.csv','_Train.csv')
	testSetName = outFile.replace('.csv','_Test.csv')

	count = 0
	countTrain = 0
	countTest = 0
	for inputFile in filenames:
		print('    Processing file %s'%inputFile)

		with open(inputFile) as infile:
			for line in infile:
				x = np.fromstring(line, dtype=float, sep=',')
	
				if shuffle[count] < totalEvents - nEvents:
					option = 'a'
	                                if countTrain == 0:
	                                        option = 'w'
	
					f = open(trainSetName, option)
	                                f.write(",".join(np.char.mod('%f', x))+'\n')
	                                f.close()
	
					countTrain += 1
				else:
					option = 'a'
	                                if countTest == 0:
	                                        option = 'w'
	
					f = open(testSetName, option)
	                                f.write(",".join(np.char.mod('%f', x))+'\n')
	                                f.close()
	
					countTest += 1
	
				count += 1

	print('Total number of events: %i'%totalEvents)
	print('Number of training events: %i'%countTrain)
	print('Number of test events: %i (%.2f%%)'%(countTest,float(countTest)/float(totalEvents)*100.0))

if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('--inputFile', type=str)
        parser.add_argument('--nEvents', type=int, default=1000)
	parser.add_argument('--outFile', type=str)

	args = parser.parse_args()

	filenames = glob.glob(args.inputFile)

	CreateTrainTestSet(filenames, args.nEvents, args.outFile)
