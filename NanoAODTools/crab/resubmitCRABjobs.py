import argparse , os

# set up an argument parser                                                                                                                 \
                                                                                                                                             
parser = argparse.ArgumentParser()

parser.add_argument('--loc', dest = 'LOC', default= './CRABtasks')
parser.add_argument('--name', dest='NAME', default=None)# used to name txt file and eos directory                                            
parser.add_argument('--v', dest='VERBOSE', default=True)


ARGS = parser.parse_args()



# cd to location given                                                                                                                       


#os.system( "cd " + ARGS.LOC )                                                                                                               

lstxt = "ls -d -- "  + ARGS.LOC + "/*/"

# Find all subdirectories and write CRAB resubmit commands for them                                                                          

#commandList = []                                                                                                                            
for fn in filter(None,os.popen( lstxt  ).read().split('\n')):

    #commandList.append( "crab resubmit "+ fn )                                                                                              
    os.system( "crab resubmit " +fn  )
    if ARGS.VERBOSE :  print "Running command :  {}".format( "crab resubmit " + fn   )


