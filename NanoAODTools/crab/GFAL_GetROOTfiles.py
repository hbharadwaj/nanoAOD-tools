#!/usr/bin/env python
###
### Scrambled from https://github.com/xrootd/xrootd-python/tree/master/examples
###

#from XRootD import client
#from XRootD.client.flags import DirListFlags
import os

def GFAL_GetROOTfiles( path, gfalstr = "root://cms-xrd-global.cern.ch/" ):

    v = True
    if v : print "Using GFAL_GetROOTfiles to get list or .root files located here: {}".format( path )  

    testlstxt = "gfal-ls " + gfalstr + path
    print path
    print "path..."
    if 'CRAB' in path:
        testlstxt = "ls /eos/cms" + path
    os.system( testlstxt )
    print testlstxt
    print "testlstxt"
    rootfiles = []
    xrdstr  = "root://cms-xrd-global.cern.ch/"
    for fn in filter(None,os.popen( testlstxt  ).read().split('\n')):
        #    #print "FILE X : {}".format(fn)            
        if '.root' in fn :                   
            rootfiles.append( xrdstr +  path + fn )
        #if v :  print "Adding to txt file :  {}".format( xrdstr + path + fn  )

    if len(rootfiles) < 2 :
        print "Try using ls "
        
        lsnew1 = "ls " +'/eos/cms'+  path


        for fn in filter(None,os.popen( lsnew1  ).read().split('\n')):
            rootfiles.append( xrdstr + '/eos/cms' + path + fn )

    if len(rootfiles) < 2 :
        print "Try using gfal-ls "
        cmd2 = 'env -i X509_USER_PROXY=/tmp/x509up_u$UID gfal-ls  srm://ingrid-se02.cism.ucl.ac.be:8444/srm/managerv2?SFN=/storage/data/cms'+ path

        for fn in filter(None,os.popen( cmd2  ).read().split('\n')):
            if '.root' in fn :
                rootfiles.append( xrdstr +  path + fn )


    return rootfiles
#['', 'eos', 'cms', 'store', 'user', 'asparker', 'TopLFV_nanoAOD', 'v6-1-1', '2017', 'CRAB_UserFiles', 'TopNanoAODv6-1-1_2017', '201008_025758', '0000', '']
