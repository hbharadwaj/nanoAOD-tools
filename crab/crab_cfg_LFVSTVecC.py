from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config
#, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'NanoPostprocessorLFVtest_Jan19_LFVStVecC_20FilesPerJob_addSkimFile'
config.General.transferLogs = True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.outputFiles = [ 'output_hists.root', 'tree_Skim.root' ]
config.JobType.scriptExe = 'crab_script_new.sh'
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.inputFiles = ['crab_script_test_new.py', '../scripts/haddnano.py', "/afs/cern.ch/user/a/asparker/public/LFVTopCode_MyFork/nano_cmssw_mc_try2/CMSSW_10_6_4/src/data/TopLFV/input/RoccoR2017.txt","/afs/cern.ch/user/a/asparker/public/LFVTopCode_MyFork/nano_cmssw_mc_try2/CMSSW_10_6_4/src/data/TopLFV/include/MyAnalysis.h", "/afs/cern.ch/user/a/asparker/public/LFVTopCode_MyFork/nano_cmssw_mc_try2/CMSSW_10_6_4/src/data/TopLFV/lib/main.so", "testMC.txt"  ]

config.JobType.sendPythonFolder = True
config.section_("Data")
#config.Data.inputDataset = '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/palencia-TopNanoAODv6-1-1_2017-a11761155c05d04d6fed5a2401fa93e8/USER'

datasetsFile = open( 'LFVtest.txt' )                                                                                                                                 
jobsLines = datasetsFile.readlines()
filelist = [] 
for l in jobsLines:
    filelist.append(str(l[:-1]))
print filelist 
config.Data.userInputFiles = filelist
    

config.Data.inputDBS = 'phys03'
#config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 20
#config.Data.totalUnits = 10

config.Data.outLFNDirBase = '/store/user/%s/NanoPosttest_Jan19_LFVStVecC' % ( 'asparker' )
# getUsernameFromSiteDB())
config.Data.publication = False
#config.Data.outputDatasetTag = 'NanoTestPost_TT_3perjob_goodOutfiles3'
config.section_("Site")
#config.Site.storageSite = "T2_DE_DESY"

config.Site.storageSite = "T2_CH_CERN"
# config.section_("User")
#config.User.voGroup = 'dcms'
config.JobType.allowUndistributedCMSSW = True
