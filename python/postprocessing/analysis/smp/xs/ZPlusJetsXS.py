import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

import random
import array

class ZPlusJetsXS(Module):
    def __init__(self ):
        self.writeHistFile = True
        self.verbose = False
    def beginJob(self, histFile, histDirName):
        Module.beginJob(self, histFile, histDirName)
        self.mBin = array.array('d', [0, 5, 10, 20, 40, 60, 80, 100]) #array.array('d', [0, 5, 10, 20, 40, 60, 80, 100 ,150, 200, 350])
        self.nbinsm = len(self.mBin) - 1
        self.mBinB = array.array('d', [0, 2.5, 5, 7.5, 10, 15, 20,30, 40,50, 60, 70, 80, 90,100 ,125,150,175, 200,225, 250,275, 300, 325,350])
        self.nbinsmB = len(self.mBinB) - 1
        
        
        #self.addObject( ROOT.TH2F('h_response',   'h_response',   self.nbinsmB, self.mBinB, self.nbinsm, self.mBin) )
        self.addObject( ROOT.TH2F('h_response',   'h_response',   self.nbinsm, self.mBin, self.nbinsm, self.mBin) )
        self.addObject( ROOT.TH1F('h_reco',   'h_reco',   self.nbinsm, self.mBin) )
        self.addObject( ROOT.TH1F('h_gen',    'h_gen',    self.nbinsm, self.mBin) )
        self.addObject( ROOT.TH1F('h_fake',   'h_fake',   self.nbinsm, self.mBin) )
        self.addObject( ROOT.TH1F('h_miss',   'h_miss',   self.nbinsm, self.mBin) )
    def endJob(self):
        Module.endJob(self)
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def getSubjets(self, p4, subjets, dRmax=0.8):
        ret = []
        for subjet in subjets :
            if p4.DeltaR(subjet.p4()) < dRmax and len(ret) < 2 :
                ret.append(subjet.p4())
        return ret
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        weight = 1.0
            
        recojets = list(Collection(event, "FatJet"))
        recosubjets = list(Collection(event,"SubJet"))
        genjets = list(Collection(event, "GenJetAK8"))
        gensubjets = list(Collection(event, "SubGenJetAK8"))        
        recoToGen = matchObjectCollection( recojets, genjets, dRmax=0.1 )
        genjetsGroomed = {}
        recojetsGroomed = {}
        for igen,gen in enumerate(genjets):
            gensubjetsMatched = self.getSubjets( p4=gen.p4(),subjets=gensubjets, dRmax=0.8)
            genjetsGroomed[gen] = sum( gensubjetsMatched, ROOT.TLorentzVector() ) if len(gensubjetsMatched) > 0 else None
        for ireco,reco in enumerate(recojets):
            if reco.subJetIdx1 >= 0 and reco.subJetIdx2 >= 0 :
                recojetsGroomed[reco] = recosubjets[reco.subJetIdx1].p4() + recosubjets[reco.subJetIdx2].p4()
            elif reco.subJetIdx1 >= 0 :
                recojetsGroomed[reco] = recosubjets[reco.subJetIdx1].p4()
            else :
                recojetsGroomed[reco] = None

        for reco,gen in recoToGen.iteritems():
            recoSD = recojetsGroomed[reco]
            if reco == None or recoSD == None :
                continue
            self.h_reco.Fill( recoSD.M() )
            genval = None
            if gen != None:
                genSD = genjetsGroomed[gen]
                if genSD != None:
                    if self.verbose : 
                        print ' reco: %6.2f %5.2f %5.2f %6.2f %6.2f , gen : %6.2f %5.2f %5.2f %6.2f %6.2f ' % (
                            reco.p4().Perp(), reco.p4().Eta(), reco.p4().Phi(), reco.p4().M(), recoSD.M(),
                            gen.p4().Perp(), gen.p4().Eta(), gen.p4().Phi(), gen.p4().M(), genSD.M()
                            )
                    genval = genSD.M()
                    self.h_response.Fill( genSD.M(), recoSD.M() )
                    self.h_gen.Fill( genSD.M() )                
            if genval == None :
                self.h_fake.Fill( recoSD.M() )
        for igen,gen in enumerate(genjets):
            if gen not in recoToGen.values() :
                genSD = genjetsGroomed[gen]
                if genSD == None :
                    continue
                self.h_response.Fill( genSD.M(), -1.0 )
                self.h_gen.Fill( genSD.M() )
                self.h_miss.Fill( genSD.M() )


        return True
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

zplusjetsxs = lambda : ZPlusJetsXS() 
