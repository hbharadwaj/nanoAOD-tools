from WMCore.Configuration import Configuration

#Taken from example here
#https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3FAQ#crab_submit_fails_with_Block_con

# this will use CRAB client API
from CRABAPI.RawCommand import crabCommand

# talk to DBS to get list of files in this dataset
from dbs.apis.dbsClient import DbsApi
dbs = DbsApi('https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader')

dataset0 = '/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/arizzi-NanoCrabXmasRunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asym___heIV_v6-v1__32-f64d1fc6d0aff52acf7debc448857e96/USER'
fileDictList = dbs.listFiles(dataset=dataset0)

print ("dataset %s has %d files" % (dataset0, len(fileDictList)))

# DBS client returns a list of dictionaries, but we want a list of Logical File Names
lfnList = [ dic['logical_file_name'] for dic in fileDictList ]



config = Configuration()

config.section_("General")
config.General.requestName = 'XmasNanoAOD_DY1_testing0'
config.General.transferLogs= True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
#config.Data.inputDataset = '/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/arizzi-NanoCrabXmasRunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asym___heIV_v6-v1__32-f64d1fc6d0aff52acf7debc448857e96/USER'
#config.Data.inputDBS = 'global'

# following 3 lines are the trick to skip DBS data lookup in CRAB Server
config.Data.userInputFiles = lfnList
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

#config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
#config.Data.unitsPerJob = 1 #100
#config.Data.totalUnits = 2000
#config.Data.inputDBS='phys03'
config.Data.outLFNDirBase = '/store/user/asparker/Xmas_NanoAOD/'
config.Data.publication = False #True
config.Data.outputDatasetTag = 'XmasNanoPost'
config.section_("Site")
#config.Site.storageSite = "T3_US_FNALLPC"

# since there is no data discovery and no data location lookup in CRAB
# you have to say where the input files are
config.Site.whitelist = ['T2_IT_Bari']

config.Site.storageSite = "T3_US_FNALLPC" #'T2_CH_CERN'

result = crabCommand('submit', config = config)

print (result)
