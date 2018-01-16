import ROOT
import math, os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

"""
@ak8JetIDProducer Package to compute the AK8 jet ID by matching to AK4 jets, in case the AK8 jet ID variables are not stored.

"""
class ak8SubjetVariableProducer(Module):
    def __init__(self):

        self.ak8JetBranchName = "FatJet"
        self.ak8SubJetBranchName = "SubJet"
        self.lenVar = "n" + self.ak8JetBranchName

    def beginJob(self):
        pass
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("%s_msoftdrop_corr" % self.ak8JetBranchName, "F", lenVar=self.lenVar)
        self.out.branch("%s_maxCSVV2"       % self.ak8JetBranchName, "F", lenVar=self.lenVar)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        ak8jets    = Collection(event, self.ak8JetBranchName    )
        ak8subjets = Collection(event, self.ak8SubJetBranchName )

        msds = []
        csvs = []
        for jet in ak8jets:
            sub1Index = jet.subJetIdx1
            sub2Index = jet.subJetIdx2
            msd = -1.0
            maxCSVV2 = -1.0
            if sub1Index >= 0 and sub2Index >= 0:
                groomedjet = ak8subjets[sub1Index].p4() + ak8subjets[sub2Index].p4()
                msd = groomedjet.M()
                maxCSVV2 = max( ak8subjets[sub1Index].btagCSVV2, ak8subjets[sub2Index].btagCSVV2 )
            msds.append(msd)
            csvs.append(maxCSVV2)

        self.out.fillBranch("%s_msoftdrop_corr" % self.ak8JetBranchName, msds)
        self.out.fillBranch("%s_maxCSVV2"       % self.ak8JetBranchName, csvs)
        return True

ak8SubjetVariables = lambda : ak8SubjetVariableProducer()
