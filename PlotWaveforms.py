import ROOT

waveformFiles = '/nfs/slac/g/exo_data3/exo_data/data/WIPP/root/[runNumber]/'

ROOT.gSystem.Load('../EXOEnergy/lib/libEXOEnergy.so')

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

runNumber = 5220

tWF = ROOT.TChain('tree','tree')
tWF.Add(waveformFiles.replace('[runNumber]','%i'%runNumber)+'*.root')

ed = ROOT.EXOEventData()
tWF.SetBranchAddress('EventBranch',ed)

tWF.GetEntry(0)

nsamples = ed.GetWaveformData().fNumSamples
nBL = nsamples/3
nWF = ed.GetWaveformData().GetNumWaveforms()

histos = []
histosOffset = []
channels = []
sumHisto = ROOT.TH1F("h_sum","h_sum",nsamples,0,nsamples)
peakHisto = ROOT.TH1F("h_peak","h_peak",74,0,74)

sumHisto.SetLineColor(1)
peakHisto.SetLineColor(1)

sumHisto.GetXaxis().SetTitle("sample")
sumHisto.GetYaxis().SetTitle("sum amplitude")
sumHisto.GetXaxis().CenterTitle()
sumHisto.GetYaxis().CenterTitle()

peakHisto.GetXaxis().SetTitle("channel")
peakHisto.GetYaxis().SetTitle("amplitude")
peakHisto.GetXaxis().CenterTitle()
peakHisto.GetYaxis().CenterTitle()

offset = 50

c1 = ROOT.TCanvas()

h_empty = ROOT.TH2F("h_empyt","h_empty",100,0,nsamples,100,-200,74*offset+200)

h_empty.GetXaxis().SetTitle("sample")
h_empty.GetYaxis().SetTitle("amplitude + offset")
h_empty.GetXaxis().CenterTitle()
h_empty.GetYaxis().CenterTitle()
h_empty.GetYaxis().SetTitleOffset(1.2)

h_empty.Draw()

for i in range(nWF):
	histo = ROOT.TH1F("h_%i"%i,"h_%i"%i,nsamples,0,nsamples)
	histoNoOffset = ROOT.TH1F("hNoOffset_%i"%i,"hNoOffset_%i"%i,nsamples,0,nsamples)

	histo.SetLineColor(1)

	wf = ed.GetWaveformData().GetWaveform(i)
	ch = wf.fChannel

	if ch < 152:
		continue

	wf.Decompress()

	BL = 0.0
	for k in range(nBL):
		BL += wf.At(k)
	BL /= (nBL)

	for k in range(nsamples):
		histo.SetBinContent(k, wf.At(k)-BL+(ch-152)*offset)
		histoNoOffset.SetBinContent(k, wf.At(k)-BL)
		sumHisto.SetBinContent(k, sumHisto.GetBinContent(k)+wf.At(k)-BL)

	histos.append(histoNoOffset)
	histosOffset.append(histo)
	channels.append(ch-152)

	histo.Draw("same")

maxBin = sumHisto.GetMaximumBin()
rms = 0
for k in range(nsamples):
	rms += sumHisto.GetBinContent(k)*sumHisto.GetBinContent(k)
rms /= nsamples
rms = ROOT.TMath.Sqrt(rms)

print("maximum at %i, max = %f, rms = %f"%(maxBin,sumHisto.GetMaximum(),rms))

for k in range(len(channels)):
	peakHisto.SetBinContent(channels[k],histos[k].GetBinContent(maxBin)/sumHisto.GetMaximum())
	print histos[k].GetBinContent(maxBin)/sumHisto.GetMaximum()

c2 = ROOT.TCanvas()

sumHisto.Draw()

c3 = ROOT.TCanvas()

peakHisto.Draw()

c1.SaveAs("plots/WFs_5220_0.pdf")
c2.SaveAs("plots/sumWF_5220_0.pdf")
c3.SaveAs("plots/peakChannel_5220_0.pdf")

raw_input("Enter...")
