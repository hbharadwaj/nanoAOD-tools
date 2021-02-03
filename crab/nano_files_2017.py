import sys
import os
import subprocess
import readline
import string

data2017_samples = {}
mc2017_samples = {}
#data2017_samples ['DYM10to50'] = ['address', 'data/mc','dataset','year', 'run', 'cross section','lumi','Neventsraw']                        

mc2017_samples['2017_DYM10to50'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv6-1-1_2017/200613_065556/0000/'], 'mc','','2017', '','18610','41.53','39521230'] ## '78,994,955' ## <-  is event number from miniaod, we must be missing an extension

mc2017_samples['2017_DYM50'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/TopNanoAODv6-1-1_2017/200613_070408/0000/'], 'mc','','2017', '','5765.4','41.53','182217609'] ## '84,597,528' ## now we have ore events ?  182,217,609

## example nanoAOD datset on DAS where I got number of events from
## https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fphys03&input=dataset+%3D+%2FTTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8%2Fpalencia-TopNanoAODv6-1-1_2018-0d1d4920f08f56d048ece029b873a2cc%2FUSER
mc2017_samples['2017_TTTo2L2Nu'] = [['/store/group/phys_top/topNanoAOD/v6-1-1/2018/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2018/200610_155014/0000/'], 'mc','','2017', '','87.31','41.53', '64310000' ] ##'8926992'] what is going on with number of events?

mc2017_samples['2017_ST_tW'] = [['/store/group/phys_top/topNanoAOD/v6-1-1/2017/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2017/200610_154434/0000/'], 'mc','','2017', '','19.47','41.53','11271078']


mc2017_samples['2017_ST_atW'] = [[ '/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/schoef-TopNanoAODv6-1-1_2016-88146d75cb10601530484643de5f7795/USER', '/store/group/phys_top/topNanoAOD/v6-1-1/2017/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2017/200610_154530/0000/'], 'mc','','2017', '','19.47','41.53','11271078']

mc2017_samples['2017_WWTo2L2Nu'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/WWTo2L2Nu_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2017/200615_072350/0000/'], 'mc','','2017', '','12.178','41.53','2000000']

mc2017_samples['2017_ZZTo2L2Nu'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/ZZTo2L2Nu_13TeV_powheg_pythia8/TopNanoAODv6-1-1_2017/200709_070028/0000/'], 'mc','','2017', '','0.564','41.53','8744768']

mc2017_samples['2017_ZZTo4L'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/ZZTo4L_13TeV_powheg_pythia8/TopNanoAODv6-1-1_2017/200615_073451/0000/'], 'mc','','2017', '','1.212','41.53','616075000']




mc2017_samples['2017_WZTo2L2Q'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/TopNanoAODv6-1-1_2017/200615_072720/0000/'], 'mc','','2017', '','5.595','41.53','27582164']

mc2017_samples['2017_WZTo3LNu'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/WZTo3LNu_13TeV-powheg-pythia8/TopNanoAODv6-1-1_2017/200615_072748/0000/'], 'mc','','2017', '','4.43','41.53','976400']

mc2017_samples['2017_WJetsToLNu'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TopNanoAODv6-1-1_2017/200615_072257/0000/'], 'mc','','2017', '','61526.7','41.53','74635450']

mc2017_samples['2017_TTWJetsToQQ'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/TopNanoAODv6-1-1_2017/200629_065523/0000/'], 'mc','','2017', '','0.4062','41.53','811306']

mc2017_samples['2017_TTWJetsToLNu'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/TopNanoAODv6-1-1_2017/200705_105512/0000/'], 'mc','','2017', '','0.2043','41.53','4925829']

mc2017_samples['2017_TTZToLLNuNu'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/TopNanoAODv6-1-1_2017/200615_071611/0000/'], 'mc','','2017', '','0.2529','41.53','7932650']

mc2017_samples['2017_TTZToQQ'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/TopNanoAODv6-1-1_2017/200615_071706/0000/'], 'mc','','2017', '','0.5297','41.53','750000']



data2017_samples['2017_B_MuonEG'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/MuonEG/TopNanoAODv6-1-1_2017/200615_081001/0000/'], 'data','MuonEG','2017', 'B','1','1','1']
data2017_samples['2017_C_MuonEG'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/MuonEG/TopNanoAODv6-1-1_2017/200630_170320/0000/','/pnfs/iihe/cms/store/user/xgao/samples-20191203/data/2017/MuonEG/crab_MuonEG_runC/191204_020526/0001/'], 'data','MuonEG','2017', 'C','1','1','1']


data2017_samples['2017_D_MuonEG'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/MuonEG/TopNanoAODv6-1-1_2017/200615_081058/0000/'], 'data','MuonEG','2017', 'D','1','1','1']
data2017_samples['2017_E_MuonEG'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/MuonEG/TopNanoAODv6-1-1_2017/200615_081126/0000/'], 'data','MuonEG','2017', 'E','1','1','1']
data2017_samples['2017_F_MuonEG'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/MuonEG/TopNanoAODv6-1-1_2017/200619_103726/0000/'], 'data','MuonEG','2017', 'F','1','1','1']




data2017_samples['2017_B_SingleMuon'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleMuon/TopNanoAODv6-1-1_2017/200706_172229/0000/'], 'data','SingleMuon','2017', 'B','1','1','1']
data2017_samples['2017_C_SingleMuon'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleMuon/TopNanoAODv6-1-1_2017/200617_193103/0000/'], 'data','SingleMuon','2017', 'C','1','1','1']
###past here conversion is NOT complete
data2017_samples['2017_D_SingleMuon'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleMuon/TopNanoAODv6-1-1_2017/200612_180908/0000/'], 'data','SingleMuon','2017', 'D','1','1','1']
data2017_samples['2017_E_SingleMuon'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleMuon/TopNanoAODv6-1-1_2017/200612_180934/0000/'], 'data','SingleMuon','2017', 'E','1','1','1']
data2017_samples['2017_F_SingleMuon'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleMuon/TopNanoAODv6-1-1_2017/200612_181001/0000/'], 'data','SingleMuon','2017', 'F','1','1','1']

data2017_samples['2017_B_SingleElectron'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleElectron/TopNanoAODv6-1-1_2017/200615_081218/0000/'], 'data','SingleElectron','2017', 'B','1','1','1']
data2017_samples['2017_C_SingleElectron'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleElectron/TopNanoAODv6-1-1_2017/200615_081246/0000/'], 'data','SingleElectron','2017', 'C','1','1','1']
data2017_samples['2017_D_SingleElectron'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleElectron/TopNanoAODv6-1-1_2017/200615_081311/0000/'], 'data','SingleElectron','2017', 'D','1','1','1']
data2017_samples['2017_E_SingleElectron'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleElectron/TopNanoAODv6-1-1_2017/200615_081338/0000/'], 'data','SingleElectron','2017', 'E','1','1','1']
data2017_samples['2017_F_SingleElectron'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/SingleElectron/TopNanoAODv6-1-1_2017/200615_081411/0000/'], 'data','SingleElectron','2017', 'F','1','1','1']

data2017_samples['2017_B_DoubleEG'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleEG/TopNanoAODv6-1-1_2017/200615_080330/0000/'], 'data','DoubleEG','2017', 'B','1','1','1']
data2017_samples['2017_C_DoubleEG'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleEG/TopNanoAODv6-1-1_2017/200615_080356/0000/'], 'data','DoubleEG','2017', 'C','1','1','1']
data2017_samples['2017_D_DoubleEG'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleEG/TopNanoAODv6-1-1_2017/200615_080422/0000/'], 'data','DoubleEG','2017', 'D','1','1','1']
data2017_samples['2017_E_DoubleEG'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleEG/TopNanoAODv6-1-1_2017/200615_080448/0000/'], 'data','DoubleEG','2017', 'E','1','1','1']
data2017_samples['2017_F_DoubleEG'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleEG/TopNanoAODv6-1-1_2017/200615_080514/0000/'], 'data','DoubleEG','2017', 'F','1','1','1']

data2017_samples['2017_B_DoubleMu'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleMuon/TopNanoAODv6-1-1_2017/200615_080544/0000/'], 'data','DoubleMu','2017', 'B','1','1','1']
data2017_samples['2017_C_DoubleMu'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleMuon/TopNanoAODv6-1-1_2017/200615_080609/0000/'], 'data','DoubleMu','2017', 'C','1','1','1']
data2017_samples['2017_D_DoubleMu'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleMuon/TopNanoAODv6-1-1_2017/200615_080634/0000/'], 'data','DoubleMu','2017', 'D','1','1','1']
data2017_samples['2017_E_DoubleMu'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleMuon/TopNanoAODv6-1-1_2017/200615_080700/0000/'], 'data','DoubleMu','2017', 'E','1','1','1']
data2017_samples['2017_F_DoubleMu'] = [['/store/user/piedavid/topNanoAOD/v6-1-1/2017/DoubleMuon/TopNanoAODv6-1-1_2017/200615_080726/0000/'], 'data','DoubleMu','2017', 'F','1','1','1']


#/pnfs/iihe/cms/store/user/rgoldouz/TopLfvFullSim/2017/IIHE_Ntuple/ntuple_SMEFTfr_ST_clequ3_emutu

mc2017_samples['2017_LFVStVecC'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_155453/0000/'], 'mc','','2017', '','0.0512' ,'41.53','500000']
mc2017_samples['2017_LFVStVecU'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_155716/0000/'], 'mc','','2017', '','0.515' ,'41.53','494000']
mc2017_samples['2017_LFVTtVecC'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201008_025340/0000/'], 'mc','','2017', '','0.032'  ,'41.53','500000']
mc2017_samples['2017_LFVTtVecU'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201008_025758/0000/'], 'mc','','2017', '','0.032','41.53','498000']

#tensor interaction                                                                                                                                                                                                
mc2017_samples['2017_LFVStClequ3U'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_150303/0000/'], 'mc','','2017', '','1.9' ,'41.53','500000']
mc2017_samples['2017_LFVStClequ3C'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_150454/0000/'], 'mc','','2017', '','0.187' ,'41.53','500000']
mc2017_samples['2017_LFVTtClequ3U'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_152919/0000/'], 'mc','','2017', '','0.1876','41.53','500000']
mc2017_samples['2017_LFVTtClequ3C'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_153218/0000/'], 'mc','','2017', '','0.1876','41.53','500000']

#scalar interaction                                                                                                                                                                                                
mc2017_samples['2017_LFVStClequ1C'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_133418/0000/'], 'mc','','2017', '','0.008' ,'41.53','500000']
mc2017_samples['2017_LFVStClequ1U'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_145731/0000/'], 'mc','','2017', '','0.102' ,'41.53','500000']
mc2017_samples['2017_LFVTtClequ1C'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201007_153437/0000/'], 'mc','','2017', '','0.004'  ,'41.53','500000']
mc2017_samples['2017_LFVTtClequ1U'] = [['/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/201008_024659/0000/'], 'mc','','2017', '','0.004','41.53','500000']



#/eos/cms/store/user/asparker/TopLFV_nanoAOD/v6-1-1/2017/CRAB_UserFiles/TopNanoAODv6-1-1_2017/
#201007_133418  201007_145731  201007_150303  201007_150454  201007_152919  201007_153218  201007_153437  201007_155453  201007_155716  201008_024659  201008_025340  201008_025758
