import ROOT

f = ROOT.TFile("zplusjetsxs_hists.root")

h_response = f.Get('zjets/h_response')
h_reco = f.Get('zjets/h_reco')
h_gen = f.Get('zjets/h_gen')
h_fake = f.Get('zjets/h_fake')
h_miss = f.Get('zjets/h_miss')

#h_response.GetXaxis().SetRangeUser(0,40)
#h_response.GetYaxis().SetRangeUser(0,40)
#h_reco.GetXaxis().SetRangeUser(0,40)
#h_gen.GetXaxis().SetRangeUser(0,40)

'''         
for ihist in [h_reco,h_gen,h_fake,h_miss]:    
    for i in xrange(ihist.GetNbinsX()+1):        
        wx = ihist.GetXaxis().GetBinWidth(i)                
        ihist.SetBinContent( i, ihist.GetBinContent(i)/wx)
        ihist.SetBinError( i, ihist.GetBinError(i)/wx)
'''
#h_reco.Add( h_fake, -1.0 )
#h_gen.Add( h_miss, -1.0 )

tunfolder = ROOT.TUnfoldDensity(h_response,ROOT.TUnfold.kHistMapOutputVert,ROOT.TUnfold.kRegModeNone, ROOT.TUnfold.kEConstraintNone, ROOT.TUnfoldDensity.kDensityModeBinWidth) 
tunfolder.SetInput( h_reco )

#scanResult = ROOT.TSpline3()
#tunfolder.ScanTau(1000,0.00001,0.00005,scanResult,ROOT.TUnfoldDensity.kEScanTauRhoAvg)


tunfolder.DoUnfold(0.0)
h_unfolded = tunfolder.GetOutput("unfolded")

h_reco.SetLineColor(ROOT.kBlack)
h_gen.SetLineColor(ROOT.kRed)
h_unfolded.SetMarkerStyle(20)
h_unfolded.SetMarkerColor(ROOT.kRed)

c1 = ROOT.TCanvas("c1", "c1")
hs = ROOT.THStack("hs", "hs")
hs.Add( h_gen, "hist" )
hs.Add( h_reco, "hist" )
hs.Add( h_unfolded, "e" )
hs.Draw("nostack")

c2 = ROOT.TCanvas("c2", "c2")
h_response.Draw("colz")
