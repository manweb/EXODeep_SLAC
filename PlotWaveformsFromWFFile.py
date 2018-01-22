import ROOT
import numpy as np
import csv
import matplotlib.pyplot as plt
import argparse

def PlotWaveform(inputFile):
	histos = []
	
	nsamples = 350
	offset = 50
	
	with open(inputFile) as infile:
		for line in infile:
			x = np.fromstring(line, dtype=float, sep=',')

			plt.close('all')
		
			fig = plt.figure(figsize=(15,5))
			ax1 = fig.add_subplot(1,3,1)
			ax2 = fig.add_subplot(1,3,2)
			ax3 = fig.add_subplot(1,3,3)
		
			wf = x[0:74*350]
			labels = x[74*350:74*350+5]
			wfR = np.reshape(wf,(74,nsamples))
			wfRoffsetY = wfR-np.mean(wfR[:,:100],axis=1).reshape(74,1)+np.arange(74*offset,0,-offset).reshape(74,1)
			wfRoffsetX = np.array([np.arange(nsamples),]*74)
		
			ax1.imshow(wfR, interpolation='nearest', aspect='auto', cmap='summer')
			ax2.plot(wfRoffsetX.T,wfRoffsetY.T,c='black')
			ax3.plot(np.arange(nsamples),np.sum(wfR-np.mean(wfR[:,:100],axis=1).reshape(74,1),axis=0),c='black')

			ax1.set_xlabel('time ($\mu$s)')
			ax1.set_ylabel('channel')

			ax2.set_xlabel('time ($\mu$s)')
			ax2.set_ylabel('channel + offset', labelpad=10)

			ax3.set_xlabel('time ($\mu$s)')
			ax3.set_ylabel('amplitude (a.u.)', labelpad=10)

			plt.subplots_adjust(left=0.05, right=0.95, wspace=0.3)

			#plt.title('E_c = %.2f, E_s = %.2f, x = (%.2f,%.2f,%.2f)'%(labels[3], labels[4], labels[0], labels[1], labels[2]))

			print('E_c = %.2f, E_s = %.2f, x = (%.2f,%.2f,%.2f)'%(labels[3], labels[4], labels[0], labels[1], labels[2]))

			plt.show(block=False)
		
			raw_input("Enter...")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputFile', type=str)

	args = parser.parse_args()

	PlotWaveform(args.inputFile)

