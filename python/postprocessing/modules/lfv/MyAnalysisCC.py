from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TChain, TSelector, TTree
from ROOT import *

import os,sys,inspect

class MyAnalysisCC(Module ):
    def __init__(self, isdata, afileList, loopInfo ):
        self.writeHistFile = True
        self.isdata = isdata
        self.afileList = afileList
        self.ch = ROOT.TChain("Events")
        for line in self.afileList :
            self.ch.Add( line )

        base = "$CMSSW_BASE/src/data"
        
        ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
        print "Load(BASE/TopLFV/lib/main.so"
        gSystem.Load("%s/TopLFV/lib/main.so"%(base) )
        gInterpreter.ProcessLine('#include'+ '"%s/TopLFV/include/MyAnalysis.h"'%(base))


        print("Load C++ MyAnalysis worker module")
  
        print(" Importing MyAnalysis class...")

 
        print  self.ch 
        self.worker = MyAnalysis( self.ch )
        self.loopInfo = loopInfo
  
        pass
        

    def beginJob(self, histFile, histDirName):
        Module.beginJob(self, histFile, histDirName)
        print "beginJob opened histfile"
       
        self.worker.Loop( self.loopInfo[0] , self.loopInfo[1], self.loopInfo[2], self.loopInfo[3], self.loopInfo[4], self.loopInfo[5], self.loopInfo[6], self.loopInfo[7]  )
        print " beginJob ran Loop function from MYANALYSIS"
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.initReaders(inputTree)  # initReaders must be called in beginFile
        self.out = wrappedOutputTree
        #self.out.branch("MHTju_pt", "F")
        #self.out.branch("MHTju_phi", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    # this function gets the pointers to Value and ArrayReaders and sets
    # them in the C++ worker class
    def initReaders(self, tree):
        self.nJet = tree.valueReader("nJet")
        self.Jet_pt = tree.arrayReader("Jet_pt")
        self.Jet_phi = tree.arrayReader("Jet_phi")
        #self.worker.setJets(self.nJet, self.Jet_pt, self.Jet_phi)
        # self._ttreereaderversion must be set AFTER all calls to
        # tree.valueReader or tree.arrayReader
        self._ttreereaderversion = tree._ttreereaderversion

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail,
        go to next event)"""

        # do this check at every event, as other modules might have read
        # further branches
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)
        # do NOT access other branches in python between the check/call to
        # initReaders and the call to C++ worker code
        #output = self.worker.getHT()

        #self.out.fillBranch("MHTju_pt", output[0])
        #self.out.fillBranch("MHTju_phi", -output[1])  # note the minus
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid
# having them loaded when not needed

myan = lambda: MyAnalysisCC()
