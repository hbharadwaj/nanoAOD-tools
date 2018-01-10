#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.analysis.smp.xs.ZPlusJetsXS_2D import *
p=PostProcessor(".",inputFiles(),"Jet_pt>170",modules=[ZPlusJetsXS_2D()],provenance=True,fwkJobReport=True,jsonInput=runsAndLumis(),histFileName='DY1_M-50_TuneCP5-madMLM-pythia8_XmasNano0.root', histDirName='zjets'  , postfix='nano0')

p.run()

print "DONE"
os.system("ls -lR")

