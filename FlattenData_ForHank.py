import numpy as np
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
import glob
from scipy.stats import gaussian_kde

def GetEnergyDistribution(filenames, nFeatures):
        dataX = []
	dataY = []
	dataZ = []
	dataE = []

	# loop over all files, retrieve the position (x,y,z) and energy label and store them in
	# the corresponding arrays
        for inputFile in filenames:
                print("Processing file %s"%inputFile)
		nEvents = sum(1 for row in open(inputFile))
		count = 0
                with open(inputFile) as infile:
                        for line in infile:
                                x = np.fromstring(line, dtype=float, sep=',')
                                dataX.append(x[nFeatures])
				dataY.append(x[nFeatures+1])
				dataZ.append(x[nFeatures+2])
				dataE.append(x[nFeatures+3])

				count += 1

				if count%1000 == 0:
					print("%i events processed (%.2f%%)"%(count, float(count)/float(nEvents)*100))

	return list(np.asarray(dataX)), list(np.asarray(dataY)), list(np.asarray(dataZ)), list(np.asarray(dataE))

def Flatten(filenames, plotName, onlyPlot, marginFactor):
	nFeatures = 74*350
	print("Number of features: %i"%nFeatures)

	# Get the event distribution from the data. The position (x,y,z) and energy distributions are stored
	# separately in numpy arrays
	dataX, dataY, dataZ, dataE = GetEnergyDistribution(filenames, nFeatures)

	# Stack data into matrix. Each row corresponds to the (x,y,z,E) of that event
	# The data is also split into a x,y matrix and z,E matrix which is used for display
	# purposes
	data = np.vstack([dataX, dataY, dataZ, dataE])
	dataXY = np.vstack([dataX, dataY])
	dataZE = np.vstack([dataZ, dataE])

	# Create the gaussian KDE for the data
	pdf = gaussian_kde(data)
	pdfXY = gaussian_kde(dataXY)
	pdfZE = gaussian_kde(dataZE)
	#pdf.covariance_factor = lambda : .02
	#pdf._compute_covariance()

	# Create a mesh within the 4 dimensional space with 20 points in each dimension
	# The min and max in each dimension can be changed to only evaluate the PDF within
	# these boundaries and not consider the region outside of that boundaries for
	# finding the minimum
	X, Y, Z, E = np.mgrid[0:160:20j, -160:160:20j, -180:180:20j, 1000:2500:20j]
	positions = np.vstack([X.ravel(), Y.ravel(), Z.ravel(), E.ravel()])

	# The meshes in x,y and z,E space are used for display purposes
	XY_x, XY_y = np.mgrid[-200:200:80j, -200:200:80j]
	positionsXY = np.vstack([XY_x.ravel(), XY_y.ravel()])

	ZE_z, ZE_e = np.mgrid[-200:200:80j, 700:3500:80j]
	positionsZE = np.vstack([ZE_z.ravel(), ZE_e.ravel()])

	# Add a radial cut. This is done by adding a large number to all points outside
	# of the cut. This regioin will be neglected when searching for the minimum
	R = X.ravel()**2 + Y.ravel()**2
	RCut = (R > 160.0**2).astype(int)*1e6

	# The same approach can be done for a z cut if desired
	ZCut = (np.absolute(Z.ravel()) < 50.0).astype(int)*1e6

	# Evaluate the PDF at the points of the mesh
	pdfEval = pdf(positions) + RCut + ZCut
	pdfEvalXY = np.reshape(pdfXY(positionsXY).T, XY_x.shape)
	pdfEvalZE = np.reshape(pdfZE(positionsZE).T, ZE_z.shape)

	# Find the point in the mesh with smallest probability
	idx = np.argmin(pdfEval)
	minimum = pdfEval[idx]

	print data.shape
	print positions.shape
	print RCut.shape
	print pdfEval.shape
	print("Minimum %.15f at: (%f,%f,%f,%f)"%(minimum,positions[0,idx],positions[1,idx],positions[2,idx],positions[3,idx]))

	fig = plt.figure(figsize=(10,15))
	ax1 = fig.add_subplot(3,2,1)
	ax2 = fig.add_subplot(3,2,2)
	ax3 = fig.add_subplot(3,2,3)
	ax4 = fig.add_subplot(3,2,4)
	ax5 = fig.add_subplot(3,2,5)
	ax6 = fig.add_subplot(3,2,6)

	ax1.imshow(np.rot90(pdfEvalXY), interpolation='nearest', aspect='auto', cmap='summer', extent=[-200, 200, -200, 200])
	ax2.imshow(np.flipud(pdfEvalZE), interpolation='nearest', aspect='auto', cmap='summer', extent=[700, 3500, -200, 200])

	ax1.plot(positions[0,idx], positions[1,idx], 'x', color='b')
	ax2.plot(positions[3,idx], positions[2,idx], 'x', color='b')

	ax3.hist(dataX, np.linspace(-200,200,40), histtype='step', color='b')
	ax4.hist(dataY, np.linspace(-200,200,40), histtype='step', color='b')
	ax5.hist(dataZ, np.linspace(-200,200,40), histtype='step', color='b')
	ax6.hist(dataE, np.linspace(700,3500,40), histtype='step', color='b')

	ax1.set_xlim([-200, 200])
	ax1.set_ylim([-200, 200])
	ax2.set_xlim([700, 3500])
	ax2.set_ylim([-200, 200])

	ax3.set_xlim([-200, 200])
	ax3.set_ylim(ymin=0)
	ax4.set_xlim([-200, 200])
	ax4.set_ylim(ymin=0)
	ax5.set_xlim([-200, 200])
	ax5.set_ylim(ymin=0)
	ax6.set_xlim([700, 3500])
	ax6.set_ylim(ymin=0)

	ax1.set_xlabel('x (mm)')
	ax1.set_ylabel('y (mm)')
	ax2.set_xlabel('energy (keV)')
	ax2.set_ylabel('z (mm)')
	ax3.set_xlabel('x (mm)')
	ax4.set_xlabel('y (mm)')
	ax5.set_xlabel('z (mm)')
	ax6.set_xlabel('energy (keV)')

	#plt.show()
	plt.savefig(plotName)

	if onlyPlot:
		return

	# Loop over the data and throw out events in order to flatten the distribution.
	# In order to throw out the least amount of events, an event at or below the minimal
	# PDF value should always be kept. This is achieved by scaling the PDF value of the
	# current event by the minimum PDF value. The event is then kept with probability
	# prob = minimum/pdf(current event). If a margin factor is chosen the probablility
	# of keeping the event is increased by this factor. This intorduces some non-uniformity
	# After selecting whether to keep or throw out the event, the event gets written into
	# a new file. One file for the kept events and one file for the thrown out events.
	# The thrown out events can be used for testing
	flattenedData = []
	for inputFile in filenames:
		print("Processing file: %s"%inputFile)
		outFile = inputFile.replace(".csv", "_Flattened.csv")
		outFileCut = inputFile.replace(".csv", "_Flattened_Cut.csv")
		nEvents = sum(1 for row in open(inputFile))
		count = 0
		nDropped = 0
		with open(inputFile) as infile:
			for line in infile:
				x = np.fromstring(line, dtype=float, sep=',')
				current_X = x[nFeatures]
				current_Y = x[nFeatures+1]
				current_Z = x[nFeatures+2]
				current_E = x[nFeatures+3]
				current_data = np.vstack([current_X, current_Y, current_Z, current_E])
				prob = minimum/pdf(current_data)*marginFactor
				if prob > 1.0:
					prob = 1.0
				rand_sample = np.random.uniform(0,1,1)

				if rand_sample > prob:
					option = 'a'
                                	if nDropped == 0:
                                        	option = 'w'

					f = open(outFileCut, option)
                                	f.write(",".join(np.char.mod('%f', x))+'\n')
                                	f.close()
	
					nDropped += 1
					continue

				option = 'a'
				if count == 0:
					option = 'w'

				f = open(outFile, option)
				f.write(",".join(np.char.mod('%f', x))+'\n')
				f.close()

				#flattenedData.append(energy)

				count += 1

				if count%1000 == 0:
					print("%i events processed, %i events dropped"%(count,nDropped))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputFile', type=str)
	parser.add_argument('--plotName', type=str, default='APDWFSpectra.png')
	parser.add_argument('--onlyPlot', action='store_true')
	parser.add_argument('--marginFactor', type=float, default=1.0)

	args = parser.parse_args()

	onlyPlot = False
	if args.onlyPlot:
		onlyPlot = True

	filenames = glob.glob(args.inputFile)

	Flatten(filenames, args.plotName, onlyPlot, args.marginFactor)

