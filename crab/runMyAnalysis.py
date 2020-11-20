from os import listdir, mkdir, popen
from os.path import isfile, join, exists
#from MyNanoAnalysis import *
###
#    HATS comment: 
# Now we want to create an interface for our class in python
# Since we have a lot of data, we will write this so that it loops over a directory
# filled with our input files, and spits out a one output file 
# corresponding to the entire directory.
###
usage = """%prog [options]

This script takes as input a directory of input .root files, and runs the hatsTrees.C macro on them."""

###
#    HATS comment: 
#  Let's not hardcode anything, instead let's run our class's Loop method by
#  passing our python interface some options
#  In case we forget how to use our python interface, we'll write help comments too :-)
###
from optparse import OptionParser
parser = OptionParser(usage)

parser.add_option("-l", "--load", dest = "load",
                  action = "store_true", default = False,
                  help = "do not recompile the class, instead load it from a compiled library" )
parser.add_option("-i", "--inDir", dest = "inDir",
                  help = "the input directory of root files" )
parser.add_option("-t", "--inTreeName", dest = "inTreeName", default = "Events" ,
                  help = "the name of the input tree inside the input file" )
parser.add_option("-o", "--outFileName", dest = "outFileName", default = "test_2017_MC.root",
                  help = "the output root file name. It will be located within the 'output' directory" )
parser.add_option("-n", "--inFileName", dest = "inFileName", default = "testMC.txt",
                  help = "the input txt file name, given instead of inDir . It will be located within the 'InputFiles' directory" )
(options, args) = parser.parse_args()

###
#    HATS comment: 
# Here is a pyROOT gotcha: once you import anything from ROOT, the ROOT command line options 
# will override anything you've defined with your OptionParser. So if you define something
# in your options like -l, that will conflict with the ROOT option to disable the ROOT 
# splash logo. So we only import ROOT once we've already parsed our options.
###

from ROOT import *

###   HATS comment:
# let's combine all the input trees into one TChain 
# Then we can pass that to our ROOT class to crunch
###
print "Loading"
chain = TChain(options.inTreeName)
inFiles = []


with open(options.inFileName) as f:
    inFiles = [line.rstrip() for line in f]




limits = 1
count = 0
for sample in inFiles:
  count +=1
  print "adding %s" % sample
  chain.Add(sample)
  if count >= limits:
      break

print chain
###   HATS comment:
# By default, gSystem.CompileMacro will compile your ROOT class, load it on its own, and then delete it
# once your pyROOT script is closed. Instead, we want to be able to just compile it once, keep the
# compiled library, and then we can reuse it again without recompiling it
# This is important if you're going to run this script e.g. in a cluster submission
# because if two parallel processes try to compile the macro simultaneously,
# one process might try overwriting the library while another is trying to load it.
#
# The options we use are:
# g --> compile with debug symbols. This is nice if you have a bug in your macro
# O --> optimize the code. This does something behind the scenes, so why not
# c --> compile the macro only and don't load it. We do this so that if we only want to load it, we can, but if we want to do both, we won't try twice
# k --> keep the compiled library and don't delete it when the pyroot script ends.
###

#//gSystem.Load("../../include/MyAnalysis.h")

#if not options.load:
#//  gSystem.CompileMacro("/afs/cern.ch/user/a/asparker/public/LFVTopCode_MyFork/crab_nano_data/CMSSW_10_2_18/src/TopLFV/src/MyAnalysis.C", "gOck")
#//    gSystem.CompileMacro("/afs/cern.ch/user/a/asparker/public/LFVTopCode_MyFork/new_nano_mc/TopLFV/src/MyNanoAnalysis.C", "gOck") #gO                                            #    
#    gSystem.CompileMacro("MyNanoAnalysis.C", "gOck") #gO
#    #gROOT.LoadMacro("MyNanoAnalysis.C+");
#    print "gSystem.CompileMacro"


#gInterpreter.ProcessLine('#include "../../include/MyAnalysis.h"')

#gInterpreter.ProcessLine('#include "../../include/PU_reWeighting.h"')
#gInterpreter.ProcessLine('#include "../../include/lepton_candidate.h"')
#gInterpreter.ProcessLine('#include "../../include/jet_candidate.h"')
#gInterpreter.ProcessLine('#include "../../include/RoccoR.h"')
#gInterpreter.ProcessLine('#include "../../include/BTagCalibrationStandalone.h"')


#include "../../include/MyAnalysis.h"
#include "../../include/PU_reWeighting.h"
#include "../../include/lepton_candidate.h"
#include "../../include/jet_candidate.h"
#include "TRandom.h"
#include "TRandom3.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TRandom3.h>
#include <TLorentzVector.h>
#include <time.h>
#include <iostream>
#include <cmath>
#include <vector>
#include "../../include/RoccoR.h"
#include "../../include/BTagCalibrationStandalone.h"

#gSystem.Load("../../src/RoccoR.o")

gInterpreter.ProcessLine('#include "../../include/MyAnalysis.h"') 
gSystem.Load("../../lib/main.so")
#gInterpreter.ProcessLine('#include "../../include/MyAnalysis.h"')
#gInterpreter.ProcessLine('#include "../../src/MyNanoAnalysis.cc"')

instance = MyNanoAnalysis(chain)


### HATS comment:
# and now we call our class's 'Loop' method
###
if not exists("output"):
  mkdir("output")

loopInfo =  [ "2017_testtheMC.root", "mc" , "" , "2017" , "" , 1 , 1 , 1   ]

#loopInfo =  [ "2017_B_DoubleEG_0_0.root", "data" , "DoubleEG" , "2017" , "B" , 1 , 1 , 1   ]                                                                  
instance.Loop( "output/%s" % options.outFileName , loopInfo[1], loopInfo[2], loopInfo[3],loopInfo[4], loopInfo[5],loopInfo[6], loopInfo[7]  )
