import ROOT

f = ROOT.TFile("zplusjetsxs_hists.root")

h_response = f.Get('zjets/h_response')
h_reco = f.Get('zjets/h_reco')
h_gen = f.Get('zjets/h_gen')
h_fake = f.Get('zjets/h_fake')
h_miss = f.Get('zjets/h_miss')

h_reco.Add( h_fake, -1.0 )
#h_gen.Add( h_miss, -1.0 )

tunfolder = ROOT.TUnfoldDensity(h_response,ROOT.TUnfold.kHistMapOutputHoriz,ROOT.TUnfold.kRegModeNone, ROOT.TUnfold.kEConstraintNone, ROOT.TUnfoldDensity.kDensityModeBinWidth) 
tunfolder.SetInput( h_reco )
tunfolder.DoUnfold(0.0)
h_unfolded = tunfolder.GetOutput("unfolded")


h_gen.SetLineColor(ROOT.kBlue)
h_unfolded.SetLineColor(ROOT.kRed)

c1 = ROOT.TCanvas("c1", "c1")
h_gen.Draw()
h_reco.Draw('same')
h_unfolded.Draw('same')

c2 = ROOT.TCanvas("c2", "c2")
h_response.Draw("colz")
