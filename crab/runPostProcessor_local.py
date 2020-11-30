

#!/Usr-/bin/env python                                                                                                                                                                                                                                     
import os,sys
#import ROOT
from importlib import import_module

### Import the nanoAODtools
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
#from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.pdfWeightProducer import * 

#this takes care of converting the input files from CRAB                                                                                                                                                                                                                                                                     
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

### this is the selection module to pick LFV events                                                                                                                                 
from PhysicsTools.NanoAODTools.postprocessing.modules.lfv.MyAnalysisCC import *                                                                                                      
#from MyAnalysisCC import *
print "from PhysicsTools.NanoAODTools.postprocessing.modules.lfv.MyAnalysisCC import *"

era =  '2017'
preselection = ''
modulesToRun = []

fileIn = ['root://cms-xrd-global.cern.ch//store/user/piedavid/topNanoAOD/v6-1-1/2017/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/TopNanoAODv6-1-1_2017/200615_072720/0000/tree_26.root']
#['root://cms-xrd-global.cern.ch//store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleEG/TopNanoAODv6-1-1_2017/200615_080330/0000/tree_51.root'  ]


#if '17MC' in era :
    #modulesToRun.append( pdfWeightProducer() ) 
    #modulesToRun.append( jetmetUncertainties2017AK8PFPuppiAll() )
    #modulesToRun.append( puAutoWeight() )
if '16MC' in era :                                                                                                                          
    modulesToRun.append( pdfWeightProducer() )                                                                                              
    modulesToRun.append( jetmetUncertainties2016AK8PFPuppiAll() )                                                                           
    modulesToRun.append( puWeight() )  

if '17' in era :
    preselection = "(Jet_pt>30 && abs(Jet_eta)<2.5  )&& (     (Electron_pt > 30. && nElectron >= 1  && abs(Electron_eta) < 2.5   )    ||   (Muon_pt > 30 && nMuon >= 1  &&  abs(Muon_eta) < 2.5  ) )"
if '16' in era : 
    preselection = ""
isdata = True
loopInfo = [ "2017_B_DoubleEG_0_0.root", "data" , "DoubleEG" , "2017" , "B" , 1 , 1 , 1   ] 

print "myanalysis =  MyAnalysisCpp(  isdata, fileIn , loopInfo    )"
myanalysis =  MyAnalysisCC(  isdata, fileIn , loopInfo    )
modulesToRun.append( myanalysis )



print "era"
print era
print "preselection"
print preselection

nameis = '2017_B_DoubleEG_0_0' #'LPV_SkimTOPnanoAOD'                                                                                                                                                                                                                                 


                                                                
p1=PostProcessor(".", fileIn  , preselection, "keep_and_drop.txt", modulesToRun, provenance=True,fwkJobReport=True,histFileName= nameis +'-histos.root', histDirName='lfv', haddFileName =  nameis +'.root',jsonInput=runsAndLumis() )

#if '16MC' in era :
#    print "ERROR not running: Not yet set up to process 2016 data or MC, fix preselection triggers for this!"
#else :
p1.run()

print "DONE"
#os.system("ls -lR")

#/afs/cern.ch/user/a/asparker/public/LFVTopCode_MyFork/nanoAODtools_crab_mc_cmssw/CMSSW_10_6_2/src/
