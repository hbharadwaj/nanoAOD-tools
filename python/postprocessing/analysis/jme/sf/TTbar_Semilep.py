import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

import random
import array

class TTbar_SemiLep(Module):
    def __init__(self ):
        self.writeHistFile = True
        self.verbose = False
    def beginJob(self, histFile, histDirName):
        Module.beginJob(self, histFile, histDirName)

        self.isttbar = False
        if 'TTJets_' in histFile :
           self.isttbar = True 

        self.minMupt = 53.
        self.maxMuEta = 2.1
        self.maxRelIso = 0.1
        self.minMuMETPt = 40.
        #is High Pt
        #remove jet within 0.3
        #veto:
        # High pT muon ID
        #pT > 20 GeV, eta < 2.4??
        #relIso < 0.1


        #self.minElpt = 120.
        #self.minElMETPt = 80.
        #self.goodElEta = if eta < 1.44, 1.56 < eta < 2.5
        # HEEP v7 + iso
        #veto
        # HEEP + iso pt > 35 remove ecal crack region eta < 1.44, 1.56 < eta < 2.5
        #

        self.minLepWPt = 200.

        self.minJetPt = 200.

        self.minTopmass = 140.
        self.maxTopmass = 200.

        #>= 1 CSVmedium akt4 jet, pT > 30 GeV
        self.minAK4Pt = 30.

        #Angular selection (not used by Thea now):

        #dR( lepton, leading AK8 jet) > pi/2
        #dPhi(leading AK8 jet, MET) > 2
        
        #dPhi (leading AK8 jet, leptonic W) >2
        self.minDPhiWJet = 2.  

        self.addObject( ROOT.TH1D('h_lep0pt',          'h_lep0pt',        40, 0, 200 ) )
        self.addObject( ROOT.TH1D('h_lep0eta',         'h_lep0eta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_lep0phi',         'h_lep0phi',      100, -5, 5 ) )

        self.addObject( ROOT.TH1D('h_toppt',          'h_toppt',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_topeta',         'h_topeta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_topphi',         'h_topphi',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_topmass',        'h_topmass',      60, 140, 200 ) )

        self.addObject( ROOT.TH1D('h_wpt',          'h_wpt',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_weta',         'h_weta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_wphi',         'h_wphi',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_wmass',        'h_wmass',      100, 50, 150 ) )

        self.addObject( ROOT.TH1D('h_wpt_ptbin0',          'h_wpt_ptbin0',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_weta_ptbin0',         'h_weta_ptbin0',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_wphi_ptbin0',         'h_wphi_ptbin0',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_wmass_ptbin0',        'h_wmass_ptbin0',      100, 50, 150 ) )

        self.addObject( ROOT.TH1D('h_wpt_ptbin1',          'h_wpt_ptbin1',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_weta_ptbin1',         'h_weta_ptbin1',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_wphi_ptbin1',         'h_wphi_ptbin1',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_wmass_ptbin1',        'h_wmass_ptbin1',      100, 50, 150 ) )

        self.addObject( ROOT.TH1D('h_wpt_ptbin2',          'h_wpt_ptbin2',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_weta_ptbin2',         'h_weta_ptbin2',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_wphi_ptbin2',         'h_wphi_ptbin2',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_wmass_ptbin2',        'h_wmass_ptbin2',      100, 50, 150 ) )

        self.addObject( ROOT.TH1D('h_wleppt',          'h_wleppt',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_wlepeta',         'h_wlepeta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_wlepphi',         'h_wlepphi',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_wlepmass',        'h_wlepmass',      100, 50, 150 ) )


        self.addObject( ROOT.TH1D('h_genjetpt',          'h_genjetpt',   100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_genjeteta',         'h_genjeteta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_genjetphi',         'h_genjetphi',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_genjetmass',        'h_genjetmass',      300, 0, 300 ) )

        self.addObject( ROOT.TH1D('h_recoAK8jetpt',          'h_recoAK8jetpt',  100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_recoAK8jeteta',         'h_recoAK8jeteta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_recoAK8jetphi',         'h_recoAK8jetphi',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_recoAK8jetmass',        'h_recoAK8jetmass',      300, 0, 300 ) )

        if self.isttbar :
            self.addObject( ROOT.TH1D('h_matchedAK8jetpt',          'h_matchedAK8jetpt',      100, 0, 500 ) )
            self.addObject( ROOT.TH1D('h_matchedAK8jeteta',         'h_matchedAK8jeteta',      48, -3, 3 ) )
            self.addObject( ROOT.TH1D('h_matchedAK8jetphi',         'h_matchedAK8jetphi',      100, -5, 5 ) )
            self.addObject( ROOT.TH1D('h_matchedAK8jetmass',        'h_matchedAK8jetmass',      300, 0, 300 ) )

            self.addObject( ROOT.TH1D('h_unmatchedAK8jetpt',          'h_unmatchedAK8jetpt',      100, 0, 500 ) )
            self.addObject( ROOT.TH1D('h_unmatchedAK8jeteta',         'h_unmatchedAK8jeteta',      48, -3, 3 ) )
            self.addObject( ROOT.TH1D('h_unmatchedAK8jetphi',         'h_unmatchedAK8jetphi',      100, -5, 5 ) )
            self.addObject( ROOT.TH1D('h_unmatchedAK8jetmass',        'h_unmatchedAK8jetmass',      300, 0, 300 ) )



        self.addObject( ROOT.TH1D('h_drGenReco',    'h_drGenReco',   40, 0, 0.8) )
        self.addObject( ROOT.TH1D('h_drGenGroomed', 'h_drGenGroomed',40, 0, 0.8) )
                            
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
            ###### Get gen Top candidate #######
            genleptons = Collection(event, "GenDressedLepton")

            if len(genleptons) < 1 :
                return False
            if abs(genleptons[0].pdgId) != 13 :
                return False
            if genleptons[0].p4().Perp() < self.minMu0pt * 0.9 :
                return False
            genAK4s = Collection(event, "GenJet")    # are these Ak4s ?
            genAK4jets = [ x for x in genAK4s if x.p4().Perp() > self.minAK4Pt * 0.8 ]
            if self.verbose :
                print '----'
                print 'Gen leptons:'
                self.printCollection( genleptons )

            METgen = Collection(event, "GenMET") # this may not be correct syntax
            WLep = genleptons[0].p4() + METgen[0].p4()
            if WLep.Perp() < self.minLepWPt * 0.9 :
                return False
            if self.verbose:
                print '-----'
                print 'Gen W Leptonic:'
                print self.printP4( WLep )

            ###### Get list of gen jets #######
            # List of gen jets:
            allgenjets = list(Collection(event, "GenJetAK8"))
            if self.verbose:
                print '-----'
                print 'all genjets:'
                self.printCollection( allgenjets )
            genjets = [ x for x in allgenjets if x.p4().Perp() > self.minJetPt * 0.8 and x.p4().DeltaPhi( WbosonLep ) > self.minDPhiWJet     ]
            # List of gen subjets (no direct link from Genjet):
            gensubjets = list(Collection(event, "SubGenJetAK8"))
            # Dictionary to hold ungroomed-->groomed for gen
            genjetsGroomed = {}
            # Get the groomed gen jets
            maxSubjetMass = 1.
            for igen,gen in enumerate(genjets):
                gensubjetsMatched = self.getSubjets( p4=gen.p4(),subjets=gensubjets, dRmax=0.8)
                for isub,sub in enumerate(gensubjetsMatched) : 
                    if sub.p4().M() > maxSubjetMass : maxSubjetMass = sub.p4().M() 
                    self.h_drGenGroomed.Fill( gen.p4().DeltaR( sub ) )
                genjetsGroomed[gen] = sum( gensubjetsMatched, ROOT.TLorentzVector() ) if (len(gensubjetsMatched) > 0 and sum( gensubjetsMatched, ROOT.TLorentzVector() ).p4().Perp() > self.minJetPt *0.8 and sum( gensubjetsMatched, ROOT.TLorentzVector() ).p4().M() > self.minTopmass  *0.8 )else None
                
            if self.verbose:
                print '----'
                print 'opposite-LepW genjets:'
                for genjet in genjets:
                    sdmassgen = genjetsGroomed[genjet].M() if genjet in genjetsGroomed else -1.0
                    print '         : %s %6.2f' % ( self.printP4(genjet), sdmassgen )            
            

            
        ###### Get reco Top candidate #######
        # List of reco muons
        allmuons = Collection(event, "Muon")
        # Select reco muons:
        muons = [ x for x in allmuons if x.tightId ]
        if len(muons) < 1 :
            return False
        if muons[0].p4().Perp() < self.minMupt    :
                return False    

        MET = Collection(event, "MET") # this may not be correct syntax
        if MET[0].p4().Perp() < self.minMuMETPt :
            return False
        WcandLep = muons[0].p4() + MET[0].p4()
        if WcandLep.Perp() < self.minWpt or WcandLep.M() < self.minWmass or WcandLep.M() > self.maxWmass :
            return False

        allrecoAK4jets = list(Collection(event, "Jet")) # are these AK4s ? 
        recojetsAK4 = [ x for x in allrecoAK4jets if x.p4().Perp() > self.minAK4Pt ]

        Topcand =  WcandLep +  recojetsAK4[0].p4()  
        self.h_toppt.Fill( Topcand.Perp() )
        self.h_topmass.Fill( Topcand.M() )
        if self.verbose:
            print '-----'
            print ' reco Top Leptonic:', self.printP4( Topcand)
        
        ###### Get list of reco jets #######
        # List of reco jets:
        allrecojets = list(Collection(event, "FatJet"))
        if self.verbose:
            print '----'
            print 'all recojets:'
            self.printCollection( allrecojets )
        recojets = [ x for x in allrecojets if x.p4().Perp() > self.minJetPt and x.p4().DeltaPhi( Topcand ) > self.minDPhiWJet and  x.p4().M() > self.minTopmass ]
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

        for reco,gen in recoToGen.iteritems():
            recoSD = recojetsGroomed[reco]
            if reco == None :
                continue
            #if recoSD != None :
            #    # Fill the groomed det if available

            # Now check ungroomed gen
            genSDVal = None
            if gen != None:
                if self.isttbar :
                    self.h_matchedAK8jetpt.Fill(recoSD.Perp())
                    self.h_matchedAK8jeteta.Fill(recoSD.Eta())
                    self.h_matchedAK8jetphi.Fill(recoSD.Phi())
                    self.h_matchedAK8jetmass.Fill(recoSD.M())
                    
                self.h_drGenReco.Fill( reco.p4().DeltaR(gen.p4()) )

                genSD = genjetsGroomed[gen]
                if recoSD != None and genSD != None:
                    genSDVal = genSD.M()
                                        
                    if self.verbose : 
                        print ' reco: %s %8.4f, gen : %s %8.4f ' % (
                            self.printP4(reco), recoSD.M(), 
                            self.printP4(gen), genSD.M()
                            )

            elif  :
                # Here we have a groomed det, but no groomed gen
                if genSDVal == None and recoSD != None :
                    if self.isttbar :
                        self.h_unmatchedAK8jetpt.Fill(recoSD.Perp())
                        self.h_unmatchedAK8jeteta.Fill(recoSD.Eta())
                        self.h_unmatchedAK8jetphi.Fill(recoSD.Phi())
                        self.h_unmatchedAK8jetmass.Fill(recoSD.M())

        return True
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ttbar_semilep = lambda : TTbar_SemiLep() 
