#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

# this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

modulesList = []
from PhysicsTools.NanoAODTools.postprocessing.modules.lfv.MyAnalysisCC import *


from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *


ch = ROOT.TChain("Events")

#jmeCorrections = createJMECorrector(True, "2017", "", "Total", "AK4PFchs")

#modulesList.append( jmeCorrections() )

print "init MyAnalysis class"
modulesList.append( MyAnalysisCC( False , ch ,  [ "output_hists.root",  "mc" , "" , "2017" , "" , 0.0512, 41.53, 500000   ]))

print "run postprocessor init"

p = PostProcessor(".",
                  inputFiles(),
                  "(nMuon + nElectron) >=3",
                  modules=modulesList,
                  provenance=True,
                  fwkJobReport=True,
                  noOut=True,
                  histFileName= 'output_hists.root', histDirName = 'lfv',
                  jsonInput=runsAndLumis())


p.run()


print("DONE")
