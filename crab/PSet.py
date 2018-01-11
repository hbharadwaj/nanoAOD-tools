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
        #'/store/user/arizzi/NanoCrabProdXmas/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NanoCrabXmasRunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asym___heIV_v6-v1__32/171221_092730/0000/nano_100.root'
        'file:/uscms_data/d3/aparker/nanoAod/CMSSW_9_4_1/src/PhysicsTools/NanoAOD/test/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8.root'
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('DY1_M-50_TuneCP5-madMLM-pythia8_XmasNano.root'))
process.out = cms.EndPath(process.output)

