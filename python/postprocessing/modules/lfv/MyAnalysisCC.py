from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetSmearer import jetSmearer
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TChain, TSelector, TTree
from ROOT import *

import os,sys,inspect

class MyAnalysisCC(Module ):
    def __init__(self , isdata, afileList, loopInfo ):
        self.writeHistFile = True
        self.isdata = isdata
        self.afileList = afileList#[#0]
        self.elist  = None #afileList[1]

   
        if self.elist != None :
            print "GetEntries for Events tree"
            print self.afileList.GetEntries()
            print "Get number of entries passing preselection"  
            print self.elist.GetN()
            self.afileList.SetEntryList(self.elist)

        #self.ch = ROOT.TChain("Events")
        #for line in self.afileList :
        #    self.ch.Add( line )
        #print "$CMSSW_BASE"
        #print $CMSSW_BASE
        #os.system( "echo $CMSSW_BASE" )
        self.base = os.environ['CMSSW_BASE'] + '/src/data'  #"$CMSSW_BASE/src/data"   #"../../../data"  #"$CMSSW_BASE/src/data"
        #print " os.environ['CMSSW_BASE'] + '/src/data'" 
        #print base
        #print os.environ['CMSSW_BASE']        
        ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
        #print "Load(BASE/TopLFV/lib/main.so"
        gSystem.Load("%s/TopLFV/lib/main.so"%(self.base) )
        #if isdata:
        #    gInterpreter.ProcessLine('#include '+ '"%s/TopLFV/include/MyAnalysisData.h"'%(self.base))
        #else :
        #    gInterpreter.ProcessLine('#include '+ '"%s/TopLFV/include/MyAnalysis.h"'%(self.base))


        print("Load C++ MyAnalysis worker module")
  
        #print(" Importing MyAnalysis class...")

        #print "Give input files to MyAnalysis class in TChain"
        #print  self.ch 
        self.loopInfo = loopInfo
        #if self.dontRun :
        #    print "not looping"
        #else :
        #elif self.histFileName is not None and self.histDirName is not None:
        #self.histFileName = "output_hists.root"
        print self.loopInfo

        #self.worker.Loop( self.loopInfo[0] , self.loopInfo[1], self.loopInfo[2], self.loopInfo[3], self.loopInfo[4], self.loopInfo[5], self.loopInfo[6], self.loopInfo[7]  )
        #print " _init_ ran Loop function from MYANALYSIS"


        #JMR - make sure the numbers correspond with jetmetUncertainties.py
        self.jmrVals = []
        if '16' in self.loopInfo[3]  :
            self.jmrVals = [1.0, 1.2, 0.8] #nominal, up, down
        elif '17' in self.loopInfo[3]  :
            self.jmrVals = [1.09, 1.14, 1.04]
        elif '18' in self.loopInfo[3]  :
            self.jmrVals = [1.108, 1.142, 1.074]
        print "JMR values:"
        print self.jmrVals


        #JER for MC
        #global tags
        globalTag = "Summer16_07Aug2017_V11_MC" #2016
        if '17' in self.loopInfo[3] :
            globalTag = "Fall17_17Nov2017_V32_MC" #2017
        elif '18' in self.loopInfo[3]  :
            globalTag = "Autumn18_V19_MC"

        #jer input files # Fall17_17Nov2017_V32 94X_mc2017_realistic_v17
        self.jerInputFileName = "Summer16_25nsV1_MC_PtResolution_AK4PFPuppi.txt"
        self.jerUncertaintyInputFileName = "Summer16_25nsV1_MC_SF_AK4PFPuppi.txt"
        if '17MC' in self.loopInfo[3] :
            self.jerInputFileName = "Fall17_V3_MC_PtResolution_AK4PFPuppi.txt"
            self.jerUncertaintyInputFileName = "Fall17_V3_MC_SF_AK4PFPuppi.txt"
        elif '18MC' in self.loopInfo[3] :
            self.jerInputFileName = "Autumn18_V7b_MC_PtResolution_AK4PFPuppi.txt"
            self.jerUncertaintyInputFileName = "Autumn18_V7b_MC_SF_AK4PFPuppi.txt"    



        self.jetSmearer = None
        if 'mc' in self.loopInfo[1] : self.jetSmearer = jetSmearer(globalTag, "AK4PFPuppi", self.jerInputFileName, self.jerUncertaintyInputFileName, self.jmrVals)

        print "JetSmearer"
        print self.jetSmearer 

  
        pass
        
    def runloop(self,  atree ):
        #self.afileList = atree
        print "runloop will give ttree to MyAnalysis Loop"
        ROOT.SetOwnership(atree, False )
        print atree        
        self.worker = MyAnalysis( atree ) #self.afileList )
        self.worker.Loop( self.loopInfo[0] , self.loopInfo[1], self.loopInfo[2], self.loopInfo[3], self.loopInfo[4], self.loopInfo[5], self.loopInfo[6], self.loopInfo[7] , self.jetSmearer )
        ROOT.SetOwnership( self.worker, False )
        print "runloop ran MyAnalysis Loop"
        pass


    #def addTree(self, atree ):
    #    self.afileList = atree
    #    pass

    def beginJob(self, histFile, histDirName):

        Module.beginJob(self, histFile, histDirName)
        print "beginJob did not open histfile"
        #print self.afileList 
        #self.worker = MyAnalysis( self.afileList)#ch)
        #self.worker.Loop( self.loopInfo[0] , self.loopInfo[1], self.loopInfo[2], self.loopInfo[3], self.loopInfo[4], self.loopInfo[5], self.loopInfo[6], self.loopInfo[7]  )
        #print " beginJob ran Loop function from MYANALYSIS"
        #self.worker.Loop( self.loopInfo[0] , self.loopInfo[1], self.loopInfo[2], self.loopInfo[3], self.loopInfo[4], self.loopInfo[5], self.loopInfo[6], self.loopInfo[7]  )
        #print " beginJob ran Loop function from MYANALYSIS"

        if 'mc' in self.loopInfo[1] :  self.jetSmearer.beginJob()
  
    def endJob(self):

        if 'mc' in self.loopInfo[1] :  self.jetSmearer.endJob()

        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

        if self.isdata:
            gInterpreter.ProcessLine('#include '+ '"%s/TopLFV/include/MyAnalysisData.h"'%(self.base))
        else :
            gInterpreter.ProcessLine('#include '+ '"%s/TopLFV/include/MyAnalysis.h"'%(self.base))




        #self.initReaders(inputTree)  # initReaders must be called in beginFile
        #self.out = wrappedOutputTree
        #self.out.branch("MHTju_pt", "F")
        #self.out.branch("MHTju_phi", "F")
        print "beginfile"
        pass


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
