import ROOT
import math, os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import matchObjectCollection

"""
@ak8JetIDProducer Package to compute the AK8 jet ID by matching to AK4 jets, in case the AK8 jet ID variables are not stored.

"""
class ak8JetIDProducer(Module):
    def __init__(self):

        self.ak4JetBranchName = "Jet"
        self.ak8JetBranchName = "FatJet"
        self.lenVar = "n" + self.ak8JetBranchName

    def beginJob(self):
        pass
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("%s_jetId" % self.ak8JetBranchName, "F", lenVar=self.lenVar)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        ak4jets = Collection(event, self.ak4JetBranchName )
        ak8jets = Collection(event, self.ak8JetBranchName )
        matchAK4ToAK8 = matchObjectCollection( ak8jets, ak4jets )

        jetid = []
        for x in ak8jets:
            y = matchAK4ToAK8[x]
            if y != None :
                jetid.append( y.jetId )
            else :
                jetid.append(0)

        self.out.fillBranch("%s_jetId" % self.ak8JetBranchName, jetid)
        return True

ak8JetID = lambda : ak8JetIDProducer()
