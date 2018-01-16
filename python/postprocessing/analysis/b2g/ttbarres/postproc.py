#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.analysis.b2g.ttbarres.TTbarResAnaHadronic import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetSmearer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.ak8JetIDProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.ak8SubjetVariableProducer import *
from PhysicsTools.NanoAODTools.postprocessing.examples.puWeightProducer import *


files=[
    "test94X_NANO_14.root",
    ]

import random
random.seed(12345)

#p0=PostProcessor(".",files,'FatJet_pt > 400.',"keep_and_drop.txt",[],outputbranchsel="output_keep_and_drop.txt",histFileName='ttbarreshad_predfile.root', histDirName='ttbarres', postfix='predwrite')

p0=PostProcessor(".",files,'FatJet_pt > 400.',"keep_and_drop.txt",[jetmetUncertaintiesAK4Puppi(), jetmetUncertaintiesAK8Puppi(), ak8JetID(),ak8SubjetVariables(),ttbarreshad_preddistwriter()],outputbranchsel="output_keep_and_drop.txt", histFileName='ttbarreshad_predfile.root', histDirName='ttbarres', postfix='predwrite')

p0.run()
