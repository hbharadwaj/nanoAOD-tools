#!/usr/bin/env python                                                                                                                                                                
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.analysis.smp.xs.ZPlusJetsXS_2D import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *                                                                                                   
#from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *                                                                                              
#from PhysicsTools.NanoAODTools.postprocessing.examples.puWeightProducer import *                                                                                                    

if False :
    with open('zjets_files.txt') as f:
        files = f.readlines()
    files = [x.strip() for x in files]

fdir = '/uscms_data/d3/aparker/nanoAod/CMSSW_9_4_1/src/PhysicsTools/NanoAOD/test/'
#'/Users/Om/Desktop/unfolding/nanoAOD/nanoFW/NanoAODTools/python/postprocessing/analysis/smp/xs/nanoTrees/'#
files = [ fdir+'DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8.root']

import random
random.seed(12345)
                                                                                                                                                                      
p1=PostProcessor(".",files,"Jet_pt>170 && ( (nElectron > 1 && HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet140_v) || (nMuon > 1 && HLT_IsoMu22 ))","keep_and_drop.txt",[ZPlusJetsXS_2D()],provenance=True,fwkJobReport=True,histFileName='DY1_M-50_TuneCP5-madMLM-pythia8-80xNanoV0-hists.root', histDirName='zjets'  , postfix='170GevFatJet')

p1.run()
