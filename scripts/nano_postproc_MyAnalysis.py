#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] outputDir inputFiles")
    parser.add_option("-s", "--postfix", dest="postfix", type="string", default=None,
                      help="Postfix which will be appended to the file name (default: _Friend for friends, _Skim for skims)")
    parser.add_option("-J", "--json", dest="json", type="string",
                      default=None, help="Select events using this JSON file")
    parser.add_option("-c", "--cut", dest="cut", type="string",
                      default=None, help="Cut string")
    parser.add_option("-b", "--branch-selection", dest="branchsel",
                      type="string", default=None, help="Branch selection")
    parser.add_option("--bi", "--branch-selection-input", dest="branchsel_in",
                      type="string", default=None, help="Branch selection input")
    parser.add_option("--bo", "--branch-selection-output", dest="branchsel_out",
                      type="string", default=None, help="Branch selection output")
    parser.add_option("--friend", dest="friend", action="store_true", default=False,
                      help="Produce friend trees in output (current default is to produce full trees)")
    parser.add_option("--full", dest="friend", action="store_false", default=False,
                      help="Produce full trees in output (this is the current default)")
    parser.add_option("--noout", dest="noOut", action="store_true",
                      default=False, help="Do not produce output, just run modules")
    parser.add_option("-P", "--prefetch", dest="prefetch", action="store_true", default=False,
                      help="Prefetch input files locally instead of accessing them via xrootd")
    parser.add_option("--long-term-cache", dest="longTermCache", action="store_true", default=False,
                      help="Keep prefetched files across runs instead of deleting them at the end")
    parser.add_option("-N", "--max-entries", dest="maxEntries", type="long", default=None,
                      help="Maximum number of entries to process from any single given input tree")
    parser.add_option("--first-entry", dest="firstEntry", type="long", default=0,
                      help="First entry to process in the three (to be used together with --max-entries)")
    parser.add_option("--justcount", dest="justcount", default=False,
                      action="store_true", help="Just report the number of selected events")
    parser.add_option("-z", "--compression", dest="compression", type="string",
                      default=("LZMA:9"), help="Compression: none, or (algo):(level) ")
    parser.add_option("-d", "--hdname", dest="hdname", type="string",
                      default='lfv', help="hist dir name")
    (options, args) = parser.parse_args()

    if options.friend:
        if options.cut or options.json:
            raise RuntimeError(
                "Can't apply JSON or cut selection when producing friends")

    if len(args) < 2:
        parser.print_help()
        sys.exit(1)
    outdir = args[0]
    args = args[1:]
    print "infile list"
    print args
    args1 = args[0]
    print "1st infile"
    print args1
  
    fn = ""
    fs = args1.split("/")
    for p in fs :
        if ".root" in p:
            fnt = p
            fnp = fnt.split(".")[0]
            #fn = outdir + '/'+ fnp + '_hists_local.root' 
            fn = "output_lfv_hists.root" 
    print fn
    #outDir/tree_23_Skim.root 
  


    modules = []
    from PhysicsTools.NanoAODTools.postprocessing.modules.lfv.MyAnalysisCC import *
    
    inFiles = []

    #comtxt = ''
    #arglist = args.split(' ')
    
    for a in args:
        inFiles.append(a)   
    #with open(options.inFileName) as f:
    #    inFiles = [line.rstrip() for line in f]
        #for f in inFiles:
        #   comtxt +=f+' '



    modules.append( MyAnalysisCC( False, inFiles , [ fn,  "mc" , "" , "2017" , "" , 1 , 1 , 1   ] )) 
    '''
    for mod, names in options.imports:
        import_module(mod)
        obj = sys.modules[mod]
        selnames = names.split(",")
        mods = dir(obj)
        for name in selnames:
            if name in mods:
                print("Loading %s from %s " % (name, mod))
                if type(getattr(obj, name)) == list:
                    for mod in getattr(obj, name):
                        modules.append(mod( false, testMC.txt , [ string(fn) , "mc" , "" , "2017" , "" , 1 , 1 , 1   ] ))
                else:
                    modules.append(getattr(obj, name)(  false, testMC.txt , [ string(fn) , "mc" , "" , "2017" , "" , 1 , 1 , 1   ]  ))
    '''
    if options.noOut:
        if len(modules) == 0:
            raise RuntimeError(
                "Running with --noout and no modules does nothing!")
    print modules
    print "Ran above modules"
    if options.branchsel != None:
        options.branchsel_in = options.branchsel
        options.branchsel_out = options.branchsel
    p = PostProcessor(outdir, args,
                      cut=options.cut,
                      branchsel=options.branchsel_in,
                      modules=modules,
                      compression=options.compression,
                      friend=options.friend,
                      postfix=options.postfix,
                      jsonInput=options.json,
                      noOut=options.noOut,
                      justcount=options.justcount,
                      prefetch=options.prefetch,
                      longTermCache=options.longTermCache,
                      maxEntries=options.maxEntries,
                      firstEntry=options.firstEntry,
                      outputbranchsel=options.branchsel_out,
                      histFileName= fn , 
                      histDirName= options.hdname)
    p.run()
