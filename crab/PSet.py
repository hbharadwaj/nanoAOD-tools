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
#'tree_23TEST.root'
#'/store/user/piedavid/topNanoAOD/v6-1-1/2017/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/TopNanoAODv6-1-1_2017/200615_072720/0000/tree_23.root'
#'tree_3.root',
#'/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_155453/0000/tree_9.root'
'tree_9.root'

]
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule",
                                  fileName=cms.untracked.string('output_hists.root'), fakeNameForCrab =cms.untracked.bool(True))
process.out = cms.EndPath(process.output)
