from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'XmasNanoAOD_DY1_test1'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
config.Data.inputDataset = '/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/arizzi-NanoCrabXmasRunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asym___heIV_v6-v1__32-f64d1fc6d0aff52acf7debc448857e96/USER'
config.Data.inputDBS = 'global'
#config.Data.splitting = 'FileBased'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 100
config.Data.totalUnits = 2000
config.Data.inputDBS='phys03'
config.Data.outLFNDirBase = '/store/user/asparker/XmasNanoAOD/'
config.Data.publication = True
config.Data.outputDatasetTag = 'XmasNanoTestPost'
config.section_("Site")
config.Site.storageSite = "T3_US_FNALLPC"

