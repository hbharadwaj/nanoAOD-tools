#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.analysis.smp.xs.ZPlusJetsXS_2D import *

#fdir = '/uscms_data/d3/aparker/nanoAod/CMSSW_9_4_1/src/PhysicsTools/NanoAOD/test/'

#files = [ fdir+'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8.root']

#inputFiles()

from  PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule import *
p=PostProcessor(".",inputFiles(),"Jet_pt>200",modules=[exampleModule()],provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())
p.run()

print "DONE"
os.system("ls -lR")

#p=PostProcessor(".", files ,"Jet_pt>170",modules=[ZPlusJetsXS_2D()],provenance=False,fwkJobReport=False,jsonInput=runsAndLumis(),histFileName= requestName() + '_ZPlusJetsXS_2D_hists.root', histDirName='zjets'  , postfix='skimmed-ZPlusJetsXS_2D', haddFileName= requestName() + '_ZPlusJetsXS_2D_hadded.root'  )

#p.run()

#print "DONE"
#os.system("ls -lR")

