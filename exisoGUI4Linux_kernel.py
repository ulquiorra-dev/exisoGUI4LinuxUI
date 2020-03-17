__author__ = 'francisco'
__email__ = "bosito7@gmail.com"

"""This file content al functions to interact whitch exiso
   The program exiso has to be in the same folder"""

import os
import commands
import subprocess

Status = []
"""Quantity of files in an ISOs"""
NISOFiles = 0
"""Actual file in a ISO"""
ActFileInISOCount = 0
"""Actual ISO in a list of ISOs"""
ActISOFile = 0
"""List of ISOs"""
ISOsList = []
"""Longs"""
Logs = []
"""Conversion of ISOs ended"""
TaskEnded = True

extract_popen = object()

def GetFolderISOFiles(Path):
    """This funtion return one list whits the path of ISOs in the folder path insired in parameter"""
    ISOFiles = []
    for file in os.listdir(Path):
        if file[-3:] == 'iso' or file[-3:] == 'ISO':
            ISOFiles.append(Path + '/' +file)
    print(ISOFiles)
    return ISOFiles

def NumberOfFilesInISO(XISOPath, XSystemUpdateFolder):
    """This funtion return integer the number of files in ISO"""
    command='./extract-xiso -l '
    if XSystemUpdateFolder == True:
        command = command + '-s '
    command = command + '"' + XISOPath + '"'
    print(command)
    commandOut = commands.getstatusoutput(command)
    commandOut = commandOut[1].split('\n')
    global Logs
    Logs.append(commandOut)
    NOF = int(commandOut[-1].split(' ')[0])
    print('Number of files')
    print(NOF)
    global NISOFiles
    NISOFiles = NOF
    return NOF #Retornar el numero de ficheros

def ExtractFilesInISO(XISOPath, ExtractPath, XSystemUpdateFolder):
    """This funtion extract the files in ISO"""
    command=['./extract-xiso', '-x']
    if XSystemUpdateFolder == True:
        command.append('-s')
    command.append(XISOPath)
    command.append('-d')
    command.append(ExtractPath)
    print(command)
    sp = subprocess
    global extract_popen
    extract_popen = subprocess.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    global ActFileInISOCount
    ActFileInISOCount = -1
    for line in extract_popen.stdout:
        Status = line
        print(Status)
        if Status.split(' ')[0] == 'extracting' :
            ActFileInISOCount = ActFileInISOCount + 1
    extract_popen.wait()



def ProcManyISOs(ListOfISOSs, XSystemUpdateFolder):
    global ActISOFile
    global TaskEnded
    if(TaskEnded):
        TaskEnded = False
        for ISO in ListOfISOSs:
            NumberOfFilesInISO(ISO, XSystemUpdateFolder)
            ExtractFilesInISO(ISO, ISO[:-4], XSystemUpdateFolder)
            ActISOFile = ActISOFile + 1
        TaskEnded = True



#GetFolderISOFiles('/media/francisco/2FEF84C4658A4E73/ZMEGA')/media/francisco/2FEF84C4658A4E73/ZMEGA/X360/Madagascar Karts/
#NumberOfFilesInISO('/media/francisco/2FEF84C4658A4E73/ZMEGA/X360/Midle eart/MidleearthmordarDVD1.iso',True)
#NumberOfFilesInISO('/media/francisco/2FEF84C4658A4E73/ZMEGA/X360/Midle eart/MidleearthmordarDVD1.iso',False)
#NumberOfFilesInISO1('/media/francisco/2FEF84C4658A4E73/ZMEGA/X360/Midle eart/MidleearthmordarDVD1.iso',True)

#ExtractFilesInISO('/media/DATOS/zDownloads/x360/Tropico 5/Tro pico 5.DownloadsFull.Net/complex-tropico5/complex-tropico5/complex-tropico5.iso','/media/DATOS/zDownloads/x360/Tropico 5/Tropico 5',True)
#ExtractFilesInISO('/media/francisco/2FEF84C4658A4E73/ZMEGA/X360/Midle eart/MidleearthmordarDVD1.iso','/media/francisco/2FEF84C4658A4E73/ZMEGA/X360/Midle eart/ME',True)
#a = ['/media/francisco/2FEF84C4658A4E73/ZMEGA/X360/Midle eart/MidleearthmordarDVD1.iso','/media/francisco/2FEF84C4658A4E73/ZMEGA/X360/Midle eart/MidleearthmordarDVD2.iso']
#ProcManyISOs(a, True)
#print(NISOFiles)
#print(ActFileCount)