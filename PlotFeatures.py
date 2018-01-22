import numpy as np
import csv
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob
import argparse

def PlotLabels(filenames):
	reader = csv.reader(open(filenames[0]), delimiter=',')
	#nFeatures = len(next(reader)) - 4
	nFeatures = 74*350
	print("Number of features: %i"%nFeatures)

        data1 = []
	data2 = []
	data3 = []
	data4 = []
        for inputFile in filenames:
                print("Processing file %s"%inputFile)
		nEvents = sum(1 for row in open(inputFile))
		count = 0
                with open(inputFile) as infile:
                        for line in infile:
                                x = np.fromstring(line, dtype=float, sep=',')
				cols = np.reshape(x[0:nFeatures],(74,350))
                                data1.append([cols[0,5], cols[0,10], cols[0,15], cols[0,280]])
				data2.append([cols[1,5], cols[1,10], cols[1,15], cols[1,280]])
				data3.append([cols[2,5], cols[2,10], cols[2,15], cols[2,280]])
				data4.append([cols[3,5], cols[3,10], cols[3,15], cols[3,280]])

				count += 1

				if count%1000 == 0:
					print("%i events processed (%.2f%%)"%(count, float(count)/float(nEvents)*100))

	d1 = np.asarray(data1)
	d2 = np.asarray(data2)
	d3 = np.asarray(data3)
	d4 = np.asarray(data4)

	fig = plt.figure(figsize=(8,8))
	ax1 = fig.add_subplot(2,2,1)
	ax2 = fig.add_subplot(2,2,2)
	ax3 = fig.add_subplot(2,2,3)
	ax4 = fig.add_subplot(2,2,4)

	ax1.hist(d1, np.linspace(-20,50,70), histtype='step')
	ax2.hist(d2, np.linspace(-20,50,70), histtype='step')
	ax3.hist(d3, np.linspace(-20,50,70), histtype='step')
	ax4.hist(d4, np.linspace(-20,50,70), histtype='step')

	"""ax1.set_xlim([-200, 200])
	ax1.set_ylim(ymin=0)
	ax2.set_xlim([-200, 200])
	ax2.set_ylim(ymin=0)
	ax3.set_xlim([-200, 200])
	ax3.set_ylim(ymin=0)
	ax4.set_xlim([300, 3500])
	ax4.set_ylim(ymin=0)
"""
	"""ax1.set_xlabel('x (mm)')
	ax2.set_xlabel('y (mm)')
	ax3.set_xlabel('z (mm)')
	ax4.set_xlabel('energy (keV)')
"""
	plt.show()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputFile', type=str)

	args = parser.parse_args()

	filenames = glob.glob(args.inputFile)

	PlotLabels(filenames)

