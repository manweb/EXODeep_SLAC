
source /nfs/slac/g/exo_data4/users/maweber/software/Devel/setup.sh;
cd /nfs/slac/g/exo_data4/users/maweber/software/Devel/EXODEEP/;
python FlattenData.py --inputFile 'data/WF/EnergyThreshold_700_posX_posY_calib_new/APDWFSignalsEnergyThresholdCut_*.csv' --plotName 'APDWFSpectra_posX_posY_calib_new_101717.png' --marginFactor 1.2 > /nfs/slac/g/exo_data4/users/maweber/software/Devel/EXODEEP/data/output/FlattenData_calib.out 2> /nfs/slac/g/exo_data4/users/maweber/software/Devel/EXODEEP/data/output/FlattenData_calib.err;

