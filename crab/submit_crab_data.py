import argparse
import subprocess

# set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--e', dest='ERA')
parser.add_argument('--d', dest = 'DATASET') # /DoubleMuon/piedavid-Run2017C-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER
ARGS = parser.parse_args()

### This scrip makes all of the files needed to submit the CRAB job:
### The CRAB config - crabConfig.py
### The scriptexe - runPostProcessor.sh
### The crab script (that runs the nanaod-tools postprocessor on the nano ntuples) - runPostProcessor.py



# make a CRAB config file with template arguments
CRAB_CFG = '''

from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config

config = Configuration()



splits = '{DATASET}'.split('/')
idname = splits[1]
id2 = splits[2].split('Run')[1].split('-')[0]
idname += id2

print idname


config.section_("General")
config.General.requestName = 'NanoLFVtest_Jan28_%s' % ( idname )
config.General.transferLogs = True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.outputFiles = [ 'output_hists.root', 'tree_Skim.root' ]
config.JobType.scriptExe = 'crab_script_dm2.sh'
# hadd nano will not be needed once nano tools are in cmssw                                                                                                                                                        
config.JobType.inputFiles = ['crab_script_dm2.py', '../scripts/haddnano.py', "/afs/cern.ch/user/a/asparker/public/LFVTopCode_MyFork/new_mc_nanocmssw_Jan2021/data/CMSSW_10_6_4/src/data/TopLFV/input/RoccoR2017.txt","/afs/cern.ch/user/a/asparker/public/LFVTopCode_MyFork/new_mc_nanocmssw_Jan2021/data/CMSSW_10_6_4/src/data/TopLFV/include/MyAnalysis.h", "/afs/cern.ch/user/a/asparker/public/LFVTopCode_MyFork/new_mc_nanocmssw_Jan2021/data/CMSSW_10_6_4/src/data/TopLFV/lib/main.so", "testMC.txt"  ]

config.JobType.sendPythonFolder = True
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
config.Data.inputDataset = '{DATASET}'




config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

config.Data.outLFNDirBase = '/store/user/%s/NanoPosttest_Jan28_%s' % ( 'asparker', idname )
config.Data.publication = False
config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"

'''

# open crabConfig.py, substitute into CRAB_CFG the arguments from ARGS, write it, run it, and remove it

open('crabConfig.py' , 'w').write(CRAB_CFG.format(**ARGS.__dict__))

#open('crab_cfg_%s.py' % (idname), 'w').write(CRAB_CFG.format(**ARGS.__dict__))



### make the runPostProcessor.py script

CRAB_SCRIPT = '''
#!/usr/bin/env python                                                                                                                                                                                              
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

# this takes care of converting the input files from CRAB                                                                                                                                                          
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

modulesList = []
from PhysicsTools.NanoAODTools.postprocessing.modules.lfv.MyAnalysisCC import *

ch = ROOT.TChain("Events")
# fix this "DoubleMu" should be not hardcoded
modulesList.append( MyAnalysisCC( False , ch , [ "output_hists.root",   "data" , "DoubleMu" , '{ERA}' , idname.split('{ERA}') , 1,1,1  ] ))

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

'''

open('crab_script_dm2.py', 'w').write(CRAB_SCRIPT.format(**ARGS.__dict__))


BASH_SCRIPT = '''
#this is not mean to be run locally                                                                                                                                                                                
#                                                                                                                                                                                                                  
echo Check if TTY
if [ "`tty`" != "not a tty" ]; then
  echo "YOU SHOULD NOT RUN THIS IN INTERACTIVE, IT DELETES YOUR LOCAL FILES"
else
echo "%%%%%%%%%%%%%%%%%  Running my nano CRAB  %%%%%%%%%%%%%%%%%%%%%%%%% "
echo "ENV..................................."
env
echo "VOMS"
voms-proxy-info -all
echo "CMSSW BASE, python path, pwd"
echo $CMSSW_BASE
echo $PYTHON_PATH
echo $PWD
rm -rf $CMSSW_BASE/lib/
rm -rf $CMSSW_BASE/src/
rm -rf $CMSSW_BASE/module/
rm -rf $CMSSW_BASE/python/
mv lib $CMSSW_BASE/lib
mv src $CMSSW_BASE/src
mv module $CMSSW_BASE/module
mv python $CMSSW_BASE/python

echo Found Proxy in: $X509_USER_PROXY
python crab_script_dm2.py $1
fi



'''
open('crab_script_dm2.sh', 'w').write(BASH_SCRIPT.format(**ARGS.__dict__))

#use crabConfig.py- run it, and remove it

subprocess.call('crab submit -c crabConfig.py', shell=True)
subprocess.call('echo "crab submit -c crabConfig.py"', shell=True)
#subprocess.call('rm crabConfig.py', shell=True)

