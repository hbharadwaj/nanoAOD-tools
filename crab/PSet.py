#this fake PSET is needed for local test and for crab to figure the output filename
#you do not need to edit it unless you want to do a local test using a different input file than
#the one marked below
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = [
	#'../../NanoAOD/test/lzma.root' ##you can change only this line
        #'/store/user/asparker/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/WJetsToLNu_HT-400To600TuneCUETP8M113TeV-madgraphMLM-pythia8RunIISummer16MiniAODv2-PUMoriond17/180115_042519/0000/test80X_NANO_12.root'
        #'/store/user/srappocc/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/TTJetsTuneCUETP8M113TeV-madgraphMLM-pythia8RunIISummer16MiniAODv2-PUMoriond1780XmcRun2/180112_155912/0000/test80X_NANO_81.root',
        #'/store/user/srappocc/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/TTJetsTuneCUETP8M113TeV-madgraphMLM-pythia8RunIISummer16MiniAODv2-PUMoriond1780XmcRun2/180112_155912/0000/test80X_NANO_71.root',
        #'/store/user/srappocc/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/TTJetsTuneCUETP8M113TeV-madgraphMLM-pythia8RunIISummer16MiniAODv2-PUMoriond1780XmcRun2/180112_155912/0000/test80X_NANO_61.root',
        #'/store/user/srappocc/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/TTJetsTuneCUETP8M113TeV-madgraphMLM-pythia8RunIISummer16MiniAODv2-PUMoriond1780XmcRun2/180112_155912/0000/test80X_NANO_51.root',
        '/store/user/srappocc/SingleMuon/SingleMuon_Run2016G-07Aug17-v1/180113_045720/0000/test_data_80X_NANO_10.root'

]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('test_data_80X_NANO.root'))
process.out = cms.EndPath(process.output)

