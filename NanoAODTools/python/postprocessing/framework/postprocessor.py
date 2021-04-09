#!/usr/bin/env python
import os
import time
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.branchselection import BranchSelection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import *
from PhysicsTools.NanoAODTools.postprocessing.framework.output import FriendOutput, FullOutput
from PhysicsTools.NanoAODTools.postprocessing.framework.preskimming import preSkim
from PhysicsTools.NanoAODTools.postprocessing.framework.jobreport import JobReport
from PhysicsTools.NanoAODTools.postprocessing.modules.lfv.MyAnalysisCC import *
class PostProcessor :
    def __init__(self,outputDir,inputFiles,cut=None,branchsel=None,modules=[],compression="LZMA:9",friend=False,postfix=None,
         jsonInput=None,noOut=False,justcount=False,provenance=False,haddFileName=None,fwkJobReport=False,histFileName=None,histDirName=None, outputbranchsel=None):
        self.outputDir=outputDir
        self.inputFiles=inputFiles
        self.cut=cut
        self.modules=modules
        self.compression=compression
        self.postfix=postfix
        self.json=jsonInput
        self.noOut=noOut
        self.friend=friend
        self.justcount=justcount
        self.provenance=provenance
        self.jobReport = JobReport() if fwkJobReport else None
        self.haddFileName=haddFileName
        self.histFile = None
        self.histDirName = None
        if self.jobReport and not self.haddFileName :
            print "Because you requested a FJR we assume you want the final hadd. No name specified for the output file, will use tree.root"
            self.haddFileName="tree.root"
        self.branchsel = BranchSelection(branchsel) if branchsel else None
        self.outputbranchsel = BranchSelection(outputbranchsel) if outputbranchsel else None
        self.histFileName=histFileName
        self.histDirName=histDirName
    def run(self) :
        outpostfix = self.postfix if self.postfix != None else ("_Friend" if self.friend else "_Skim")
        if not self.noOut:
            
            if self.compression != "none":
                ROOT.gInterpreter.ProcessLine("#include <Compression.h>")
                (algo, level) = self.compression.split(":")
                compressionLevel = int(level)
                if   algo == "LZMA": compressionAlgo  = ROOT.ROOT.kLZMA
                elif algo == "ZLIB": compressionAlgo  = ROOT.ROOT.kZLIB
                else: raise RuntimeError("Unsupported compression %s" % algo)
            else:
                compressionLevel = 0
            print "Will write selected trees to "+self.outputDir
            if not self.justcount:
                if not os.path.exists(self.outputDir):
                    os.system("mkdir -p "+self.outputDir)
        else:
            compressionLevel = 0

        if self.noOut:
            if len(self.modules) == 0:
                raise RuntimeError("Running with --noout and no modules does nothing!")

            # Open histogram file, if desired
            if (self.histFileName != None and self.histDirName == None) or (self.histFileName == None and self.histDirName != None) :
                raise RuntimeError("Must specify both histogram file and histogram directory!")
            elif self.histFileName != None and self.histDirName != None:
                self.histFile = ROOT.TFile.Open( self.histFileName, "RECREATE" )
            else :
                self.histFile = None

        
        for m in self.modules:
            if hasattr( m, 'writeHistFile') and m.writeHistFile :
                m.beginJob(histFile=self.histFile,histDirName=self.histDirName)
            else :
                m.beginJob()


        fullClone = (len(self.modules) == 0)
        outFileNames=[]
        t0 = time.clock()
        totEntriesRead=0
        fnum = 0


        ## hadd all input files so we can loop just once

#        cmd = './haddnano.py ' + 'haddedtree.root ' + '   '
        
        inTree = ROOT.TChain('Events')
        for fname in self.inputFiles:
            inTree.Add( fname )
            inFile = ROOT.TFile.Open(fname)
#            cmd += (fname + ' ')

#        print cmd
#        os.system(cmd)

#        inFile = ROOT.TFile.Open('haddedtree.root')
#        inFile = inTree.GetCurrentFile()
            
#        inTree = inFile.Get("Events")

        print "inTree"
        print inTree


        totEntriesRead+=inTree.GetEntries()
        # pre-skimming
        elist,jsonFilter = preSkim(inTree, self.json, self.cut)
        #if self.justcount:
        #    print 'Would select %d entries from %s'%(elist.GetN() if elist else inTree.GetEntries(), fname)
        #    #continue
        #else:
        print 'Pre-select %d entries out of %s '%(elist.GetN() if elist else inTree.GetEntries(),inTree.GetEntries())
        
        if fullClone:
            # no need of a reader (no event loop), but set up the elist if available
            if elist: inTree.SetEntryList(elist)
        else:
            # initialize reader
            inTree = InputTree(inTree, elist)


#        if not self.noOut:
#
#            #outFileNames.append(outFileName)
#            if compressionLevel:
#                outFileName = os.path.join(self.outputDir, os.path.basename(fname).replace(".root",outpostfix+".root"))
#                outFile = ROOT.TFile.Open(outFileName, "RECREATE", "", compressionLevel)
#                outFileNames.append(outFileName)
#                outFile.SetCompressionAlgorithm(compressionAlgo)
#            # prepare output tree
#            if self.friend:
#                outTree = FriendOutput(inFile, inTree, outFile)
#            else:
#                outTree = FullOutput(inFile, inTree, outFile, branchSelection = self.branchsel, fullClone = fullClone, jsonFilter = jsonFilter,provenance=self.provenance)
#        else :
#            outFile = None
#            outTree = None

        
        ### Run central modules like jetmetHelperRun2 before MyAnalysisCC module
        print "Run These modules with python loops :"
        print self.modules[:-1]
        #(nall, npass, timeLoop) = eventLoop(self.modules[:-1], inFile, outFile, inTree, outTree)
        #elist,jsonFilter = preSkim(inTree, self.json, self.cut)# the "eventLoop" function cancels the entrylist, need to preskim again.

        print "Run This module with C ++ loops :"
        print [self.modules[-1]]
        ## by default in nanoAOD-tools the loop is in python,
        ## the module below has the loop run in C++
        ## only run this on last module in the list [self.modules[-1] which is our modules/lfv/MyAnalysisCC module
        inTree.SetEntryList(elist)
        nothing = treeLoop([self.modules[-1]], inFile, inTree, elist) #, outTree)

        



        # prepare output file

            
        # process events, if needed

        
        # we need to run this event loop on the jetmethelper2 module
       
        print "run treeLoop in postprocessor"
        #only run the tree loop (C++ loop instead of python) on last in list, which should be MyAnalysisCC

#        if not self.noOut:
#            outTree.write()
#            outFile.Close()
#            print "Done %s" % outFileName

        for m in self.modules: m.endJob()
        
        print  totEntriesRead/(time.clock()-t0), "Hz"


#        if self.haddFileName :
#                os.system("./haddnano.py %s %s" %(self.haddFileName," ".join(outFileNames))) #FIXME: remove "./" once haddnano.py is distributed with cms releases
        if self.jobReport :
                #self.jobReport.addOutputFile(self.haddFileName) # outFileNames[0]
                self.jobReport.save()
