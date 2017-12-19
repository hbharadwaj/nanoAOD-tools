#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.analysis.smp.xs.ZPlusJetsXS import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
#from PhysicsTools.NanoAODTools.postprocessing.examples.puWeightProducer import *

files=["~/cernbox/NANO/zjets_test.root"]

import random
random.seed(12345)
p1=PostProcessor(".",files,'nFatJet + nGenJetAK8 >= 1 && GenJetAK8_pt > 110',"keep_and_drop.txt",[ZPlusJetsXS()],provenance=False, histFileName='zplusjetsxs_hists.root', histDirName='zjets', postfix='zjets')
p1.run()
