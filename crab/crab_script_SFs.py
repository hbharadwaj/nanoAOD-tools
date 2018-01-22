#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.analysis.jmar.sf.TTbar_SemiLep import *

#fdir = '/uscms_data/d3/aparker/nanoAod/CMSSW_9_4_1/src/PhysicsTools/NanoAOD/test/'
#'/Users/Om/Desktop/unfolding/nanoAOD/nanoFW/NanoAODTools/python/postprocessing/analysis/smp/xs/nanoTrees/'#
#files = [ fdir+'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8.root']


#inputFiles()
p=PostProcessor(".", inputFiles() ,"Jet_pt>200 && ( (nElectron > 0 && HLT_Ele115_CaloIdVT_GsfTrkIdT) || (nMuon > 0 && HLT_Mu50))" ,modules=[TTbar_SemiLep()],provenance=True,fwkJobReport=False,jsonInput=runsAndLumis(),histFileName= 'TTbar_SemiLep_hists.root', histDirName='ttbar_semilep'  , postfix='skimmed', haddFileName=  'TTbar_SemiLep_hadded.root'  )

p.run()

print "DONE"
os.system("ls -lR")

