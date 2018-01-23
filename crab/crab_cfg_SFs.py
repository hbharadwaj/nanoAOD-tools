from WMCore.Configuration import Configuration

from CRABAPI.RawCommand import crabCommand 

config = Configuration()

config.section_("General")

config.General.transferLogs= True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/uscms/home/aparker/nobackup/nanoAod/myfork/CMSSW_9_4_1/src/PhysicsTools/NanoAODTools/crab/PSet.py'
config.JobType.scriptExe = '/uscms/home/aparker/nobackup/nanoAod/myfork/CMSSW_9_4_1/src/PhysicsTools/NanoAODTools/crab/crab_script_SFs.sh'
config.JobType.inputFiles = ['/uscms/home/aparker/nobackup/nanoAod/myfork/CMSSW_9_4_1/src/PhysicsTools/NanoAODTools/crab/crab_script_SFs.py','/uscms/home/aparker/nobackup/nanoAod/myfork/CMSSW_9_4_1/src/PhysicsTools/NanoAODTools/scripts/*'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
# following 3 lines are the trick to skip DBS data lookup in CRAB Server
#config.Data.userInputFiles = lfnList
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

config.Data.publication = True

config.section_("Site")


# since there is no data discovery and no data location lookup in CRAB
# you have to say where the input files are
#config.Site.whitelist = ['T2_IT_Bari']


#this fake PSET is needed for local test and for crab to figure the output filename                                                                                                                                                                           
#you do not need to edit it unless you want to do a local test using a different input file than                                                                                                                                                              
#the one marked below                                                                                                                                                                                                                                        

#result = crabCommand('submit', config = config)

#print (result)
