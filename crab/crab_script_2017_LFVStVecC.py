
#!/usr/bin/env python                                                                                                                                                                                              
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

# this takes care of converting the input files from CRAB                                                                                                                                                          
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

modulesList = []
from PhysicsTools.NanoAODTools.postprocessing.modules.lfv.MyAnalysisCC import *


ch = ROOT.TChain("Events")
modulesList.append( MyAnalysisCC( 'False'  , ch , [ "output_hists.root",   'mc' , '' , '2017' , '' , , 0.0512 , 41.53 ] ))


p = PostProcessor(".",
                      inputFiles(),
                      "(nMuon + nElectron) >=3",
                      modules=modulesList,
                      provenance=True,
                      fwkJobReport=True,haddFileName= 'tree_Skim.root',
                      histFileName= 'output_hists.root', histDirName = 'lfv',
                      jsonInput=runsAndLumis())


p.run()

print("DONE")

    