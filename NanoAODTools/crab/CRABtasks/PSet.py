# this fake PSET is needed for local test and for crab to figure the output
# filename you do not need to edit it unless you want to do a local test using
# a different input file than the one marked below
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(),
    # lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = [
#'root://cms-xrd-global.cern.ch//store/user/piedavid/topNanoAOD/v6-1-1/2017/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/TopNanoAODv6-1-1_2017/200615_072720/0000/tree_24.root'
'/store/user/piedavid/topNanoAOD/v6-1-1/2017/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv6-1-1_2017/200613_065556/0000/tree_1.root'
#'/store/user/piedavid/topNanoAOD/v6-1-1/2017/MuonEG/TopNanoAODv6-1-1_2017/200615_081001/0000/tree_1.root'#'tree_1.root'#, 'tree_118.root'#, 'tree_9.root' # MC test file
#'tree_15.root'#, 'tree_15.root'

]
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule",
                                  fileName=cms.untracked.string('output_hists.root'), fakeNameForCrab =cms.untracked.bool(True))
process.out = cms.EndPath(process.output)
