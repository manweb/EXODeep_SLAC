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

def GetMeanFromFile(meanFile):
        mean = np.genfromtxt(open(meanFile), delimiter=',')
        print mean

        return mean

def CreateTestSet(filenames, nEvents, meanFile, subtractMean, outFile):
	totalEvents = CountNumberOfEvents(filenames)

	print('Creating test set...')

	nFeatures = 74*350
	if subtractMean:
		print('Reading mean file...')
		mean = GetMeanFromFile(meanFile)
	else:
		mean = np.zeros(nFeatures)

	normalizedData = np.zeros(nFeatures+5)

	count = 0
	for inputFile in filenames:
		testFile = inputFile.replace('Flattened', 'Flattened_Cut')
		if not os.path.isfile(testFile):
			print('    File %s not found'%testFile)

			continue

		print('    Processing file %s'%testFile)

		nTrain = sum(1 for row in open(inputFile))
		nTest = sum(1 for row in open(testFile))
		print('    Number of training events in this file: %i'%nTrain)
		print('    Number of test events in this file: %i'%nTest)

		keep_events = int(float(nTrain)/float(totalEvents)*float(nEvents))
		if keep_events < 10:
			keep_events = 10

		if keep_events > nTest:
			keep_events = nTest

		print('    Selecting %i events'%keep_events)
		step = np.floor(float(nTest)/float(keep_events))
		print('    Step: %i'%step)
		with open(testFile) as infile:
			idx = 0
			for line in infile:
				if not idx % step == 0:
					idx += 1
					continue

				x = np.fromstring(line, dtype=float, sep=',')
				normalizedData[0:nFeatures] = x[0:nFeatures] - mean
                                normalizedData[nFeatures:nFeatures+5] = x[nFeatures:nFeatures+5]

				option = 'a'
				if count == 0:
					option = 'w'

				f = open(outFile, option)
                                f.write(",".join(np.char.mod('%f', normalizedData))+'\n')
                                f.close()

				count += 1
				idx += 1

				print count

	print('%i events written'%count)

def CreateTestSetFiducial(filenames, subtractMean, outFile):
	print('Creating test set with fiducial cut...')

	nFeatures = 74*350
	if subtractMean:
		print('Reading mean file...')
		mean = GetMeanFromFile(meanFile)
	else:
		mean = np.zeros(nFeatures)

	normalizedData = np.zeros(nFeatures+5)

	fv = 50
	fv_x1 = 100
	fv_y1 = 0
	fv_z1 = 100

	fv_x2 = 0
	fv_y2 = 100
	fv_z2 = 100

	fv_x3 = 0
	fv_y3 = 0
	fv_z3 = -100

	fv_E = 2615
	fv_dE = 160

	outFile1 = outFile.replace('.csv','_fv1.csv')
	outFile2 = outFile.replace('.csv','_fv2.csv')
	outFile3 = outFile.replace('.csv','_fv3.csv')

	count1 = 0
	count2 = 0
	count3 = 0
	for inputFile in filenames:
		print('Processing file %s'%inputFile)

		with open(inputFile) as infile:
			for line in infile:
				x = np.fromstring(line, dtype=float, sep=',')
                                normalizedData[0:nFeatures] = x[0:nFeatures] - mean
                                normalizedData[nFeatures:nFeatures+5] = x[nFeatures:nFeatures+5]

				fx = x[nFeatures]
				fy = x[nFeatures+1]
				fz = x[nFeatures+2]
				fE = x[nFeatures+3]

				if fx > fv_x1-fv/2 and fx < fv_x1+fv/2 and fy > fv_y1-fv/2 and fy < fv_y1+fv/2 and fz > fv_z1-fv/2 and fz < fv_z1+fv/2 and fE > fv_E-fv_dE and fE < fv_E+fv_dE:
					option = 'a'
                                	if count1 == 0:
                                        	option = 'w'

                                	f = open(outFile1, option)
                                	f.write(",".join(np.char.mod('%f', normalizedData))+'\n')
                                	f.close()

					count1 += 1
				elif fx > fv_x2-fv/2 and fx < fv_x2+fv/2 and fy > fv_y2-fv/2 and fy < fv_y2+fv/2 and fz > fv_z2-fv/2 and fz < fv_z2+fv/2 and fE > fv_E-fv_dE and fE < fv_E+fv_dE:
					option = 'a'
                                	if count2 == 0:
                                        	option = 'w'

                                	f = open(outFile2, option)
                                	f.write(",".join(np.char.mod('%f', normalizedData))+'\n')
                                	f.close()

					count2 += 1
				elif fx > fv_x3-fv/2 and fx < fv_x3+fv/2 and fy > fv_y3-fv/2 and fy < fv_y3+fv/2 and fz > fv_z3-fv/2 and fz < fv_z3+fv/2 and fE > fv_E-fv_dE and fE < fv_E+fv_dE:
					option = 'a'
                                	if count3 == 0:
                                        	option = 'w'

                                	f = open(outFile3, option)
                                	f.write(",".join(np.char.mod('%f', normalizedData))+'\n')
                                	f.close()

					count3 += 1

	print('Done creating test files')
	print('Events written:')
	print('		fv1: %i'%count1)
	print('		fv2: %i'%count2)
	print('		fv3: %i'%count3)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputFile', type=str)
	parser.add_argument('--nEvents', type=int, default=1000)
	parser.add_argument('--meanFile', type=str, default='')
	parser.add_argument('--subtractMean', action='store_true')
	parser.add_argument('--outFile', type=str)
	parser.add_argument('--fiducialCut', action='store_true')

	args = parser.parse_args()

	filenames = glob.glob(args.inputFile)

	if args.fiducialCut:
		CreateTestSetFiducial(filenames, args.subtractMean, args.outFile)
	else:
		CreateTestSet(filenames, args.nEvents, args.meanFile, args.subtractMean, args.outFile)

