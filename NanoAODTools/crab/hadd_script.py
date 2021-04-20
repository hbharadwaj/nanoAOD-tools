import argparse
import subprocess
import sys
import os
import readline
import string
import nano_files_2017

SAMPLES = {}

SAMPLES.update(nano_files_2017.mc2017_samples)

parse = argparse.ArgumentParser(prog='NTupleReader')

# parse.add_argument('--s', dest = 'SELECTED', default= None) 
parse.add_argument('input_directory_orig', type = str, nargs = 1, help = 'The directory you would like to access')
parse.add_argument('output_directory_orig', type = str, nargs = 1, help = 'The directory you would like your output file to go in' )
#parse.add_argument('file_name_orig', type = str, nargs =1, help = 'The name of the output file')
parse.add_argument('file_extension_orig', type = str, default = '.root', nargs = 1, help = 'The file extension for the files you want recorded in the output file' )
parse.add_argument('file_keyword_orig', type = str, default = 'histos', nargs = 1, help = ' part of filename e.g. histos or  trees' )
parse.add_argument( '--delve', default = True, help = 'If marked true, subdirectories of the given directory will be entered and their contents with the specified extension will be coppied to the output file. Default value is false')
parse.add_argument('--append', default = False, help = 'If marked true, the output file listed will be appended with the files found in the specified search directory. default is false')
args = parse.parse_args()


def hadd4CRAB3(input_directory,output_directory,file_name,file_extension = '.root',file_keyword = 'hists'):
    #obtain input file directory
    inputDirectory = input_directory

    #obtain placement directory and ensure proper format
    preplacementDirectory = output_directory.split(os.sep)

    placementDirectory = ""

    for parts in preplacementDirectory:
        placementDirectory = placementDirectory + parts + "/"

    #obtain the new filename
    fileName = file_name
    rootfileName = str(file_name) + str(file_extension)

    #otain the file type extension to be used and put in the output file
    fileType = file_extension
    fileKeyword = file_keyword

    #create and open the file in the desired directory
    os.chdir(placementDirectory)

    if args.append == False:
        if os.path.isfile(str(preplacementDirectory) + str(fileName) + ".txt") == True:
            if raw_input( "WARNING: The file you wanted to create already exists. Do you want to overwrite it? enter 'N' to escape: ") == "N" or "n" or "No" or "no" or "NO":
                print "script cancelled"
                sys.exit()
        myfile = open(placementDirectory + fileName + ".sh", 'w')
        
    if args.append == True:
        myfile = open(placementDirectory + fileName + ".sh", 'a')


    # create a list of files to hadd
    myfilelist = []
    filestring = '  '
    #enter specified root directory and recursively enter all subdirectories to get pertinent files
    if args.delve == True:
        print("Searching specified directory and all subdirectories for " + fileType + " and adding them to the output file")
        dirlist = []
        commandis = "ls -u "+ inputDirectory     #"xrdfs  root://cmseos.fnal.gov/  ls -u "+ inputDirectory  
        for eosDir1 in os.popen( commandis  ).read().split('\n'):
            #print(commandis +eosDir1+"/")
            for eosDir2 in filter(None,os.popen( commandis +eosDir1+"/" ).read().split('\n')):
                #print(commandis +eosDir1+"/"+eosDir2+"/")
                for eosDir3 in filter(None,os.popen( commandis +eosDir1+"/"+eosDir2+"/" ).read().split('\n')):
                    #print(commandis +eosDir1+"/"+eosDir2+"/"+eosDir3+"/")
                    for eosDir in filter(None,os.popen( commandis +eosDir1+"/" +eosDir2+"/" +eosDir3+"/"  ).read().split('\n')):
                        dirlist.append(eosDir)
                        print"The eosDir is {}".format(eosDir)
                        for eosFile in filter(None,os.popen(" ls -u "+ inputDirectory+eosDir1+"/" +eosDir2+"/" +eosDir3+"/"+ eosDir).read().split('\n')) :
                            filenameFull =  eosFile
                            if filenameFull.endswith(fileType) and "fail" not in inputDirectory.split(os.sep) :
                                if fileKeyword in filenameFull :
                                    myfilelist.append(filenameFull)  
                                    filestring += ' '+ inputDirectory +eosDir1+"/" +eosDir2+"/" +eosDir3+"/"+ eosDir +'/'+ filenameFull     
                                    print"Adding file to list for hadd: {}".format(filenameFull)
    #enter only the specified directory and copy file names
    else:( rootfileName)
    #haddCmd.append(' ') 
    #haddCmd.append(filestring)
    #haddCmd.append( file.replace( idirs[0], odir ) )
    #for dir in idirs:
    #    haddCmd.append( file.replace( idirs[0], dir ) )
    #import pdb; pdb.set_trace()
    #cmd = ' '.join(haddCmd)

    cmd = 'hadd ' + rootfileName + filestring
    print cmd
    myfile.write(cmd)
    print"hadd command written to file {}".format(myfile)
    myfile.close()
    #os.system(cmd)

    subprocess.call( cmd   , shell=True)


out_dir = args.output_directory_orig[0]

if not (os.path.exists(out_dir)):
    os.makedirs(out_dir)

for key, item in SAMPLES.items() :
    print ''
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ new MC or data sample $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"  
    print key
    print args.input_directory_orig[0]+str(key)+"/"
    print out_dir
    print ''

    if(os.path.exists(args.input_directory_orig[0]+str(key))):
        hadd4CRAB3(args.input_directory_orig[0]+str(key)+"/",out_dir,key)


year = "2017"
addedFilesData = {"2017": []}
addedFilesMc = {"2017": []}
addedFilesTTV = {"2017": []}
addedFilesWZ = {"2017": []}
addedFilesZZ = {"2017": []}
addedFilesTTbar = {"2017": []}

out_dir_h = out_dir #+ '/haddedFiles/'
if not (os.path.exists(out_dir_h)):
    os.makedirs(out_dir_h)

for key, value in SAMPLES.items():
    if value[1]=='data':
        addedFilesData[year].append( out_dir + key + '.root ')
    elif ('TTWJetsToLNu' in key) or ('TTZToLLNuNu' in  key):
        addedFilesTTV[year].append(  out_dir + key + '.root ')
    elif ('WZTo3LNu' in key):
        addedFilesWZ[year].append(  out_dir + key + '.root ')
    elif ('ZZTo4L' in key):
        addedFilesZZ[year].append(  out_dir + key + '.root ')
    elif ('TTTo2L2Nu' in key):
        addedFilesTTbar[year].append(  out_dir + key + '.root ')
    elif ('LFV' not in key):
        addedFilesMc[year].append(  out_dir + key + '.root ')
    else:
        hadd='hadd ' + out_dir + key + '.root '

# os.system('rm *_data.root')
# os.system('rm *_others.root')
# os.system('rm *_TTV.root')
# os.system('rm *_WZ.root')
# os.system('rm *_ZZ.root')
# os.system('rm *_TTbar.root')

# hadddata_2017 ='hadd'+ out_dir_h + '2017_data' + '.root ' + ' '.join(addedFilesData['2017'])
haddmc_2017 ='hadd'+ out_dir_h + '2017_others' + '.root ' + ' '.join(addedFilesMc['2017'])
haddTTV_2017 ='hadd'+ out_dir_h + '2017_TTV' + '.root ' + ' '.join(addedFilesTTV['2017'])
haddWZ_2017 ='hadd'+ out_dir_h + '2017_WZ' + '.root ' + ' '.join(addedFilesWZ['2017'])
haddZZ_2017 ='hadd'+ out_dir_h + '2017_ZZ' + '.root ' + ' '.join(addedFilesZZ['2017'])
haddTTbar_2017 ='hadd'+ out_dir_h + '2017_TTbar' + '.root ' + ' '.join(addedFilesTTbar['2017'])

os.system(haddmc_2017)
os.system(haddTTV_2017)
os.system(haddWZ_2017)
os.system(haddZZ_2017)
os.system(haddTTbar_2017)
