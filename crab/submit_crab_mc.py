import argparse
import subprocess
import sys
import os
import readline
import string
import nano_files_2017
from GFAL_GetROOTfiles import *


# set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--n', dest='DATE')# Name tag for data, I use the day I submitted the CRAB jobs
parser.add_argument('--e', dest='ERA')
parser.add_argument('--d', dest = 'DATASET', default= None) # /DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER  
parser.add_argument('--s', dest = 'SELECTED', default= None) # 
parser.add_argument('--mod', dest = 'MCORDATA', default= None) # /DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER  

ARGS = parser.parse_args()

SAMPLES = {}

SAMPLES.update(nano_files_2017.mc2017_samples)


# /DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER  
# 2017_DYM50'
### This scrip makes all of the files needed to submit the CRAB job:
### The CRAB config - crabConfig.py
### The scriptexe - runPostProcessor.sh
### The crab script (that runs the nanaod-tools postprocessor on the nano ntuples) - runPostProcessor.py
#for key, value in SAMPLES.items():

## set to thi for testing
#'2017_ST_atW'
ARGS.SELECTED = '2017_ST_atW'




# [['/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER','/store/group/phys_top/topNanoAOD/v6-1-1/2017/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2017/200610_154434/0000/'], 'mc','','2017', '','19.47','41.53','11271078']

for key, item in SAMPLES.items() :
#    ARGS.DATASET = samp

    if ARGS.SELECTED != None :
        if key != ARGS.SELECTED :
            continue

    print key 
    print item
    print SAMPLES[key]


    dataset = item[0]

    ARGS.MCORDATA = item[1]


    ARGS.XSEC = item[4]

    ARGS.LUMI = item[5]

    ARGS.NEV = item[6]


    if len(dataset) > 1 :
        ARGS.DATASET = dataset[0]
    else:
        ARGS.DATASET = None    


    #splits = item[0].split('/')
    #print splits
    ## data type e.g. DoubleMuon 

    #id0 = splits[1]


    ## era and lumi section e.g. 2017B 2018B 
    # id2 = splits[2].split('Run')[1].split('-')[0]
    idname = key #id0 +  id2

    ## just letter e.g. B


    print idname



    # make a CRAB config file with template arguments
    CRAB_CFG = '''
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config
config = Configuration()

idname = '{SELECTED}'


config.section_("General")
config.General.requestName = 'NanoLFVtest_%s_%s' % ( '{DATE}', idname )
config.General.transferLogs = True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.outputFiles = [ 'output_hists.root', 'tree_Skim.root' ]
config.JobType.scriptExe = 'crab_script_%s.sh' % (idname )
    # hadd nano will not be needed once nano tools are in cmssw                                                                                                                                                        
config.JobType.inputFiles = ['crab_script_%s.py' % (idname), '../scripts/haddnano.py', "/afs/cern.ch/user/a/asparker/public/LFVTopCode_MyFork/new_mc_nanocmssw_Jan2021/data/CMSSW_10_6_4/src/data/TopLFV/input/RoccoR2017.txt","/afs/cern.ch/user/a/asparker/public/LFVTopCode_MyFork/new_mc_nanocmssw_Jan2021/data/CMSSW_10_6_4/src/data/TopLFV/include/MyAnalysis.h", "/afs/cern.ch/user/a/asparker/public/LFVTopCode_MyFork/new_mc_nanocmssw_Jan2021/data/CMSSW_10_6_4/src/data/TopLFV/lib/main.so", "testMC.txt"  ]

config.JobType.sendPythonFolder = True
config.JobType.allowUndistributedCMSSW = True

config.section_("Data")
config.Data.inputDataset = '{DATASET}'




config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

config.Data.outLFNDirBase = '/store/user/%s/NanoPosttest_%s_%s' % ( 'asparker', '{DATE}' ,idname )
config.Data.publication = False
config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"

    '''

    # open crabConfig.py, substitute into CRAB_CFG the arguments from ARGS, write it, run it, and remove it

    open('crabConfig%s.py'% (idname ) , 'w').write(CRAB_CFG.format(**ARGS.__dict__))

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
modulesList.append( MyAnalysisCC( False , ch , [ "output_hists.root",   '{MCORDATA}' , '' , '{ERA}' , '' ,float( {XSEC}) ,float( {LUMI}) , float({NEV}) ] ))


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

    open('crab_script_%s.py' % (idname), 'w').write(CRAB_SCRIPT.format(**ARGS.__dict__))


    BASH_SCRIPT = '''
#this is not mean to be run locally                                                                                                                          echo Check if TTY
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
python 'crab_script_%s.py' % ('{SELECTED}') $1
fi



    '''
    open('crab_script_%s.sh' % (idname), 'w').write(BASH_SCRIPT.format(**ARGS.__dict__))

    #use crabConfig.py- run it, and remove it

    subprocess.call('crab submit -c crabConfig%s.py' % (idname), shell=True)
    subprocess.call('echo "crab submit -c crabConfig%s.py" ' % (idname), shell=True)
    #subprocess.call('rm crabConfig.py', shell=True)

