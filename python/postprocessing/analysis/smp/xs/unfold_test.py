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

## for i in xrange(h_response.GetNbinsX()+1):
##     sumj = 0.
##     x = 0
##     wx = h_response.GetXaxis().GetBinWidth(i)
##     for j in xrange(h_response.GetNbinsY()+1):
##         sumj += h_response.GetBinContent(i,j)
##     if sumj > 0.0:
##         for j in xrange(h_response.GetNbinsY()+1):
##             wy = h_response.GetYaxis().GetBinWidth(j)
##             h_response.SetBinContent( i, j, h_response.GetBinContent(i,j) / sumj )
##             h_response.SetBinError( i, j,  h_response.GetBinError(i,j) / sumj )
            
## for ihist in [h_reco,h_gen,h_fake,h_miss]:    
##     for i in xrange(ihist.GetNbinsX()+1):        
##         wx = ihist.GetXaxis().GetBinWidth(i)        
##         for j in xrange(ihist.GetNbinsY()+1):
##             wy = ihist.GetYaxis().GetBinWidth(j)
##             ihist.SetBinContent( i,j, ihist.GetBinContent(i,j)/wx/wy)
##             ihist.SetBinError( i,j, ihist.GetBinError(i,j)/wx/wy)

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
