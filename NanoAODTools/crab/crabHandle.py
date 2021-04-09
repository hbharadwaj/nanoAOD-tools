#!/usr/bin/env python

#If started with bash instead of python, source crab first
''':'
if [ -z "$CMSSW_BASE" ]; then echo "Must setup CMSSW environment first!"; exit 1; fi
. /cvmfs/cms.cern.ch/crab3/crab.sh
exec python $0 "$@"
'''

import sys
import os
import socket
import traceback
import subprocess

from versioning import versionLoad as load
from versioning import upConvert
from versioning import dump
import pickle

try:
    from CRABAPI.RawCommand import crabCommand as cc
    import CRABClient.UserUtilities
    import CRABClient.ClientUtilities
    CRABClient.UserUtilities.setConsoleLogLevel(CRABClient.ClientUtilities.LOGLEVEL_MUTE)
    from CRABClient.ClientExceptions import CachefileNotFoundException
except ImportError:
    #Run again, this time internally setting up crab environment first
    os.execlp('bash','bash',*sys.argv)

def inc(x):
    x+=1
    return x

try:
    sys.argv.pop(sys.argv.index('noFetch'))
    fetch=False
except ValueError:
    fetch=True


try:
    pwd=sys.argv[1]
    os.chdir(pwd)
except IndexError:
    pwd=os.getcwd()

try:
    with open('crabHandleStatus.pkl','rb') as f:
        try:
            pklv1=load(f,1)
        except KeyError: #Corrupted pickle file
            print "Corrupted pickle file. Removing."
            os.remove('crabHandleStatus.pkl')
            print "Restarting python script."
            os.execlp('/usr/bin/env','python',os.path.realpath(__file__),*sys.argv[1:])
        pkl=pklv1['status']
    dirs=pkl.keys()
except IOError:
    try:
        sys.argv[2]
        dirs=sys.argv[2:]
    except IndexError:
        dirs=[direct for direct in os.listdir(pwd) if (os.path.isdir(direct))]
    pkl={ d:0 for d in dirs }
    pklv1=upConvert(pkl,0,1)
    for directory in dirs:
        pklv1['downloaded'][directory]=[x.rsplit('.root',1)[0].split('_')[-1] for x in os.listdir('%s/%s/results'%(pwd,directory))]

if not sys.stdin.isatty():
    for line in sys.stdin:
        print line,

try:
    #index=[i for i,s in enumerate(sys.argv) if 'quiet=' in index][0]
    #logfile=sys.argv.pop(index).split('=')[1]
    sys.argv.pop(sys.argv.index('quiet'))
    sys.stdout=open('./quiet_log_file.txt','wa+')
except ValueError:
    pass


try:
    sys.argv.pop(sys.argv.index('ignoreKill'))
    kill=False
except ValueError:
    kill=True

if os.path.isfile('.kill') and kill: #Nice way to kill cron job independent of node it's running on
    sys.stdout=sys.__stderr__
    try:
        with open('.kill') as f:
            contents=f.read()
            if 'CRAB' in contents:
                dirs=[direct for direct in os.listdir(pwd) if (os.path.isdir(direct))]
                for directory in dirs:
                    print 'Killing %s' % directory
                    print cc('kill',dir=directory)
    finally:
        print 'Killing cron job!'
        sys.exit(0)


from collections import defaultdict

def ordinal():
    numberDict=defaultdict(lambda:'th',{1:'st',2:'nd',3:'rd'})
    def _tmp(number):
        if number < 20:
           if number > 10:
                return str(number)+'th'
        return str(number)+numberDict[number % 10]
    return _tmp

ordinal=ordinal()
try:
    pklv1['lastStatus'].append({})
except KeyError:
    pklv1['lastStatus']=[{}]

try: #Ensure only one process is running at a time per directory
    with os.fdopen(os.open('.lock',os.O_CREAT|os.O_EXCL|os.O_WRONLY),'w') as f: f.write(socket.gethostname())
except OSError:
    sys.stdout=sys.__stderr__
    with open('.lock') as f:
        print 'Process already running on this directory on host %s.' % f.read()
    print 'If this process is not running, delete the .lock file and try again.'
    sys.exit(1)
try:
    quotaFail=False
    tmp=[]
    for directory in dirs:
        try:
            int(pkl[directory])
            tmp.append(directory)
        except ValueError:
            pass
    dirs=tmp
    for number,directory in enumerate(dirs):
        try:
            print '(Job %d/%d): Running crab status on directory %s' % (number+1,len(dirs),directory)
            results=cc('status',dir=directory)
            statuses=results['jobsPerStatus']
            pklv1['lastStatus'][-1][directory]=results
            if results['status']=='SUBMITFAILED':
                pkl[directory]='SUBMITFAILED'
                with open('.submitfailures','a') as f:
                    f.write('%s\n' % '_'.join(directory.split('_')[2:]))  
                continue
            print statuses
            if statuses=={}: #Still in the submission stage?
                continue
            if 'failed' in statuses or 'killed' in statuses: #Want to resubmit if failed:
                if 'finished' in statuses or 'transferring' in statuses or pkl[directory]<4: #But only if some of them have NOT failed
                    pkl[directory]+=1
                    print 'Resubmitting for the %s time...' % ordinal(pkl[directory])
                    cc('resubmit',dir=directory)
                elif results['status']=='FAILED': #Give up!
                    print 'Giving up!'
                    pkl[directory]='FAILED'
            finishedJobs=[x for x in results['jobs'] if results['jobs'][x]['State'] == 'finished' and x not in pklv1['downloaded'][directory]]
            try:
                finishedJobs.sort(key=lambda x:int(x))
            except ValueError:
                pass
            if finishedJobs:
                if fetch:
                    print "Fetching output for %d jobs..." % len(finishedJobs)
                while(finishedJobs):
                    if fetch:
                        go=cc('getoutput',dir=directory,jobids=','.join(finishedJobs[0:500]))
                        finishedJobs=finishedJobs[500:]
                        failed=go['failed']
                        success=go['success']
                        if failed:
                            failedJobs={(x.rsplit('.root',1)[0].split('_')[-1],failed[x]) for x in failed}
                            print '%d output requests failed.' % len(failedJobs)
                            failureReasons=set([failed[x] for x in failed])
                            print failureReasons
                            for y in failureReasons:
                                if 'quota' in y:
                                    #p=subprocess.Popen(['/bin/mail','EMAILHERE'],stdin=subprocess.PIPE)
                                    #p.communicate(input='Quota exhausted on cmslpc.')
                                    quotaFail=True
                                    with open('.kill','a') as f: f.write('Auto-killed: over quota')
                                    sys.exit(0)
                        if success:
                            successfulJobs=[x.rsplit('.root',1)[0].split('_')[-1] for x in success]
                            print '%d outputs successfully retrieved.' % len(successfulJobs)
                            pklv1['downloaded'][directory].extend(successfulJobs)   
                            pklv1['downloaded'][directory]=sorted(list(set(pklv1['downloaded'][directory])))
                    else:
                        pklv1['downloaded'][directory].extend(finishedJobs)
                        pklv1['downloaded'][directory]=sorted(list(set(pklv1['downloaded'][directory])))
                        break
            if len(pklv1['downloaded'][directory])>=len(results['jobs']):
                pkl[directory]='FINISHED'
        except CachefileNotFoundException:
            print '.requestcache file not found in directory %s.' % directory
            if pkl[directory] > 1:
                print 'Giving up!'
                pkl[directory]='NOCACHEFILE'
            else:
                print 'Will try once more.'
                pkl[directory]+=1
        except Exception:
            traceback.print_exc()
            if quotaFail: raise
            pass
finally:
    with open('crabHandleStatus.pkl','wb') as f:
        dump(pklv1,f)
    os.remove('.lock')
    jobsLeft=0
    for repeats in pkl.itervalues():
        try:
            int(repeats)
            jobsLeft+=1
        except ValueError:
            pass
    if jobsLeft > 0:
        print '%d jobs remaining!' % jobsLeft
        sys.exit(1)
    someJobsFailed=False
    try:
        sys.stdout=sys.__stdout__ #Stop being quiet
    except:
        pass #But if you can't for some reason, keep going
    if 'FAILED' in [pkl[directory] for directory in pkl]:
        someJobsFailed=True
        print 'Some jobs failed!'
    else:
        print 'All jobs finished!'
    try:
        with open('.done','wb') as f:f.write('Finished!')
        with open('.kill','wba') as f:f.write('Finished!')
    except:
        traceback.print_exc()
    finally:
        if os.path.isfile('.postJob'):
            os.execlp('bash','bash','.postJob')
        sys.exit(0)
