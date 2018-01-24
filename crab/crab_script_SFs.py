#!/Usr-/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.analysis.jmar.sf.TTbar_SemiLep import *

#fdir = '/uscms_data/d3/aparker/nanoAod/CMSSW_9_4_1/src/PhysicsTools/NanoAOD/test/'
#'/Users/Om/Desktop/unfolding/nanoAOD/nanoFW/NanoAODTools/python/postprocessing/analysis/smp/xs/nanoTrees/'#
#files = [ fdir+'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8.root']

#'Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'
#inputFiles()
p=PostProcessor(".", inputFiles()  ,"nFatJet>0&&FatJet_msoftdrop>30&&FatJet_pt>200&&MET_sumEt>40&& ( (nElectron > 0 && HLT_Ele115_CaloIdVT_GsfTrkIdT) || (nMuon > 0 && HLT_Mu50))" ,modules=[TTbar_SemiLep()],provenance=True,fwkJobReport=True,jsonInput='Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt' ,histFileName= 'TTbar_SemiLep_hists.root', histDirName='ttbar_semilep'  , postfix='_ttbar_semilep-Skim', haddFileName=  'TTbar_SemiLep_hadded.root'  )

p.run()

print "DONE"
os.system("ls -lR")

