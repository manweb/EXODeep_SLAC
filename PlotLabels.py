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

        dataX = []
	dataY = []
	dataZ = []
	dataE = []
	dataES = []
	dataESSum = []
        for inputFile in filenames:
                print("Processing file %s"%inputFile)
		nEvents = sum(1 for row in open(inputFile))
		count = 0
                with open(inputFile) as infile:
                        for line in infile:
                                x = np.fromstring(line, dtype=float, sep=',')
				cols = np.reshape(x[0:nFeatures],(74,350))
                                dataX.append(x[nFeatures])
				dataY.append(x[nFeatures+1])
				dataZ.append(x[nFeatures+2])
				dataE.append(x[nFeatures+3])
				dataES.append(x[nFeatures+4])
				dataESSum.append(np.max(np.sum(cols,axis=0)))

				count += 1

				if count%1000 == 0:
					print("%i events processed (%.2f%%)"%(count, float(count)/float(nEvents)*100))

	fig = plt.figure(figsize=(12,8))
	ax1 = fig.add_subplot(2,3,1)
	ax2 = fig.add_subplot(2,3,2)
	ax3 = fig.add_subplot(2,3,3)
	ax4 = fig.add_subplot(2,3,4)
	ax5 = fig.add_subplot(2,3,5)
	ax6 = fig.add_subplot(2,3,6)

	ax1.hist(dataX, np.linspace(-200,200,80), histtype='step', color='b')
	ax2.hist(dataY, np.linspace(-200,200,80), histtype='step', color='b')
	ax3.hist(dataZ, np.linspace(-200,200,80), histtype='step', color='b')
	ax4.hist(dataE, np.linspace(300,3500,80), histtype='step', color='b')
	ax5.hist(dataES, np.linspace(300,3500,80), histtype='step', color='b')

	H, xedges, yedges = np.histogram2d(dataE, dataES, bins=(np.linspace(0,3500,80), np.linspace(0,3500,80)))
	ax6.imshow(np.flipud(H.T), interpolation='nearest', extent=[0, 3500, 0, 3500], aspect='auto', cmap='summer')

	ax1.set_xlim([-200, 200])
	ax1.set_ylim(ymin=0)
	ax2.set_xlim([-200, 200])
	ax2.set_ylim(ymin=0)
	ax3.set_xlim([-200, 200])
	ax3.set_ylim(ymin=0)
	ax4.set_xlim([300, 3500])
	ax4.set_ylim(ymin=0)
	ax5.set_xlim([300, 3500])
	ax5.set_ylim(ymin=0)
	#ax6.set_xlim([300, 3500])
	#ax6.set_ylim(ymin=0)

	ax1.set_xlabel('x (mm)')
	ax2.set_xlabel('y (mm)')
	ax3.set_xlabel('z (mm)')
	ax4.set_xlabel('energy (keV)')
	ax5.set_xlabel('scintillation energy (keV)')

	plt.show()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputFile', type=str)

	args = parser.parse_args()

	filenames = glob.glob(args.inputFile)

	PlotLabels(filenames)

