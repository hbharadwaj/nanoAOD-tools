#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis, requestName

from  PhysicsTools.NanoAODTools.postprocessing.analysis.smp.xs.TTbar_SemiLep import *


p=PostProcessor(".",inputFiles(),"Jet_pt>200",modules=[TTbar_SemiLep()],provenance=False,fwkJobReport=False,jsonInput=runsAndLumis(),histFileName= requestName() + '_TTbar_SemiLep_hists.root', histDirName='ttbar_semilep'  , postfix='skimmed-TTbar_SemiLep', haddFileName= requestName() + '_TTbar_SemiLep_hadded.root'  )

p.run()

print "DONE"
os.system("ls -lR")

