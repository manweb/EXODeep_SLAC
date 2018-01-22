
source /nfs/slac/g/exo_data4/users/maweber/software/Devel/setup.sh;
cd /nfs/slac/g/exo_data4/users/maweber/software/Devel/EXODEEP/;
python FlattenData.py --inputFile 'data/WF/EnergyThreshold_800_calib_margin5_v2/APDWFSignalsEnergyThreshold_*.csv' --plotName 'APDWFSpectra_800_calib_margin5_v2_121417.png' --marginFactor 5.0 > /nfs/slac/g/exo_data4/users/maweber/software/Devel/EXODEEP/data/output/FlattenData2.out 2> /nfs/slac/g/exo_data4/users/maweber/software/Devel/EXODEEP/data/output/FlattenData2.err;

