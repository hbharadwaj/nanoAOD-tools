
#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

# this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

modulesList = []
from PhysicsTools.NanoAODTools.postprocessing.modules.lfv.MyAnalysisCC import *

#inFiles = []

#with open("testMC.txt") as f:
#    inFiles = [line.rstrip() for line in f]
#modulesList.append( MyAnalysisCC( False, inFiles , [ "output_hists.root",  "mc" , "" , "2017" , "" , 1 , 1 , 1   ] ))


modulesList.append( MyAnalysisCC( True , [ "output_hists.root",  "DoubleEG" , "B" , "2017" , "" , 1 , 1 , 1   ] ))

p = PostProcessor(".",
                  inputFiles(),
                  "Jet_pt>25 &&  Jet_eta < 2.5  && (nMuon + nElectron ) >=3  ",
                  modules=modulesList,
                  provenance=True,
                  fwkJobReport=True,
                  jsonInput=runsAndLumis(),
                  noOut=False)

#listpre = p.getPreselectedEvents()


#modulesList.append( MyAnalysisCC( True, listpre , [ "output_hists.root",  "DoubleMu" , "C" , "2017" , "" , 1 , 1 , 1   ] ))

#p.addModules(modulesList)

p.run()

print("DONE")
