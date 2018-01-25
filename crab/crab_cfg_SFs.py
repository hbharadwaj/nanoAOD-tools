from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
#config.General.requestName = 'SingleMuon_Run2016G-07Aug17_NanoAODV0-TTbarSemiLepSkim'
config.General.transferLogs= True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_SFs.sh'
config.JobType.inputFiles = ['crab_script_SFs.py','../scripts/haddnano.py','Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
#config.Data.inputDataset = '/SingleMuon/srappocc-SingleMuon_Run2016G-07Aug17-v1-b84139e74cafd5a0bfdaf4226ec7e7b4/USER'
#'/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/srappocc-TTJetsTuneCUETP8M113TeV-madgraphMLM-pythia8RunIISummer16MiniAODv2-PUMoriond1780XmcRun2-4a4b356339e753e24c281c17941d0081/USER'
#'/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/asparker-WJetsToLNuHT-400To600TuneCUETP8M113TeV-madgraphMLM-pythia8RunIISummer16MiniAODv2-PUMoriond17-4a4b356339e753e24c281c17941d0081/USER'
config.Data.inputDBS = 'phys03'


config.Data.splitting = 'EventAwareLumiBased'# 'FileBased'
config.Data.unitsPerJob = 100
config.Data.totalUnits = 2000
config.Data.outLFNDirBase = '/store/user/asparker/NanoAOD_V0-TTbarSkim/'

config.Data.publication = True

config.Data.outputDatasetTag = 'NanoAOD_V0-SkimTest'
config.section_("Site")
config.Site.storageSite = "T3_US_FNALLPC"



