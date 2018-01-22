import ROOT
import os

ROOT.gSystem.Load('../EXOEnergy/lib/libEXOEnergy.so')

infoRuns = ROOT.EXOSourceRunsPolishedInfo('../EXOEnergy/data/SourceRunsInfo_Phase1_20170411.txt')

runNumbers = []
#runNumbers.append(4770)
#runNumbers.append(4772)
#runNumbers.append(4773)
#runNumbers.append(4997)
runNumbers.append(5003)
runNumbers.append(5008)
runNumbers.append(5020)
runNumbers.append(5021)
runNumbers.append(5027)
runNumbers.append(5030)
runNumbers.append(5033)
runNumbers.append(5036)
runNumbers.append(5042)
runNumbers.append(5051)
runNumbers.append(5052)
runNumbers.append(5053)
runNumbers.append(5056)
runNumbers.append(5057)
runNumbers.append(5064)
runNumbers.append(5067)
runNumbers.append(5069)
runNumbers.append(5118)
runNumbers.append(5322)
runNumbers.append(5323)
runNumbers.append(5325)
runNumbers.append(5326)
runNumbers.append(5396)
runNumbers.append(5794)
runNumbers.append(5795)
runNumbers.append(5818)
runNumbers.append(5851)
runNumbers.append(5852)
runNumbers.append(5853)
runNumbers.append(5854)
runNumbers.append(5855)
runNumbers.append(5856)
runNumbers.append(5857)
runNumbers.append(5859)
runNumbers.append(5860)
runNumbers.append(5861)
#runNumbers.append(5862)
#runNumbers.append(5872)
#runNumbers.append(6045)
runNumbers.append(5066)
runNumbers.append(5806)
runNumbers.append(5807)
runNumbers.append(5809)
runNumbers.append(5827)
runNumbers.append(5828)
runNumbers.append(5829)
runNumbers.append(5830)

# Only Th-228
"""runNumbers.append(5003)
runNumbers.append(5008)
runNumbers.append(5020)
runNumbers.append(5021)
runNumbers.append(5027)
runNumbers.append(5030)
runNumbers.append(5033)
runNumbers.append(5036)
runNumbers.append(5042)
runNumbers.append(5051)
runNumbers.append(5052)
runNumbers.append(5053)
runNumbers.append(5056)
runNumbers.append(5057)
runNumbers.append(5118)
runNumbers.append(5827)
runNumbers.append(5828)
runNumbers.append(5829)
runNumbers.append(5830)
runNumbers.append(5851)
runNumbers.append(5852)
runNumbers.append(5853)
runNumbers.append(5854)
runNumbers.append(5855)
runNumbers.append(5856)
runNumbers.append(5857)
runNumbers.append(5859)
runNumbers.append(5860)
runNumbers.append(5861)
"""
#infoRuns.CutDoubleComparison('RunNumber',5003,True)
#infoRuns.CutDoubleComparison('RunNumber',5020,False)
#infoRuns.CutDefaultRuns()

body = """
source /nfs/slac/g/exo_data4/users/maweber/software/Devel/setup.sh;
cd /nfs/slac/g/exo_data4/users/maweber/software/Devel/EXODEEP/;
python PullDataForAPDStudyWithWF.py --RunNumber %s --energyThreshold 800.0 --outDir data/WF/EnergyThreshold_800_calib_margin2_v2/ --calib0 %f --calib1 %f --rotationAngle 0.5312 --subtractBaseline > %s 2> %s;
"""

allRuns = infoRuns.GetListOf('RunNumber')
runs = set([])
for i in range(allRuns.size()):
	runs.add(allRuns.at(i))

calib = ROOT.TTree()
calib.ReadFile('phase1_calibPars_ionization.txt')

applyCalibration = True

outDir = '/nfs/slac/g/exo_data4/users/maweber/software/Devel/EXODEEP/data/output/WF/EnergyThreshold_800_calib_margin2_v2/'
for run in sorted(runNumbers):
	info = infoRuns.Clone()
	info.CutExact('RunNumber','%s'%run)
	week = info.GetListOf('WeekIndex')[0]
	calib.Draw('p0:p1','week == %s && multiplicity == 1'%week,'goff')
	calibP0 = 0.0
	calibP1 = 1.0
	if applyCalibration:
		calibP0 = calib.GetV1()[0]
		calibP1 = calib.GetV2()[0]
	filename = '%srun_%s.sh'%(outDir,run)
	f = open(filename,'w')
	f.write(body % (run, calibP0, calibP1, filename.replace('.sh','.out'), filename.replace('.sh','.err')))
	f.close()
	cmd = 'chmod 755 %s'%filename
	os.system(cmd)
	cmd = 'bsub -R rhel60 -W 7200 %s'%filename
	print cmd
	os.system(cmd)

