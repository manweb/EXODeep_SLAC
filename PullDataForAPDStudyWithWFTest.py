import numpy as np
import math
#import h5py
import cPickle as pickle
import ROOT
import os, fnmatch
import argparse
import matplotlib.pyplot as plt

def GetAPDSignals(waveformData, runNumber, eventNumber, e_scint, subtractBaseline):
	numAPD = 74
	minChannel = 152
	minSample = 750
	numSamples = 350
	maxSample = minSample+numSamples
	nsamples = waveformData.fNumSamples
	nWF = waveformData.GetNumWaveforms()

	channelData = np.zeros((numAPD,numSamples))
	channels = np.zeros(numAPD)
	sumData = np.zeros(numSamples)

	apdSignals = np.zeros(numAPD*numSamples)

	if not nsamples == 2048:
		return apdSignals

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

		for k in range(0,numSamples):
			if subtractBaseline:
				np.put(apdSignals, (ch-minChannel)*numSamples+k, wf.At(k+minSample)-BL)
			else:
				np.put(apdSignals, (ch-minChannel)*numSamples+k, wf.At(k+minSample))
			np.put(sumData, k, sumData[k]+wf.At(k+minSample)-BL)

		n += 1

	img = np.reshape(apdSignals, (74,350))
	img_sum = np.sum(img, axis=0)
	img_std = np.std(img_sum[0:100])
	img_max = np.max(img_sum)

	maxBin = np.argmax(sumData)
	apdMax = np.max(sumData)
	rms = 0
	for k in range(numSamples/3):
		rms += sumData[k]*sumData[k]
	rms /= numSamples/3
	rms = math.sqrt(rms)
	
	#print('std: %.2f, max: %.2f, rms: %.2f'%(img_std, img_max, rms))

	if e_scint > 1500.0 and img_max < 4*img_std:
		fullWF = np.zeros(numAPD*nsamples)

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

                	for k in range(0,nsamples):
                	        if subtractBaseline:
                	                np.put(fullWF, (ch-minChannel)*nsamples+k, wf.At(k)-BL)
                	        else:
                	                np.put(fullWF, (ch-minChannel)*nsamples+k, wf.At(k))

		print('Event: %i -> found bad event'%eventNumber)

		imgFull = np.reshape(fullWF, (74,nsamples))

		#fig, axarr = plt.subplots(2,1,figsize=(5,8))

		#ax[0].imshow(img, interpolation='nearest', cmap='summer')
		#ax[1].imshow(imgFull, interpolation='nearest', cmap='summer')

		#plt.savefig('bad_events/bad_event_%i_%i.png'%(runNumber,eventNumber))

		#plt.close()

		img.dump('bad_events/bad_event_%i_%i.pickle'%(runNumber,eventNumber))
		imgFull.dump('bad_events/bad_event_%i_%i_full.pickle'%(runNumber,eventNumber))
	else:
		print('Event: %i'%eventNumber)

	#if apdMax < 5*rms:
	#	return np.zeros(numAPD*numSamples)

	return apdSignals

def PullData(runNumber,maxEvents,energyThreshold,applyFiducialCut,outDir,calibP0,calibP1,rotationAngle,subtractBaseline):
	print("*************************************************************")
	print("RunNumber:		%i"%runNumber)
	print("maxEvents:		%i"%maxEvents)
	print("energyThreshold:	%f"%energyThreshold)
	if applyFiducialCut:
		print("applyFiducialCut:	True")
	else:
		print("applyFiducialCut:	False")
	print("outDir:			%s"%outDir)
	print("calibP0:		%f"%calibP0)
	print("calibP1:		%f"%calibP1)
	print("rotationAngle:		%f"%rotationAngle)
	if subtractBaseline:
		print("subtractBaseline:	True")
	else:
		print("subtractBaseline:	False")
	print("*************************************************************")

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

	cut = "nsc == 1 && multiplicity == 1 && isSolicitedTrigger == 0 && t_scint > -250 && t_scint < 100"

	if applyFiducialCut:
		#cut += " && TMath::Abs(cluster_z) > 10.0 && TMath::Abs(cluster_z) < 182.0 && TMath::Sqrt(cluster_x*cluster_x+cluster_y*cluster_y) < 162.0"
		cut += " && (cluster_x > 0 || (cluster_x < 0 && TMath::Abs(cluster_y) > TMath::Abs(cluster_x))) && TMath::Abs(cluster_z) > 10.0"

	if energyThreshold > 0.0:
		cut += " && (e_charge*TMath::Cos(%f)+e_scint*TMath::Sin(%f))*0.734 + 11.8 > %f"%(rotationAngle,rotationAngle,energyThreshold)

	# Diagonal cut
	cut += " && e_scint < e_charge*1.1 + 617.4"

	n = tProcessed.Draw("eventNum:e_scint",cut,"goff")
	eventNumbers = np.copy(np.frombuffer(tProcessed.GetV1(), count=n))
	e_scint = np.copy(np.frombuffer(tProcessed.GetV2(), count=n))

	n = tProcessed.Draw("cluster_x:cluster_y:cluster_z:(%f*e_charge+%f)"%(calibP1,calibP0),cut,"goff")
	cluster_x = np.copy(np.frombuffer(tProcessed.GetV1(), count=n))
	cluster_y = np.copy(np.frombuffer(tProcessed.GetV2(), count=n))
	cluster_z = np.copy(np.frombuffer(tProcessed.GetV3(), count=n))
	e_charge = np.copy(np.frombuffer(tProcessed.GetV4(), count=n))
	#e_charge = np.ones(cluster_x.shape[0])*2615.0

	data = np.zeros(78)

	nEvents = 0
	nEventsDropped = 0
	for i in range(n):
		if (tWF.GetEntryWithIndex(runNumber,int(eventNumbers[i])) < 0):
			print("Waveform for event %i in run %i not found"%(eventNumbers[i],runNumber))
			continue

		print('Trigger source: %i'%ed.fEventHeader.fTriggerSource)
	
		apdSignals = GetAPDSignals(ed.GetWaveformData(), runNumber, eventNumbers[i], e_scint[i], subtractBaseline)

		continue

		if not apdSignals.any() or cluster_x[i] == -999 or cluster_y[i] == -999 or cluster_z[i] == -999 or e_charge[i] == -999:
			#print("APD signal for event %i in run %i is below threshold"%(tProcessed.GetV1()[i],runNumber))
			nEventsDropped += 1
			continue
	
		apdSignals = np.append(apdSignals,np.array([cluster_x[i], cluster_y[i], cluster_z[i], e_charge[i], e_scint[i]]))
	
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

		fname = outDir+'/APDWFSignalsEnergyThreshold'
		if applyFiducialCut:
			fname = outDir+'APDWFSignalsEnergyThresholdCut'

		f = open('%s_%i.csv'%(fname,runNumber),option)
		f.write(row)
		f.close()

		if nEvents%1000==0:
			print("%i events processed, %i events dropped"%(nEvents,nEventsDropped))

		if nEvents > maxEvents:
			break

	#print("Writing data. Total events: %i, Events dropped: %i"%(nEvents,nEventsDropped))
	#pickle.dump(data, open('APDmaxSignalsNormalized_%i.p'%runNumber,'wb'))

	return

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--RunNumber', type=int, nargs=1, default=5220)
	parser.add_argument('--applyFiducialCut', action='store_true')
	parser.add_argument('--energyThreshold', type=float, default=0)
	parser.add_argument('--outDir', type=str, default='data/')
	parser.add_argument('--calib0', type=float, default=0)
	parser.add_argument('--calib1', type=float, default=1)
	parser.add_argument('--rotationAngle', type=float, default=0)
	parser.add_argument('--subtractBaseline', action='store_true')

	args = parser.parse_args()
	runNumber = args.RunNumber[0]

	maxEvents = 50000

	applyFiducialCut = False
	if args.applyFiducialCut:
		applyFiducialCut = True

	energyThreshold = args.energyThreshold

	subtractBaseline = False
	if args.subtractBaseline:
		subtractBaseline = True

	PullData(runNumber,maxEvents,energyThreshold,applyFiducialCut,args.outDir,args.calib0,args.calib1,args.rotationAngle,subtractBaseline)

