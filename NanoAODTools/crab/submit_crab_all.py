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
### above is only option you need to set, 
### it will run everything 

### unless you set the option below
### ARGS.SELECTED to a name from the keys of the
### nano_files_2017.py dictionary e.g.  '2017_LFVStVecC' #'2017_ST_atW'
### Then it will run only this dataset
parser.add_argument('--s', dest = 'SELECTED', default= None) 



### Do NOT set below options, they will be set for you for each dataset
parser.add_argument('--e', dest='ERA', default= None)
parser.add_argument('--d', dest = 'DATASET', default= None) 
parser.add_argument('--mod', dest = 'MCORDATA', default= None) 
parser.add_argument('--isd', dest = 'ISDATA', default= None) 
parser.add_argument('--dt', dest = 'DATATYPE', default= None) 
parser.add_argument('--l', dest = 'LETTER', default= None) 
parser.add_argument('--id', dest='ID', default= None)

ARGS = parser.parse_args()

SAMPLES = {}

SAMPLES.update(nano_files_2017.mc2017_samples)
#SAMPLES.update(nano_files_2017.data2017_samples)


# /DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER  
# 2017_DYM50'
### This scrip makes all of the files needed to submit the CRAB job:
### The CRAB config - crabConfig.py
### The scriptexe - runPostProcessor.sh
### The crab script (that runs the nanaod-tools postprocessor on the nano ntuples) - runPostProcessor.py
#for key, value in SAMPLES.items():

## set to thi for testing
#'2017_ST_atW'
#ARGS.SELECTED = None #'2017_TTZToLLNuNu' #TTZToQQ'  #'2017_TTWJetsToLNu'  #'2017_DYM10to50'  #'2017_C_DoubleMu'   #'2017_LFVStVecU' #'2017_ST_atW'
#data2017_samples['2017_F_DoubleMu'] = [['/DoubleMuon/piedavid-Run2017F-31Mar2018-v1_TopNanoAODv6-1-1_2017-9721c24ccc7f925c513e24ff74941177/USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleMuon/TopNanoAODv6-1-1_2017/200615_080726/0000/'], 'data','DoubleMu','2017', 'F','1','1','1']


dirname = 'CRABtasks' ## If we want to change this then we should make it an ARG so we can edit name is script below
os.system('mkdir '+ dirname )
print "make CRABtasks directory to store CRAB submit scripts"
published = True

SUBMIT_SCRIPT = '''                                                                                                                                       
#!/usr/bin/env python                                                                                                                                        

import os, subprocess                                                                                                                                                  
print "Now submitting your CRAB jobs to find the LFV Top selected events from our TOP nanoAOD samples"

'''


# below is stricture of input data for reference:

# [['/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER','/store/group/phys_top/topNanoAOD/v6-1-1/2017/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2017/200610_154434/0000/'], 'mc','','2017', '','19.47','41.53','11271078']

#mc2017_samples['2017_DYM10to50'] = [['/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/piedavid-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8USER','/store/user/piedavid/topNanoAOD/v6-1-1/2017/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv6-1-1_2017/200613_065556/0000/','/store/#u#\
#ser/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201104_172003/0000/'], 'mc','','2017', '','18610','41.53','39521230'] ## '78,994#\
#,955' ## <-  is event number from miniaod, we must be missing an extension                                                                                    


## list of keys we ran over to use for the CRAB submit script
ids = []

for key, item in SAMPLES.items() :
#    ARGS.DATASET = samp

    #if ARGS.SELECTED != None :
    #    if key != ARGS.SELECTED :
    #        continue
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ new MC or data sample $$$$$$$$$$$$$$$$$$$$$$$$$"  
    print key 
    print item
    print SAMPLES[key]


    dataset = item[0]

    ARGS.MCORDATA = item[1]

    if ARGS.MCORDATA == 'data':
       ARGS.ISDATA = True
    elif ARGS.MCORDATA == 'mc':
       ARGS.ISDATA = False



    ARGS.DATATYPE = item[2] # e.g. 'DoubleMu'


    ARGS.ERA = item[3]

    ARGS.LETTER = item[4] # data section e.g.  B   

    ARGS.XSEC = item[5]

    ARGS.LUMI = item[6]

    ARGS.NEV = item[7]

    splits = dataset[0].split('/')[-1]
    if len(dataset) > 1 :
        # if there is more than 1 file location or dataset in the let then look thorugh them all
        # if the first one ends in USER then it is a dataset name
        
        print splits
        if 'USER' in splits:
            ARGS.DATASET = [dataset[0]]
            published = True
            print "Dataset name was given so CRAB submission will use this to submit"
        elif '0000' in splits:
            ARGS.DATASET = [dataset[0]]
            published = False
            print "Dataset location was given so CRAB submission will use files in that location to submit"            
 
        print "WARNING: If any dataset has more than 1 input dataset or file location this script is only submitting the first, fix this soon..."
        if ( len(dataset) > 2  ):
            if 'USER' in splits:
               
                ARGS.DATASET = [ dataset[1]  , dataset[2]  ]
                published = False
                if '2017_TTZToQQ' in key :
                    ARGS.DATASET = [ dataset[1]  , dataset[2] , dataset[3]  ]
                ### if there is more than 1 dataset, eg. if there are extensions to the MC, 
                ### then usually, 1st in list is the dataset name
                ### 2nd entry is basically a duplicate, it is the file location of that same datset
                ### 3rd entry is the location of the extension files, usually asparker cms eos space bc we created those ourselves so they are unpublished
        if ( published == False and len(dataset) == 2   ):
           
            ARGS.DATASET = [ dataset[0]  , dataset[1]  ]

            





    elif  len(dataset)  == 1 :
        ARGS.DATASET =  [dataset[0]] 
        #if '0000' in splits: 
        published = False

    elif len(dataset)  < 1 :    
        print "ERROR: No dataset name or file location given!!! "
    print "dataset or location :"
    print ARGS.DATASET

    #splits = item[0].split('/')
    #print splits
    ## data type e.g. DoubleMuon 

    #id0 = splits[1]


    ## era and lumi section e.g. 2017B 2018B 
    # id2 = splits[2].split('Run')[1].split('-')[0]
    idname = key #id0 +  id2
    ARGS.SELECTED = idname
    ## just letter e.g. B


    print idname



    # make a CRAB config file with template arguments
    CRAB_CFG = '''
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config
config = Configuration()

idname = '{SELECTED}'
dirname = 'CRABtasks'

config.section_("General")
config.General.requestName = 'NanoLFVtest_%s_%s' % ( '{DATE}', idname )
config.General.transferLogs = True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.outputFiles = [ 'output_hists.root' ]
config.JobType.scriptExe = 'crab_script_%s.sh' % ( idname )
    # hadd nano will not be needed once nano tools are in cmssw                                                                                                                                                        
config.JobType.inputFiles = ['crab_script_%s.py' % ( idname), "/afs/cern.ch/user/b/bharikri/private/TopLFV/CMSSW_10_6_4/src/data/TopLFV/input/RoccoR2017.txt","/afs/cern.ch/user/b/bharikri/private/TopLFV/CMSSW_10_6_4/src/data/TopLFV/include/MyAnalysis.h", "/afs/cern.ch/user/b/bharikri/private/TopLFV/CMSSW_10_6_4/src/data/TopLFV/lib/main.so", 'haddnano.py' ]

config.JobType.sendPythonFolder = True
config.JobType.allowUndistributedCMSSW = True
'''

    if not published :
        if len(ARGS.DATASET) == 1 :
            print dataset
            print "getting files for unpublished submission : "
            ARGS.DATASET = GFAL_GetROOTfiles( dataset[0] )
        else :
           df = [] #None
           print ARGS.DATASET
           print len(ARGS.DATASET)

           for d in ARGS.DATASET:
               print d 
               tdf = GFAL_GetROOTfiles( d )
               df += tdf
           ARGS.DATASET = df
           print ARGS.DATASET
        ## Now that we have the input files, we can make the file input part of the CRAB cfg file         
        CRAB_CFG_UNPUB= '''
config.section_("Data")                                                                                                                             

filelist = {DATASET}
#for l in jobsLines:
#    filelist.append(str(l[:-1]))
#print filelist 
config.Data.userInputFiles = filelist
  
'''

    if published:
        ARGS.DATASET = dataset[0]
        CRAB_CFG_PUB= '''                                                                                                                                         
config.section_("Data")                                                                                                                                       
config.Data.inputDataset = '{DATASET}'                                                                                                                        
'''


    CRAB_CFG3 = '''
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10

config.Data.outLFNDirBase = '/store/user/%s/NanoPosttest_%s_%s' % ( 'bharikri', '{DATE}' ,idname )
config.Data.publication = False
config.section_("Site")
config.Site.storageSite = "T3_CH_CERNBOX"

'''

    if published :
        CRAB_CFG = CRAB_CFG + CRAB_CFG_PUB +  CRAB_CFG3 
    else :    
        CRAB_CFG = CRAB_CFG + CRAB_CFG_UNPUB +  CRAB_CFG3 

    # open crabConfig.py, substitute into CRAB_CFG the arguments from ARGS, write it, run it, and remove it

    open('%s/crabConfig%s.py'% (dirname , idname ) , 'w').write(CRAB_CFG.format(**ARGS.__dict__))

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


from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *


ch = ROOT.TChain("Events")
if not {ISDATA} :
    jmeCorrections = createJMECorrector(True, "2017", "", "Total", "AK4PFchs")
    modulesList.append( jmeCorrections() )

modulesList.append( MyAnalysisCC( '{ISDATA}'  , ch , [ "output_hists.root",   '{MCORDATA}' ,'{DATATYPE}', '{ERA}' , '{LETTER}' , {XSEC}, {LUMI} , {NEV} ] ))


p = PostProcessor(".",
                      inputFiles(),
                      "(nMuon + nElectron) >=3",
                      modules=modulesList,
                      provenance=True,
                      fwkJobReport=True,noOut=True,
                      histFileName= 'output_hists.root', histDirName = 'lfv',
                      jsonInput=runsAndLumis())


p.run()

print("DONE")

    '''

    open('%s/crab_script_%s.py' % (dirname, idname), 'w').write(CRAB_SCRIPT.format(**ARGS.__dict__))


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

selected=('{SELECTED}')
py_command=('crab_script_')
py_command2=('.py')
echo "$py_command""$selected""$py_command2" $1
python "$py_command""$selected""$py_command2" $1

fi



    '''
    open('%s/crab_script_%s.sh' % (dirname, idname), 'w').write(BASH_SCRIPT.format(**ARGS.__dict__))

    ids.append(idname)

subprocess.call('cp PSet.py %s/PSet.py' % (dirname), shell=True)
subprocess.call('cd %s' % (dirname), shell=True)
subprocess.call('ln -s $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/haddnano.py .', shell=True)

sublist = []
for aid in ids :
    ARGS.ID = aid
#idname%s = '%s'
    subCommand = '''                                                                                                                                         
print " Submitting CRAB job for dataset : %s "                                                                                              
subprocess.call('crab submit -c crabConfig%s.py' , shell=True)                                                                            
subprocess.call('echo "crab submit -c crabConfig%s.py" ' , shell=True)                                                                     
                                                                                                                        
'''% (aid, aid, aid)
 
    sublist.append(subCommand)   
    SUBMIT_SCRIPT += subCommand
#print sublist    

#for s in sublist :
#    SUBMIT_SCRIPT += subCommand

open('%s/crab_submitter.py' % (dirname), 'w').write(SUBMIT_SCRIPT.format(**ARGS.__dict__))
print "You have successfully created CRAB submit scripts =D"
print "now you need to submit your jobs"
print "get a grid proxy by doing : "
print "voms-proxy-init --voms cms"
print "then cd to the CRABtasks directory and run:"
print "python crab_submitter.py"
print "That script will contain commands to run all of the scripts you just created..."
