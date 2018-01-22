import numpy as np
import csv
import argparse
import glob

def CountEvents(filenames):
	count = 0
	for inputFile in filenames:
		print("Opening file %s"%inputFile)
		with open(inputFile) as infile:
			for line in infile:
				count += 1

	print("Number of events: %i"%count)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputFile', type=str)

	args = parser.parse_args()

	filenames = glob.glob(args.inputFile)

	CountEvents(filenames)

