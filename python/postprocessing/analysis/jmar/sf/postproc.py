#!/usr/bin/env python                                                                                                                                                                
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.analysis.jmar.sf.TTbar_SemiLep import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *                                                                                                   
#from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *                                                                                              
#from PhysicsTools.NanoAODTools.postprocessing.examples.puWeightProducer import *                                                                                                    

if False :
    with open('zjets_files.txt') as f:
        files = f.readlines()
    files = [x.strip() for x in files]

fdir = '/uscms_data/d3/aparker/nanoAod/CMSSW_9_4_1/src/PhysicsTools/NanoAOD/test/'

files = [ fdir+'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8.root']

import random
random.seed(12345)
                                                                                                                                                                      
p1=PostProcessor(".",files,"Jet_pt>200","keep_and_drop.txt",[TTbar_SemiLep()],provenance=True,fwkJobReport=True,histFileName='DY1_M-50_TuneCP5-madMLM-pythia8-80xNanoV0-hists.root', histDirName='ttbar_semilept'  , postfix='200GevFatJet')

p1.run()
