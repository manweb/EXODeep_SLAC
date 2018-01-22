import numpy as np
import math
#import h5py
import cPickle as pickle
import ROOT
import os, fnmatch
import argparse

def GetAPDSignals(waveformData,normalize):
	numAPD = 74
	minChannel = 152
	nsamples = waveformData.fNumSamples
	nWF = waveformData.GetNumWaveforms()

	channelData = np.zeros((numAPD,nsamples))
	channels = np.zeros(numAPD)
	sumData = np.zeros(nsamples)
	sumHisto = ROOT.TH1I("h_sum","h_sum",nsamples,0,nsamples)

	apdSignals = np.zeros(numAPD)

	n = 0
	for i in range(nWF):
		wf = waveformData.GetWaveform(i)
		ch = wf.fChannel

		if ch < minChannel:
			continue

		wf.Decompress()

		BL = 0.0
		for k in range(nsamples/3):
			BL += wf.At(k)
		BL /= (nsamples/3)

		for k in range(nsamples):
			np.put(channelData, n*nsamples+k, wf.At(k)-BL)
			np.put(sumData, k, sumData[k]+wf.At(k)-BL)

		np.put(channels, n, ch-minChannel)

		n += 1

	maxBin = np.argmax(sumData)
	apdMax = np.max(sumData)
	rms = 0
	for k in range(nsamples):
		rms += sumData[k]*sumData[k]
	rms /= nsamples
	rms = math.sqrt(rms)
	
	if apdMax < 5*rms:
		return apdSignals

	if not normalize:
		apdMax = 1.0

	for k in range(len(channels)):
		np.put(apdSignals, channels[k], channelData[k,maxBin]/apdMax)

	return apdSignals

def PullData(runNumber,maxEvents,normalize,energyThreshold,applyFiducialCut=False):
	waveformFiles = '/nfs/slac/g/exo_data[wildcard]/exo_data/data/WIPP/root/[runNumber]/'
	preprocessedFiles = '/nfs/slac/g/exo_data4/users/Energy/data/WIPP/preprocessed/2017_Phase1_v2/ForCalibration/run_[runNumber]_tree.root'
	
	ROOT.gSystem.Load('../EXOEnergy/lib/libEXOEnergy.so')
	
	infoRuns = ROOT.EXOSourceRunsPolishedInfo('../EXOEnergy/data/SourceRunsInfo_Phase1_20170411.txt')
	
	print('Opening preprocessed file %s'%(preprocessedFiles.replace('[runNumber]','%i'%runNumber)))
	fProcessed = ROOT.TFile(preprocessedFiles.replace('[runNumber]','%i'%runNumber),'READ')
	tProcessed = fProcessed.Get('dataTree')
	
	print('Opening waveform files in directory %s'%(waveformFiles.replace('[runNumber]','%i'%runNumber)))
	tWF = ROOT.TChain('tree','tree')

	for i in range(2,8):
		wfFile = waveformFiles.replace('[wildcard]','%i'%i)+'*.root'
		tWF.Add(wfFile.replace('[runNumber]','%i'%runNumber))
	
	ed = ROOT.EXOEventData()
	tWF.SetBranchAddress('EventBranch',ed)
	
	tWF.BuildIndex("EventBranch.fRunNumber","EventBranch.fEventNumber")

	cut = "nsc==1 && multiplicity == 1"

	if applyFiducialCut:
		cut += " && TMath::Abs(cluster_z) > 10.0 && TMath::Abs(cluster_z) < 182.0 && TMath::Sqrt(cluster_x*cluster_x+cluster_y*cluster_y) < 162.0"

	if energyThreshold > 0.0:
		cut += " && e_charge > %f"%energyThreshold

	n = tProcessed.Draw("eventNum",cut,"goff")
        eventNumbers = np.copy(np.frombuffer(tProcessed.GetV1(), count=n))

        n = tProcessed.Draw("cluster_x:cluster_y:cluster_z:e_charge",cut,"goff")
        cluster_x = np.copy(np.frombuffer(tProcessed.GetV1(), count=n))
        cluster_y = np.copy(np.frombuffer(tProcessed.GetV2(), count=n))
        cluster_z = np.copy(np.frombuffer(tProcessed.GetV3(), count=n))
        e_charge = np.copy(np.frombuffer(tProcessed.GetV4(), count=n))
	
	data = np.zeros(78)

	nEvents = 0
	nEventsDropped = 0
	for i in range(n):
		if (tWF.GetEntryWithIndex(runNumber,int(eventNumbers[i])) < 0):
			print("Waveform for event %i in run %i not found"%(tProcessed.GetV1()[i],runNumber))
			continue
	
		apdSignals = GetAPDSignals(ed.GetWaveformData(),normalize)
	
		if not apdSignals.any() or cluster_x[i] == -999 or cluster_y[i] == -999 or cluster_z[i] == -999:
			#print("APD signal for event %i in run %i is below threshold"%(tProcessed.GetV1()[i],runNumber))
			nEventsDropped += 1
			continue
	
		apdSignals = np.append(apdSignals,np.array([cluster_x[i], cluster_y[i], cluster_z[i], e_charge[i]]))
	
		#if not data.any():
		#	data = apdSignals
		#else:
		#	data = np.vstack((data,apdSignals))

		nEvents += 1

		option = 'a'
		if nEvents == 0:
			option = 'w'

		row = ''
		for k in range(len(apdSignals)):
			row += '%f'%apdSignals[k]
			if not k == len(apdSignals)-1:
				row += ','
		row += '\n'

		fname = 'APDmaxSignalsEnergyThreshold'
		if normalize:
			fname = 'APDmaxSignalsEnergyThresholdNormalized'

		if applyFiducialCut:
			fname = 'APDmaxSignalsEnergyThresholdCut'

		f = open('%s_%i.csv'%(fname,runNumber),option)
		f.write(row)
		f.close()

		if nEvents%100==0:
			print("%i events processed, %i events dropped"%(nEvents,nEventsDropped))

		if nEvents > maxEvents:
			break

	#print("Writing data. Total events: %i, Events dropped: %i"%(nEvents,nEventsDropped))
	#pickle.dump(data, open('APDmaxSignalsNormalized_%i.p'%runNumber,'wb'))

	return

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--RunNumber', type=int, nargs=1, default=5220)
	parser.add_argument('--normalize', action='store_true')
	parser.add_argument('--applyFiducialCut', action='store_true')
	parser.add_argument('--energyThreshold', type=float, default=0)

	args = parser.parse_args()
	runNumber = args.RunNumber[0]

	maxEvents = 100000

	normalize = False
	if args.normalize:
		normalize = True

	applyFiducialCut = False
	if args.applyFiducialCut:
		applyFiducialCut = True

	energyThreshold = args.energyThreshold

	PullData(runNumber,maxEvents,normalize,energyThreshold,applyFiducialCut)

