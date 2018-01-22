import ROOT
import os

ROOT.gSystem.Load('../EXOEnergy/lib/libEXOEnergy.so')

infoRuns = ROOT.EXOSourceRunsPolishedInfo('../EXOEnergy/data/SourceRunsInfo_Phase1_20170411.txt')

infoRuns.CutDoubleComparison('RunNumber',5003,True)
infoRuns.CutDoubleComparison('RunNumber',5020,False)
infoRuns.CutDefaultRuns()

body = """
source /nfs/slac/g/exo_data4/users/maweber/software/Devel/setup.sh;
cd /nfs/slac/g/exo_data4/users/maweber/software/Devel/EXODEEP/;
python PullDataForAPDStudyWithWF.py --RunNumber %s --energyThreshold 1000.0 > %s 2> %s;
"""

allRuns = infoRuns.GetListOf('RunNumber')
runs = set([])
for i in range(allRuns.size()):
	runs.add(allRuns.at(i))

outDir = '/nfs/slac/g/exo_data4/users/maweber/software/Devel/EXODEEP/data/'
for run in sorted(runs):
	filename = '%srun_%s.sh'%(outDir,run)
	f = open(filename,'w')
	f.write(body % (run, filename.replace('.sh','.out'), filename.replace('.sh','.err')))
	f.close()
	cmd = 'chmod 755 %s'%filename
	os.system(cmd)
	cmd = 'bsub -R rhel60 -W 7200 %s'%filename
	print cmd
	os.system(cmd)

