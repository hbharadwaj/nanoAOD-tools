import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

import random
# Temporary problem with ROOT, it looks like this works:
import os
ROOT.gSystem.Load( '%s/standalone/libAnalysisPredictedDistribution.so' % ( os.getenv('PREDDIST_DIR') ) ) 


class TTbarResAnaHadronic(Module):
    def __init__(self, htCut=1100., minMSD=110., maxMSD=240., tau32Cut=0.6, writePredDist=False ):
        self.htCut = htCut
        self.minMSD = minMSD
        self.maxMSD = maxMSD
        self.tau32Cut = tau32Cut
        self.writePredDist = writePredDist
        self.writeHistFile = True
            
        
    def beginJob(self, histFile, histDirName):
        Module.beginJob(self, histFile, histDirName)
        self.addObject( ROOT.TH1F('h_ak4ht',   'h_ak4ht',   25, 0, 2500) )
        self.addObject( ROOT.TH1F('h_ak8pt',   'h_ak8pt',   25, 0, 2500) )
        self.addObject( ROOT.TH1F('h_ak8msd',  'h_ak8msd',  25, 0, 500) )
        self.addObject( ROOT.TH1F('h_ak8tau32','h_ak8tau32',25, 0, 1.0) )
        self.addObject( ROOT.TH1F('h_ak8n3b1', 'h_ak8n3b1', 25, 0, 5.0) )
        self.addObject( ROOT.TH1F('h_mttbar',  'h_mttbar',  25, 0, 5000) )

        if not self.writePredDist:
            self.predFile = ROOT.TFile( "ttbarreshad_predfile.root" )
            self.hpred = self.predFile.Get( "ttbarres/preddist" )
            print self.hpred
            # PredictedDistribution needs to own this to ensure it doesn't go out of scope. 
            ROOT.SetOwnership( self.hpred, False )
            self.addObject( ROOT.PredictedDistribution(self.hpred, "predJetP", "Jet p_{T} (GeV)", 30, 0, 3000.) )
            self.addObject( ROOT.PredictedDistribution(self.hpred, "predJetMTTBAR", "M_{TTBAR} (GeV)", 50, 0.0, 5000.))
            self.addObject( ROOT.PredictedDistribution(self.hpred, "predJetMTTBARMod", "M_{TTBAR} (GeV)", 50, 0.0, 5000.))
            self.addObject( ROOT.PredictedDistribution(self.hpred, "predJetSDMass", "Soft Drop Mass", 50, 0.0, 250.))
            self.addObject( ROOT.PredictedDistribution(self.hpred, "predJetMass", "Ungroomed Jet Mass", 50, 0.0, 250.))
            self.addObject( ROOT.PredictedDistribution(self.hpred, "predJetMassMod", "Ungroomed Jet Mass", 50, 0.0, 250.))
            self.addObject( ROOT.PredictedDistribution(self.hpred, "predJetSDRho", "Soft Drop Rho", 50, 0.0, 1.))

            # PredictedDistribution needs to own these also. 
            for hist in [
                    self.predJetP, self.predJetMTTBAR,
                    self.predJetMTTBARMod,
                    self.predJetSDMass, self.predJetMass, self.predJetMassMod,
                    self.predJetSDRho ] : 
                ROOT.SetOwnership( hist, False )
        else:
            self.addObject( ROOT.TH1D("preddist", "preddist", 25, 0, 2500) )
            
    def endJob(self):
        # Calculate the correlated and uncorrelated errors.
        if not self.writePredDist:
            for hist in [
                    self.predJetP, self.predJetMTTBAR,
                    self.predJetMTTBARMod,
                    self.predJetSDMass, self.predJetMass, self.predJetMassMod,
                    self.predJetSDRho ] : 
                hist.SetCalculatedErrors()
        Module.endJob(self)
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def passTopTag(self, jet):
        tau32 = jet.tau3 / jet.tau2 if jet.tau2 > 0.0 else 0.
        passTau32 = tau32 < self.tau32Cut 
        passMSD = self.minMSD < jet.msoftdrop < self.maxMSD
        return passTau32 and passMSD
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        # First check the trigger
        #passTrig = event.HLT_AK8PFHT800_TrimMass50 or event.HLT_AK8PFHT850_TrimMass50 or event.HLT_PFHT1050
        #if not passTrig :
        #    return False
        
        # Next do the PU weighting
        weight = 1.0
        weight *= event.puWeight

        

        
        ak4jets = list(Collection(event, "Jet"))
        ak8jets = list(Collection(event, "FatJet"))

        # Now get the AK4 and AK8 jets that pass the selection, and HT. Note: Jet ID only stored for
        # AK4 jets so match to them for jet ID.
        ak8MatchedToAK4 = matchObjectCollection( ak8jets, ak4jets )  # For Jet ID
        passedAK4Jets = [x for x in ak4jets if x.jetId>0 and x.pt>20 and abs(x.eta)<2.5]
        ht = sum( [ j.pt for j in passedAK4Jets ] )

        self.h_ak4ht.Fill( ht, weight )
        if ht < self.htCut :
            return False
        
        passedAK8Jets = [ x for x in ak8jets if ak8MatchedToAK4[x].jetId>0 and x.pt > 400. and abs(x.eta)<2.5  ]
        isTagged = [ self.passTopTag(x) for x in passedAK8Jets ]
        isTaggedDict = dict( zip( passedAK8Jets,isTagged) )
        if len(passedAK8Jets) < 2 :
            return False

        # Make control plots
        for ak8jet in passedAK8Jets:
            self.h_ak8pt.Fill( ak8jet.pt, weight )
            self.h_ak8msd.Fill( ak8jet.msoftdrop, weight )
            self.h_ak8tau32.Fill( ak8jet.tau3 / ak8jet.tau2 if ak8jet.tau2 > 0.0 else 0.0, weight )
            self.h_ak8n3b1.Fill( ak8jet.n3b1, weight )

        # Get a randomly assigned tag and probe jet from the leading two jets
        random.shuffle( passedAK8Jets )
        probejet, tagjet = passedAK8Jets[0:2]
        ttbarP4 = probejet.p4() + tagjet.p4()

        # Check if we have >=1 tag
        if not self.passTopTag(tagjet) :
            if not self.writePredDist:
                return False
            else:
                # Here is the anti-tag region selection to derive the mistag rate. 
                print 'Filling pred dist : ', probejet.p4().P()
                self.preddist.Fill( probejet.p4().P() )

        if not self.writePredDist:
            # Now get the predicted background estimate
            self.predJetP.Accumulate( probejet.p4().P(), probejet.p4().P(), isTaggedDict[probejet], weight )
            self.predJetMTTBAR.Accumulate( ttbarP4.M(), probejet.p4().P(), isTaggedDict[probejet], weight )
        
        # Now fill the double tagged histogram
        if isTaggedDict[probejet] : 
            self.h_mttbar.Fill( ttbarP4.M(), weight )
            return True
        else :
            return False

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ttbarreshad = lambda : TTbarResAnaHadronic() 
