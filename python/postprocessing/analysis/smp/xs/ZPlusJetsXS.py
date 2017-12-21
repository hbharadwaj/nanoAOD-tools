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
        self.mBin = array.array('d', [0, 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]) #array.array('d', [0, 5, 10, 20, 40, 60, 80, 100 ,150, 200, 350])
        self.nbinsm = len(self.mBin) - 1
        self.mBinB = array.array('d', [0, 0.5, 1, 3, 5, 7.5, 10, 15, 20,30, 40,50, 60, 70, 80, 90,100 ,125,150,175, 200,225, 250,275, 300, 325,350])
        self.nbinsmB = len(self.mBinB) - 1

        self.minDPhiZJet = 2.0
        self.minZpt = 200.
        
        #self.addObject( ROOT.TH2F('h_response',   'h_response',   self.nbinsmB, self.mBinB, self.nbinsm, self.mBin) )
        self.addObject( ROOT.TH2F('h_response',   'h_response',   self.nbinsm, self.mBin, self.nbinsm, self.mBin) )
        self.addObject( ROOT.TH1F('h_reco',   'h_reco',   self.nbinsm, self.mBin) )
        self.addObject( ROOT.TH1F('h_gen',    'h_gen',    self.nbinsm, self.mBin) )
        self.addObject( ROOT.TH1F('h_fake',   'h_fake',   self.nbinsm, self.mBin) )
        self.addObject( ROOT.TH1F('h_miss',   'h_miss',   self.nbinsm, self.mBin) )
        self.addObject( ROOT.TH1F('h_drGenReco',    'h_drGenReco',    40, 0, 0.8) )
        self.addObject( ROOT.TH1F('h_drGenGroomed', 'h_drGenGroomed', 40, 0, 0.8) )
                            
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

    def printP4( self, c ):
        if hasattr( c, "p4"):
            s = ' %6.2f %5.2f %5.2f %6.2f ' % ( c.p4().Perp(), c.p4().Eta(), c.p4().Phi(), c.p4().M() )
        else :
            s = ' %6.2f %5.2f %5.2f %6.2f ' % ( c.Perp(), c.Eta(), c.Phi(), c.M() )
        return s
    def printCollection(self,coll):
        for ic,c in enumerate(coll):
            s = self.printP4( c )
            print ' %3d : %s' % ( ic, s )
            
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        weight = 1.0

        
        isMC = event.run == 1
        if self.verbose:
            print '------------------------ ', event.event

        if isMC:
            ###### Get gen Z candidate #######
            allgen = Collection(event, "GenPart")
            zbosons = [ x for x in allgen if abs(x.pdgId) == 23 ]
            genmuons = [ x for x in allgen if abs(x.pdgId) == 13 ]
            if len(zbosons) == 0 :
                return False
            Zboson = zbosons[ len(zbosons)-1]
            if Zboson.p4().Perp() < self.minZpt * 0.9 :
                return False
            if self.verbose:
                print '-----'
                print self.printP4( Zboson )

            ###### Get list of gen jets #######
            # List of gen jets:
            allgenjets = list(Collection(event, "GenJetAK8"))
            if self.verbose:
                print '-----'
                print 'all genjets:'
                self.printCollection( allgenjets )
            genjets = [ x for x in allgenjets if x.p4().Perp() > 150. and x.p4().DeltaPhi( Zboson.p4() ) > self.minDPhiZJet ]
            # List of gen subjets (no direct link from Genjet):
            gensubjets = list(Collection(event, "SubGenJetAK8"))
            # Dictionary to hold ungroomed-->groomed for gen
            genjetsGroomed = {}
            # Get the groomed gen jets
            for igen,gen in enumerate(genjets):
                gensubjetsMatched = self.getSubjets( p4=gen.p4(),subjets=gensubjets, dRmax=0.8)
                genjetsGroomed[gen] = sum( gensubjetsMatched, ROOT.TLorentzVector() ) if len(gensubjetsMatched) > 0 else None
                self.h_drGenGroomed.Fill( gen.p4().DeltaR( genjetsGroomed[gen] ) )
            if self.verbose:
                print '----'
                print 'opposite-Z genjets:'
                for genjet in genjets:
                    sdmassgen = genjetsGroomed[genjet].M() if genjet in genjetsGroomed else -1.0
                    print '         : %s %6.2f' % ( self.printP4(genjet), sdmassgen )            
            

            
        ###### Get reco Z candidate #######
        # List of reco muons
        allmuons = Collection(event, "Muon")
        # Select reco muons:
        muons = [ x for x in allmuons if x.tightId ]
        if len(muons) < 2 :
            return False
        Zcand = muons[0].p4() + muons[1].p4()
        if Zcand.Perp() < self.minZpt or Zcand.M() < 50. or Zcand.M() > 120. :
            return False
        if self.verbose:
            print '-----'
            print ' recoZ:', self.printP4( Zcand )
        
        ###### Get list of reco jets #######
        # List of reco jets:
        allrecojets = list(Collection(event, "FatJet"))
        if self.verbose:
            print '----'
            print 'all recojets:'
            self.printCollection( allrecojets )
        recojets = [ x for x in allrecojets if x.p4().Perp() > 200. and x.p4().DeltaPhi( Zcand ) > self.minDPhiZJet ]
        if isMC == False:
            genjets = [None] * len(recojets)
        # List of reco subjets:
        recosubjets = list(Collection(event,"SubJet"))
        # Dictionary to hold reco--> gen matching
        recoToGen = matchObjectCollection( recojets, genjets, dRmax=0.05 )
        # Dictionary to hold ungroomed-->groomed for reco
        recojetsGroomed = {}        
        # Get the groomed reco jets
        for ireco,reco in enumerate(recojets):
            if reco.subJetIdx1 >= 0 and reco.subJetIdx2 >= 0 :
                recojetsGroomed[reco] = recosubjets[reco.subJetIdx1].p4() + recosubjets[reco.subJetIdx2].p4()
            elif reco.subJetIdx1 >= 0 :
                recojetsGroomed[reco] = recosubjets[reco.subJetIdx1].p4()
            else :
                recojetsGroomed[reco] = None

        if self.verbose:
            print '----'
            print 'opposite-Z recojets:'
            for recojet in recojets:
                sdmassreco = recojetsGroomed[recojet].M() if recojet in recojetsGroomed and recojetsGroomed[recojet] != None else -1.0
                print '         : %s %6.2f' % ( self.printP4( recojet),  sdmassreco )            

                
        # Loop over the reco,gen pairs.
        # Check if there are reco and gen SD jets
        # If both reco+gen: "fill"
        # If only reco: "fake"
        # (See below for "misses")
        for reco,gen in recoToGen.iteritems():
            recoSD = recojetsGroomed[reco]
            if reco == None or recoSD == None :
                continue
            #self.h_reco.Fill( recoSD.M() )
            genval = None
            if gen != None:
                genSD = genjetsGroomed[gen]
                if genSD != None:
                    if self.verbose : 
                        print ' reco: %s %8.4f , gen : %s %8.4f ' % (
                            self.printP4(reco), recoSD.M(),
                            self.printP4(gen), genSD.M()
                            )
                    genval = genSD.M()
                    self.h_response.Fill( genSD.M(), recoSD.M() )
                    self.h_gen.Fill( genSD.M() )                    
                    self.h_reco.Fill( recoSD.M() )
                    self.h_drGenReco.Fill( reco.p4().DeltaR(gen.p4()) )

                    #if recoSD.M() > 10 and genSD.M() > 10 and (genSD.M() / recoSD.M() < 0.5 or genSD.M() / recoSD.M() > 2.0) :
                    if self.verbose:
                        print '---------------------------------'
                        print ' reco: %s %8.4f , gen : %s %8.4f ' % (
                            self.printP4(reco), recoSD.M(),
                            self.printP4(gen), genSD.M()
                            )
                        print 'Z boson:'
                        print self.printP4( Zboson )
                        print 'Z candidate:'
                        print self.printP4( Zcand )
                        print 'Muons:'
                        self.printCollection( muons )
                        print 'Gen jets:'
                        self.printCollection( genjets )
                        print 'Gen subjets:'
                        self.printCollection( gensubjets )
                        print 'Reco jets:'
                        self.printCollection( recojets )
                        print 'Reco subjets:'
                        self.printCollection( recosubjets )
            if genval == None :
                self.h_fake.Fill( recoSD.M() )
        # Now loop over gen jets. If not in reco-->gen list,
        # then we have a "miss"
        for igen,gen in enumerate(genjets):
            if gen != None and gen not in recoToGen.values() :
                genSD = genjetsGroomed[gen]
                if genSD == None :
                    continue
                #self.h_response.Fill( genSD.M(), -1.0 )
                #self.h_gen.Fill( genSD.M() )
                self.h_miss.Fill( genSD.M() )

        return True
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

zplusjetsxs = lambda : ZPlusJetsXS() 
