import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

import random
import array

class ZPlusJetsXS_2D(Module):
    def __init__(self ):
        self.writeHistFile = True
        self.verbose = False
    def beginJob(self, histFile, histDirName):
        Module.beginJob(self, histFile, histDirName)
        self.ptbinsGen = array.array('d', [  200., 260., 350., 460., 550., 650., 760., 900., 1000., 1100., 1200., 1300., 13000.])
        self.ptbinsDet = array.array('d', [  200., 260., 350., 460., 550., 650., 760., 900., 1000., 1100., 1200., 1300., 13000.])
        self.nptbinsGen = 4
        self.nptbinsDet = 4
        self.binsGen = array.array('d', [0., 1., 5., 10., 15., 20., 25., 30., 35., 40., 45., 50., 100.]) 
        self.nGen = len(self.binsGen) - 1
        self.binsDet = array.array('d', [0., 0.5, 1., 3., 5., 7.5, 10., 12.5, 15., 17.5, 20., 22.5, 25., 27.5, 30., 32.5, 35., 37.5, 40., 42.5, 45., 47.5, 50., 75., 100.])
        self.nDet = len(self.binsDet) - 1
        self.nDetSD = 18
        self.nGenSD = 9

        ### Kinematics Cuts ###
        ### Considering either
        ###Z - > mu+ mu-  + Jet


        self.minMu0pt = 30.
        self.minMu1pt = 30.
        ### Or
        ### Z - > e+ e-  + Jet
        self.minEl0pt = 80.
        self.minEl1pt = 80.


        self.minZpt = 100.
        self.minZmass = 60.
        self.maxZmass = 120.

        self.minDPhiZJet = 1.57   

        self.minJetPt = 170.

        self.maxObjEta = 2.5

        
        ############################
        
        
        #### 1D - Histograms using TH1Fs and TH2F for response ###
        self.addObject( ROOT.TH2D('h_response',     'h_response',   self.nDetSD, self.binsDet, self.nGenSD, self.binsGen) )
        self.addObject( ROOT.TH1D('h_reco',         'h_reco',       self.nDetSD, self.binsDet) )
        self.addObject( ROOT.TH1D('h_gen',          'h_gen',        self.nGenSD, self.binsGen) )
        self.addObject( ROOT.TH1D('h_fake',         'h_fake',       self.nDetSD, self.binsDet) )
        self.addObject( ROOT.TH1D('h_miss',         'h_miss',       self.nGenSD, self.binsGen) )
        
        self.addObject( ROOT.TH2D('h_response_u',   'h_response_u', self.nDet, self.binsDet, self.nGen, self.binsGen) )
        self.addObject( ROOT.TH1D('h_reco_u',       'h_reco_u',     self.nDet, self.binsDet) )
        self.addObject( ROOT.TH1D('h_gen_u',        'h_gen_u',      self.nGen, self.binsGen) )
        self.addObject( ROOT.TH1D('h_fake_u',       'h_fake_u',     self.nDet, self.binsDet) )
        self.addObject( ROOT.TH1D('h_miss_u',       'h_miss_u',     self.nGen, self.binsGen) )

        self.addObject( ROOT.TH1D('h_genjetpt',     'h_genjetpt',   100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_recojetpt',    'h_recojetpt',  100, 0, 500 ) )
  
    
        ##### 2D - Histograms using TUnfold objects ###

        self.addObject( ROOT.TUnfoldBinning("detectorBinning") )
        self.detectorDistribution=self.detectorBinning.AddBinning("detectorDistribution")
        self.detectorDistribution.AddAxis("pt",self.nptbinsDet,self.ptbinsDet,
                                False, # no underflow bin (not reconstructed)
                                True # overflow bin
                                );
        self.detectorDistribution.AddAxis("mass",self.nDet,self.binsDet,
                                False, # no underflow bin (not reconstructed)
                                True # overflow bin
                                );
        
        self.addObject( ROOT.TUnfoldBinning("generatorBinning") )
        self.generatorDistribution=self.generatorBinning.AddBinning("generatorDistribution")
        self.generatorDistribution.AddAxis("pt",self.nptbinsGen,self.ptbinsGen,
                                False, # no underflow bin (not reconstructed)
                                True # overflow bin
                                );
        self.generatorDistribution.AddAxis("mass",self.nGen,self.binsGen,
                                False, # no underflow bin (not reconstructed)
                                True # overflow bin
                                );        

        self.addObject( ROOT.TUnfoldBinning("signalBinning") )
        self.signalDistribution=self.signalBinning.AddBinning("signalDistribution")
        self.signalDistribution.AddAxis("pt",self.nptbinsGen,self.ptbinsGen,
                                True, # needed for fakes
                                True # overflow bin
                                );
        self.signalDistribution.AddAxis("mass",self.nGen,self.binsGen,
                                True, # needed for fakes
                                True # overflow bin
                                );

        self.addObject( ROOT.TUnfoldBinning("backgroundBinning") )
        self.backgroundDistribution=self.backgroundBinning.AddBinning("backgroundDistribution")
        self.backgroundDistribution.AddAxis("pt",self.nptbinsGen,self.ptbinsGen,
                                False, # no underflow bin (not reconstructed)
                                True # overflow bin
                                );
        self.backgroundDistribution.AddAxis("mass",self.nGen,self.binsGen,
                                False, # no underflow bin (not reconstructed)
                                True # overflow bin
                                );             
        

        self.addObject( self.detectorBinning.CreateHistogram("h_reco") )
        self.addObject( self.generatorBinning.CreateHistogram("h_gen") )
        #self.addObject( self.signalBinning.CreateHistogram("h_sig") )
        #self.addObject( self.backgroundBinning.CreateHistogram("h_fake") )
        self.addObject( ROOT.TUnfoldBinning.CreateHistogramOfMigrations(self.generatorBinning,self.detectorBinning,"h_response") )
        
        
        ### Control plots of observed particles ###
        
        self.addObject( ROOT.TH1D('h_lep0pt',          'h_lep0pt',        40, 0, 200 ) )
        self.addObject( ROOT.TH1D('h_lep0eta',         'h_lep0eta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_lep0phi',         'h_lep0phi',      100, -5, 5 ) )

        self.addObject( ROOT.TH1D('h_lep1pt',          'h_lep1pt',        40, 0, 200 ) )
        self.addObject( ROOT.TH1D('h_lep1eta',         'h_lep1eta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_lep1phi',         'h_lep1phi',      100, -5, 5 ) )

        self.addObject( ROOT.TH1D('h_zpt',          'h_zpt',        100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_zeta',         'h_zeta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_zphi',         'h_zphi',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_zmass',        'h_zmass',      100, 50, 150 ) )

        self.addObject( ROOT.TH1D('h_genjetpt',          'h_genjetpt',   100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_genjeteta',         'h_genjeteta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_genjetphi',         'h_genjetphi',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_genjetmass',        'h_genjetmass',      300, 0, 300 ) )

        self.addObject( ROOT.TH1D('h_recojetpt',          'h_recojetpt',  100, 0, 500 ) )
        self.addObject( ROOT.TH1D('h_recojeteta',         'h_recojeteta',      48, -3, 3 ) )
        self.addObject( ROOT.TH1D('h_recojetphi',         'h_recojetphi',      100, -5, 5 ) )
        self.addObject( ROOT.TH1D('h_recojetmass',        'h_recojetmass',      300, 0, 300 ) )

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
            ###### Get gen Z candidate #######
            genleptons = Collection(event, "GenDressedLepton")
            
            #### 2 same flavor opposite charge leptons (muon or electron)
            if len(genleptons) < 2 :
                return False
            if abs(genleptons[0].pdgId) != 13 or abs(genleptons[0].pdgId) != 12 :
                return False
            if abs(genleptons[1].pdgId) != 13 or abs(genleptons[1].pdgId) != 12 :
                return False                

            if  abs(genleptons[0].pdgId) != abs(genleptons[1].pdgId) :
                return False  
            if  genleptons[0].charge * -1 != genleptons[1].charge :
                return False   

            if abs(genleptons[0].pdgId) == 12  :   
                if genleptons[0].p4().Perp() < self.minEl0pt * 0.9 or   genleptons[1].p4().Perp() < self.minEl1pt * 0.9 :
                    return False
                if abs(genleptons[1].p4().Eta()) > self.maxObjEta or  abs(genleptons[0].p4().Eta()) > self.maxObjEta:
                    return False  

            if abs(genleptons[0].pdgId) == 13  :   
                if genleptons[0].p4().Perp() < self.minMu0pt * 0.9 or   genleptons[1].p4().Perp() < self.minMu1pt * 0.9 :
                    return False
                if abs(genleptons[1].p4().Eta()) > self.maxObjEta or  abs(genleptons[0].p4().Eta()) > self.maxObjEta:
                    return False     

            if self.verbose :
                print '----'
                print 'Gen leptons:'
                self.printCollection( genleptons )
            Zboson = genleptons[0].p4() + genleptons[1].p4()
            if Zboson.Perp() < self.minZpt * 0.9 :
                return False
            if self.verbose:
                print '-----'
                print 'Gen Z:'
                print self.printP4( Zboson )

            ###### Get list of gen jets #######
            # List of gen jets:
            allgenjets = list(Collection(event, "GenJetAK8"))
            if self.verbose:
                print '-----'
                print 'all genjets:'
                self.printCollection( allgenjets )
            genjets = [ x for x in allgenjets if x.p4().Perp() > self.minJetPt * 0.8 and x.p4().DeltaPhi( Zboson ) > self.minDPhiZJet ss .  ]
            # List of gen subjets (no direct link from Genjet):
            gensubjets = list(Collection(event, "SubGenJetAK8"))
            # Dictionary to hold ungroomed-->groomed for gen
            genjetsGroomed = {}
            # Get the groomed gen jets
            for igen,gen in enumerate(genjets):
                gensubjetsMatched = self.getSubjets( p4=gen.p4(),subjets=gensubjets, dRmax=0.8)
                for isub,sub in enumerate(gensubjetsMatched) : 
                    self.h_drGenGroomed.Fill( gen.p4().DeltaR( sub ) )
                genjetsGroomed[gen] = sum( gensubjetsMatched, ROOT.TLorentzVector() ) if len(gensubjetsMatched) > 0 else None
                
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
        muons = [ x for x in allmuons if (x.tightId and  x.p4().Perp() > self.minMu1pt and abs(x.p4().Eta()) < self.maxObjEta)]
 
        # List of reco electrons
        allelectrons = Collection(event, "Electron")
        # Select reco muons:
        electrons = [ x for x in allelectrons if ( x.tightId and x.p4().Perp() > self.minEl1pt and abs(x.p4().Eta()) < self.maxObjEta  )]


        if len(muons) < 2 and len(electrons) < 2:
            return False
        lep0 = ROOT.TLorentzVector()
        lep1 = ROOT.TLorentzVector() 
        Zismu = -1   
        if len(muons) >= 2 and len(electrons) < 2:           
            Zcand = muons[0].p4() + muons[1].p4()
            lep0 = muons[0].p4()
            lep1 = muons[1].p4()
            Zismu = 1

        elif len(muons) < 2 and len(electrons) >= 2:           
            Zcand = electrons[0].p4() + electrons[1].p4()
            lep0 = electrons[0].p4()
            lep1 = electrons[1].p4()
            Zismu = 0
        elif  len(muons) >= 2 and len(electrons) >= 2:
            if  muons[0].p4().Perp() >  electrons[0].p4().Perp() :
                Zcand = muons[0].p4() + muons[1].p4()
                lep0 = muons[0].p4()
                lep1 = muons[1].p4()
                Zismu = 1
            else :
                Zcand = electrons[0].p4() + electrons[1].p4()
                lep0 = electrons[0].p4()
                lep1 = electrons[1].p4()
                Zismu = 0                

        if Zcand.Perp() < self.minZpt or Zcand.M() < self.minZmass or Zcand.M() > self.maxZmass :
            return False

        self.h_lep0pt.Fill(lep0.Perp())
        self.h_lep0eta.Fill(lep0.Eta())
        self.h_lep0phi.Fill(lep0.Phi())

        self.h_lep1pt.Fill(lep0.Perp())
        self.h_lep1eta.Fill(lep0.Eta())
        self.h_lep1phi.Fill(lep0.Phi())

        self.h_zpt.Fill( Zcand.Perp() )
        self.h_zmass.Fill( Zcand.M() )
        self.h_zeta.Fill( Zcand.Eta() )
        self.h_zphi.Fill( Zcand.Phi() )
        self.h_zismu.Fill( Zismu )        

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
        recojets = [ x for x in allrecojets if x.p4().Perp() > self.minJetPt and x.p4().DeltaPhi( Zcand ) > self.minDPhiZJet and abs(x.p4().Eta()) < self.maxObjEta ]
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
            if reco == None :
                continue
            # Always fill the ungroomed det    
            self.h_reco_u.Fill( reco.p4().M() )    
            if recoSD != None :
                
                # Fill the groomed det if available 
                #1D
                self.h_reco.Fill( recoSD.M() )
                #2D
                binNumberReco=self.detectorDistribution.GetGlobalBinNumber(reco.p4().Perp(), recoSD.M() )
                self.h_reco.Fill( binNumberReco )

            # Now check ungroomed gen
            genSDVal = None
            if gen != None:
                
                
                # Ungroomed gen OK, fill ungroomed response and truth
                self.h_response_u.Fill( reco.p4().M(), gen.p4().M() )
                self.h_gen_u.Fill( gen.p4().M() )
                
                self.h_drGenReco.Fill( reco.p4().DeltaR(gen.p4()) 
                                      
                self.h_genjetpt.Fill( gen.p4().Perp() )                      
                self.h_genjeteta.Fill( gen.p4().Eta() )
                self.h_genjetphi.Fill( gen.p4().Phi() )
                self.h_genjetmass.Fill( gen.p4().M()  )


                self.h_recojetpt.Fill(   reco.p4().Perp() )
                self.h_recojeteta.Fill(  reco.p4().Eta()  )
                self.h_recojetphi.Fill(  reco.p4().Phi()  )
                self.h_recojetmass.Fill( reco.p4().M()    )

                genSD = genjetsGroomed[gen]
                if recoSD != None and genSD != None:
                    # Groomed gen OK, fill groomed response and truth
                    binNumberGen=self.generatorDistribution.GetGlobalBinNumber(gen.p4().Perp(), genSD.M() )
                    self.h_gen.Fill( binNumberGen )
                    self.h_response.Fill( binNumberReco, binNumberGen )
                    genSDVal = genSD.M()
                                        
                    if self.verbose : 
                        print ' reco: %s %8.4f, gen : %s %8.4f ' % (
                            self.printP4(reco), recoSD.M(), 
                            self.printP4(gen), genSD.M()
                            )
                     genSDVal = genSD.M()                 
                     self.h_response.Fill( recoSD.M(), genSD.M() )
                     self.h_gen.Fill( genSD.M() )
            else :
                # Here we have a groomed det, but no groomed gen. Groomed fake. 
                if genSDVal == None and recoSD != None :
                    #1D                  
                    self.h_fake.Fill( recoSD.M() )                   
                    #2D                  
                    binNumberBkg=self.backgroundDistribution.GetGlobalBinNumber( reco.p4().Perp(), recoSD.M() )
                    self.h_gen.Fill( binNumberBkg )
        # Now loop over gen jets. If not in reco-->gen list,
        # then we have a "miss"
        for igen,gen in enumerate(genjets):
            if gen != None and gen not in recoToGen.values() :
                genSD = genjetsGroomed[gen]
                # Groomed miss: check if there is a groomed gen.
                # If there isn't, it gets skipped. 
                if genSD == None :
                    continue
                # 1D 
                #Ungroomed miss: 
                self.h_response_u.Fill( -1.0, gen.p4().M() )
                self.h_gen_u.Fill(gen.p4().M())
                self.h_miss_u.Fill(gen.p4().M())
                # groomed with Soft Drop miss :                      
                self.h_response.Fill( -1.0, genSD.M() )
                self.h_gen.Fill( genSD.M() )
                self.h_miss.Fill( genSD.M() )                     
                                      
                                     
                # 2D
                binNumberGen=self.generatorDistribution.GetGlobalBinNumber(gen.p4().Perp(), genSD.M() )
                self.h_response.Fill( 0, binNumberGen )
                self.h_gen.Fill( binNumberGen )
               


        return True
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

zplusjetsxs = lambda : ZPlusJetsXS_2D() 
