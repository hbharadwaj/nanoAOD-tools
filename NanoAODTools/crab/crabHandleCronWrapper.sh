#!/bin/bash

#Takes care of necessary environment setup and such for cron to monitor crab tasks
#To setup: first argument should be SETUP, followed by CMSSW directory (wherever cmsenv should be run)
#Rest should just be directory of crab directories


OUTPUT="`mktemp -t`"
set -e
exec 3>&1
[ -t 1 ] || exec > "$OUTPUT" # don't redirect if writing to a terminal

(
set -e
if [ "$1" == "SETUP" ]; then
    shift
#    pushd "$2"
#    if [ $# -le 3 ]; then
#        for dir in crab_*;
#        do
#            touch ${dir}_ND
#        done   
#    fi
#    popd
    if [[ "$@" =~ "%" ]]; then
        echo "No % signs allowed. crontab will lose its mind over those."
        exit 1
    fi
    if [ -d "$1" ]; then
        THIS_DATE=$(date +%M)
        THIS_SHA_HASH="$(echo $(date +%s%N) "$@" | sha256sum | awk '{print$1}')"
        cat <(crontab -l 2>/dev/null) <(echo "$THIS_DATE" '*' '*' '*' '*' 'bash' "`readlink -f "$BASH_SOURCE"`" `printf '%q ' "$THIS_SHA_HASH" "$@"`) | crontab -
    else 
        exit 1
    fi
    hostname > ~/".cronJobs/$THIS_SHA_HASH"
    echo $(date +%M) '*' '*' '*' '*' 'bash' "`readlink -f "$BASH_SOURCE"`" `printf '%q ' "$THIS_SHA_HASH" "$@"` >> ~/".cronJobs/$THIS_SHA_HASH"
    #Run it once immediately
    exec bash "`readlink -f "$BASH_SOURCE"`" `printf '%q ' "$THIS_SHA_HASH" "$@"` || { crontab -l | grep -Fv "$THIS_SHA_SUM" | crontab - ; }
    exit 0
fi

removeCrontab() {
    echo "Jobs done!"
    crontab -l | grep -Fv "$SHA_SUM" | crontab -
    rm ~/".cronJobs/$SHA_SUM"
}

SHA_SUM="$1"
shift
CMSSW_DIR="$1"
shift
. /cvmfs/cms.cern.ch/cmsset_default.sh
pushd "$CMSSW_DIR"
eval `scramv1 runtime -sh`
echo 'Checking for proxy...'
voms-proxy-info -exists
. /cvmfs/cms.cern.ch/crab3/crab.sh
popd
cd ~/bin
echo "Running crabHandle `printf '%q ' "$@"`on `hostname` at `date`"
exec >&3
stdbuf -o 0 cat "$OUTPUT" | (python crabHandle.py "$@" && removeCrontab "$@") 2>&1 | grep -v '^Retrieving' | grep -v '^Success:'
rm "$OUTPUT"
) || { echo "Job failed. Bash output is as follows:" ; exec >&3 ; cat "$OUTPUT" ; }
#[ -f ~/".cronJobs/$SHA_SUM" ] || { 
