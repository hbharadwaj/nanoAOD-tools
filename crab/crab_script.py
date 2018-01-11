#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.analysis.smp.xs.ZPlusJetsXS_2D import *

#fileis = 'file:/uscms_data/d3/aparker/nanoAod/CMSSW_9_4_1/src/PhysicsTools/NanoAOD/test/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8.root'
#inputFiles()
p=PostProcessor(".",inputFiles(),"Jet_pt>170",modules=[ZPlusJetsXS_2D()],provenance=False,fwkJobReport=False,jsonInput=runsAndLumis(),histFileName='DY1_M-50_TuneCP5-madMLM-pythia8_XmasNano_hists.root', histDirName='zjets'  , postfix='nanoPost2DSel', haddFileName='DY1_M-50_TuneCP5-madMLM-pythia8_XmasNano_hadded.root'  )

p.run()

print "DONE"
os.system("ls -lR")

